#!/usr/bin/env python3
"""
Generate a color ramp using the procedure from Refactoring UI, ch. 5.

Implements, in order:
  §5.3.3  base(500) -> edges(900/100) -> bisect(700/300) -> bisect(800/600/400/200)
  §5.4    saturation rises as lightness moves away from 50%
  §5.4.2  hue rotates toward a brighter/darker hue, capped at 20-30 degrees
  §5.5.1  grey ramps carry a temperature and compensate at both ends

Stdlib only. No dependencies.

  python3 generate_palette.py --base 'hsl(15, 65%, 45%)'
  python3 generate_palette.py --base '#0f7b6c' --extended
  python3 generate_palette.py --grey --temperature cool
  python3 generate_palette.py --base '#eab308' --json
"""
from __future__ import annotations
import argparse, colorsys, json, math, re, sys

# --- §5.4.1 ---------------------------------------------------------------
# Perceived brightness peaks at yellow/cyan/magenta and troughs at red/green/blue.
BRIGHT_HUES = (60.0, 180.0, 300.0)   # rotate toward these to lighten
DARK_HUES   = (0.0, 120.0, 240.0)    # rotate toward these to darken


# --- conversions ----------------------------------------------------------
def hex_to_hsl(s: str) -> tuple[float, float, float]:
    s = s.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f'not a hex color: {s}')
    r, g, b = (int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, sat = colorsys.rgb_to_hls(r, g, b)
    return h * 360, sat * 100, l * 100


def hsl_to_hex(h: float, s: float, l: float) -> str:
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l / 100, s / 100)
    return '#%02x%02x%02x' % tuple(round(c * 255) for c in (r, g, b))


def parse_color(s: str) -> tuple[float, float, float]:
    """Accept #rgb, #rrggbb, or hsl(h, s%, l%)."""
    s = s.strip()
    m = re.match(r'hsl\(\s*([\d.]+)\s*[, ]\s*([\d.]+)%?\s*[, ]\s*([\d.]+)%?\s*\)', s, re.I)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3))
    return hex_to_hsl(s)


def fmt_hsl(h: float, s: float, l: float) -> str:
    return f'hsl({h % 360:.0f}, {s:.0f}%, {l:.0f}%)'


# --- §5.4 saturation compensation -----------------------------------------
def _chroma_headroom(l: float) -> float:
    """HSL chroma = (1 - |2L-1|) * S. This returns the (1 - |2L-1|) term.

    As lightness approaches 0 or 100, headroom approaches 0, which is exactly
    why a constant S looks progressively duller toward the ends of a ramp.
    """
    return max(1e-6, 1.0 - abs(2.0 * (l / 100.0) - 1.0))


def compensate_saturation(s_base: float, l_base: float, l_target: float,
                          strength: float = 0.55) -> float:
    """Raise S as L moves away from 50%, so chroma stays perceptually steady.

    The book states the direction (§5.4) but gives no formula. Full chroma
    compensation is the principled limit; it saturates to 100% almost
    immediately at the ends, so `strength` scales it back. 0.55 tracks the
    behaviour of well-built ramps (including Tailwind's own) closely.
    Set --strength 0 to disable, 1.0 for full chroma preservation.
    """
    if s_base <= 0:
        return 0.0
    ratio = _chroma_headroom(l_base) / _chroma_headroom(l_target)
    return min(100.0, s_base * (ratio ** strength))


# --- §5.4.2 hue rotation --------------------------------------------------
def _signed_delta(frm: float, to: float) -> float:
    """Shortest signed angular distance, in (-180, 180]."""
    return (to - frm + 180.0) % 360.0 - 180.0


def _nearest(h: float, targets: tuple[float, ...], prefer: str = 'auto') -> float:
    """Nearest target hue. Ties are real -- from red (0 deg), yellow (60) and
    magenta (300) are exactly equidistant, and the two produce visibly
    different ramps. `prefer` breaks the tie deliberately rather than by
    tuple order; the book's position is that this is an eye decision (§5.3.5).
    """
    if prefer in ('warm', 'cool'):
        want = 1.0 if prefer == 'warm' else -1.0
        ranked = sorted(targets, key=lambda t: (abs(_signed_delta(h, t)),
                                                -want * _signed_delta(h, t)))
        return ranked[0]
    return min(targets, key=lambda t: abs(_signed_delta(h, t)))


def rotate_hue(h_base: float, l_base: float, l_target: float,
               cap: float = 20.0, prefer: str = 'auto') -> float:
    """Rotate toward a brighter hue to lighten, a darker hue to darken.

    Magnitude scales with how far the lightness moved and is hard-capped:
    past ~20-30 degrees it stops reading as lighter or darker and starts
    reading as a different color (§5.4.2).
    """
    if l_target == l_base:
        return h_base
    lighten = l_target > l_base
    target = _nearest(h_base, BRIGHT_HUES if lighten else DARK_HUES, prefer)
    delta = _signed_delta(h_base, target)
    span = (100.0 - l_base) if lighten else l_base
    if span <= 0:
        return h_base
    progress = min(1.0, abs(l_target - l_base) / span)
    return h_base + max(-cap, min(cap, delta * progress))


# --- §5.3.3 the ladder ----------------------------------------------------
def bisect_lightness(l_light: float, l_base: float, l_dark: float) -> dict[int, float]:
    """900/500/100 -> 700/300 -> 800/600/400/200. The book's exact order."""
    L = {900: l_dark, 500: l_base, 100: l_light}
    L[700] = (L[900] + L[500]) / 2          # midpoints of the two gaps
    L[300] = (L[500] + L[100]) / 2
    L[800] = (L[900] + L[700]) / 2          # then the four that opens up
    L[600] = (L[700] + L[500]) / 2
    L[400] = (L[500] + L[300]) / 2
    L[200] = (L[300] + L[100]) / 2
    return L


def build_ramp(base: tuple[float, float, float],
               l_light: float | None = None,
               l_dark: float | None = None,
               strength: float = 0.55,
               cap: float = 20.0,
               extended: bool = False,
               prefer: str = 'auto') -> dict[int, dict]:
    h0, s0, l0 = base
    l_light = 96.0 if l_light is None else l_light
    l_dark = 21.0 if l_dark is None else l_dark
    if not (l_dark < l0 < l_light):
        raise SystemExit(
            f'base lightness {l0:.0f}% must sit between --darkest {l_dark:.0f}% '
            f'and --lightest {l_light:.0f}%')

    L = bisect_lightness(l_light, l0, l_dark)
    if extended:
        L[50] = l_light + (100.0 - l_light) * 0.55
        L[950] = l_dark * 0.55

    out = {}
    for stop in sorted(L):
        lt = L[stop]
        h = h0 if stop == 500 else rotate_hue(h0, l0, lt, cap, prefer)
        s = s0 if stop == 500 else compensate_saturation(s0, l0, lt, strength)
        out[stop] = {'h': round(h % 360, 1), 's': round(s, 1), 'l': round(lt, 1),
                     'hex': hsl_to_hex(h, s, lt), 'hsl': fmt_hsl(h, s, lt)}
    return out


def grey_base(temperature: str, saturation: float) -> tuple[float, float, float]:
    """§5.5.1 — cool greys lean blue, warm greys lean yellow/orange."""
    hue = {'cool': 220.0, 'warm': 35.0, 'neutral': 0.0}[temperature]
    return hue, (0.0 if temperature == 'neutral' else saturation), 50.0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--base', help="base color, e.g. '#0f7b6c' or 'hsl(15,65%%,45%%)' -- "
                                   "your project's actual brand color, not a default")
    p.add_argument('--grey', action='store_true', help='build a neutral ramp (§5.3.4)')
    p.add_argument('--temperature', choices=('cool', 'warm', 'neutral'), default='cool',
                   help='grey temperature, §5.5.1 (default: cool)')
    p.add_argument('--grey-saturation', type=float, default=12.0,
                   help='how far to push grey temperature (default: 12)')
    p.add_argument('--lightest', type=float, help='lightness%% of stop 100 (default 96)')
    p.add_argument('--darkest', type=float, help='lightness%% of stop 900 (default 21)')
    p.add_argument('--strength', type=float, default=0.55,
                   help='saturation compensation, 0 disables, 1 preserves chroma')
    p.add_argument('--cap', type=float, default=20.0,
                   help='max hue rotation in degrees; book says never exceed 20-30')
    p.add_argument('--extended', action='store_true', help='also emit stops 50 and 950')
    p.add_argument('--toward', choices=('auto', 'warm', 'cool'), default='auto',
                   help='tie-break for hue rotation when two targets are '
                        'equidistant (reds especially): warm leans orange/yellow, '
                        'cool leans magenta/blue')
    p.add_argument('--name', default='color', help='ramp name for output')
    p.add_argument('--json', action='store_true', help='emit JSON instead of a table')
    a = p.parse_args()

    if a.cap > 30:
        print('warning: --cap above 30 deg reads as a different color, not a shade '
              '(§5.4.2)', file=sys.stderr)
    if a.grey:
        base = grey_base(a.temperature, a.grey_saturation)
        name = a.name if a.name != 'color' else 'neutral'
        # §5.3.4 greys run to a subtle off-white, not to white
        light = 98.0 if a.lightest is None else a.lightest
        dark = 17.0 if a.darkest is None else a.darkest
    elif a.base:
        base, name, light, dark = parse_color(a.base), a.name, a.lightest, a.darkest
    else:
        p.error('pass --base COLOR or --grey')

    ramp = build_ramp(base, light, dark, a.strength, a.cap, a.extended, a.toward)

    if a.json:
        print(json.dumps({name: {str(k): v for k, v in ramp.items()}}, indent=2))
    else:
        print(f'{name}   base {fmt_hsl(*base)}   '
              f'strength={a.strength} cap={a.cap}deg')
        print(f'{"stop":>5}  {"hex":<9} {"hsl":<22}')
        for stop, c in ramp.items():
            mark = '  <- base (§5.3.1)' if stop == 500 else ''
            print(f'{stop:>5}  {c["hex"]:<9} {c["hsl"]:<22}{mark}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
