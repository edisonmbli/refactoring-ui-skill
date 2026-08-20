#!/usr/bin/env python3
"""
Turn a design-tokens.json into the artifacts a project can actually consume.

Emits, from one source of truth:
  --format v4       Tailwind v4  @theme block
  --format v3       Tailwind v3  tailwind.config.js fragment
  --format css      framework-neutral CSS custom properties
  --format preview  a self-contained HTML page showing the whole system
  --format all      every one of the above, into --out

Two token layers (see 15-beyond-the-book.md):
  primitive   raw scale values          --color-primary-600
  semantic    meaning, referencing them --color-action

Semantic values use {dot.path} references into primitive. Components should
reference semantic tokens only -- that is what makes dark mode and rebranding
a remap rather than a rewrite.

Stdlib only. No dependencies.
"""
from __future__ import annotations
import argparse, json, os, re, sys

REF = re.compile(r'^\{([a-zA-Z0-9_.-]+)\}$')


def resolve(value, primitive: dict, _seen=None):
    """Resolve a {dot.path} reference into the primitive layer."""
    if not isinstance(value, str):
        return value
    m = REF.match(value.strip())
    if not m:
        return value
    path = m.group(1)
    _seen = _seen or set()
    if path in _seen:
        raise SystemExit(f'circular token reference: {path}')
    node = primitive
    for part in path.split('.'):
        if not isinstance(node, dict) or part not in node:
            raise SystemExit(f'unresolved token reference: {{{path}}}')
        node = node[part]
    if isinstance(node, dict):
        node = node.get('hex') or node.get('value')
        if node is None:
            raise SystemExit(f'reference {{{path}}} points at a group, not a value')
    return resolve(node, primitive, _seen | {path})


def flatten(prefix: str, node, primitive: dict, out: list):
    for key, val in node.items():
        name = f'{prefix}-{key}' if prefix else key
        if isinstance(val, dict) and not ('hex' in val or 'value' in val):
            flatten(name, val, primitive, out)
        else:
            out.append((name, resolve(val, primitive)))


def collect(tokens: dict) -> tuple[list, list]:
    prim, sem = tokens.get('primitive', {}), tokens.get('semantic', {})
    p, s = [], []
    flatten('', prim, prim, p)
    flatten('', sem, prim, s)
    return p, s


def emit_v4(tokens: dict) -> str:
    p, s = collect(tokens)
    L = ['@import "tailwindcss";', '', '@theme {']
    L.append('  /* primitive */')
    L += [f'  --{k}: {v};' for k, v in p]
    if s:
        L += ['', '  /* semantic -- components should use these */']
        L += [f'  --{k}: {v};' for k, v in s]
    L.append('}')
    return '\n'.join(L) + '\n'


def emit_css(tokens: dict) -> str:
    p, s = collect(tokens)
    L = [':root {', '  /* primitive */']
    L += [f'  --{k}: {v};' for k, v in p]
    if s:
        L += ['', '  /* semantic */'] + [f'  --{k}: {v};' for k, v in s]
    L.append('}')
    return '\n'.join(L) + '\n'


def _js(node, primitive: dict, indent: int = 6) -> str:
    pad, out = ' ' * indent, []
    for k, v in node.items():
        key = k if re.match(r'^[A-Za-z_$][\w$]*$', k) else f"'{k}'"
        if isinstance(v, dict) and not ('hex' in v or 'value' in v):
            out.append(f'{pad}{key}: {{\n{_js(v, primitive, indent + 2)}\n{pad}}},')
        else:
            out.append(f"{pad}{key}: '{resolve(v, primitive)}',")
    return '\n'.join(out)


def emit_v3(tokens: dict) -> str:
    prim = tokens.get('primitive', {})
    # v3 namespaces differ from the flat --color-* / --text-* of v4
    NS = {'color': 'colors', 'font': 'fontFamily', 'text': 'fontSize',
          'space': 'spacing', 'radius': 'borderRadius', 'shadow': 'boxShadow',
          'weight': 'fontWeight', 'leading': 'lineHeight'}
    L = ['/** @type {import("tailwindcss").Config} */', 'module.exports = {',
         '  theme: {', '    extend: {']
    for key, ns in NS.items():
        if key in prim:
            L.append(f'      {ns}: {{\n{_js(prim[key], prim, 8)}\n      }},')
    L += ['    },', '  },', '};']
    return '\n'.join(L) + '\n'


def emit_preview(tokens: dict) -> str:
    prim = tokens.get('primitive', {})
    meta = tokens.get('$meta', {})
    ramps = prim.get('color', {})

    def swatches(name, ramp):
        cells = ''.join(
            f'<div class="sw"><span style="background:{resolve(v, prim)}"></span>'
            f'<code>{k}</code><code class="hex">{resolve(v, prim)}</code></div>'
            for k, v in ramp.items())
        return f'<h3>{name}</h3><div class="ramp">{cells}</div>'

    color_html = ''.join(swatches(n, r) for n, r in ramps.items()
                         if isinstance(r, dict))
    type_html = ''.join(
        f'<div class="row"><code>{k}</code>'
        f'<span style="font-size:{resolve(v, prim)}">The quick brown fox</span></div>'
        for k, v in prim.get('text', {}).items())
    space_html = ''.join(
        f'<div class="row"><code>{k}</code><i style="width:{resolve(v, prim)}"></i>'
        f'<code class="hex">{resolve(v, prim)}</code></div>'
        for k, v in prim.get('space', {}).items())
    shadow_html = ''.join(
        f'<div class="sh"><div style="box-shadow:{resolve(v, prim)}"></div>'
        f'<code>{k}</code></div>'
        for k, v in prim.get('shadow', {}).items())
    radius_html = ''.join(
        f'<div class="sh"><div style="border-radius:{resolve(v, prim)};'
        f'background:#e5e7eb"></div><code>{k}</code></div>'
        for k, v in prim.get('radius', {}).items())

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{meta.get('name', 'Design system')}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; margin: 0; padding: 3rem 2rem;
         max-width: 68rem; margin-inline: auto; background: #fff; color: #111827; }}
  h1 {{ font-size: 1.75rem; letter-spacing: -.02em; margin: 0 0 .25rem; }}
  .sub {{ color: #6b7280; margin: 0 0 3rem; }}
  h2 {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .08em;
        color: #6b7280; margin: 3rem 0 1rem; }}
  h3 {{ font-size: .875rem; font-weight: 600; margin: 1.5rem 0 .5rem; }}
  .ramp {{ display: flex; flex-wrap: wrap; gap: .5rem; }}
  .sw {{ display: flex; flex-direction: column; gap: .25rem; }}
  .sw span {{ display: block; width: 4.5rem; height: 3rem; border-radius: .375rem;
              box-shadow: inset 0 0 0 1px rgb(0 0 0 / .06); }}
  code {{ font: 12px ui-monospace, monospace; color: #374151; }}
  .hex {{ color: #9ca3af; }}
  .row {{ display: flex; align-items: baseline; gap: 1rem; padding: .35rem 0;
          border-bottom: 1px solid #f3f4f6; }}
  .row > code:first-child {{ width: 4rem; flex: none; color: #6b7280; }}
  .row i {{ display: block; height: .75rem; background: #6366f1; border-radius: 2px; }}
  .sheets {{ display: flex; flex-wrap: wrap; gap: 2rem; }}
  .sh {{ text-align: center; }}
  .sh div {{ width: 5rem; height: 5rem; background: #fff; border-radius: .5rem;
             margin-bottom: .5rem; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #111827; color: #f9fafb; }}
    code {{ color: #d1d5db; }} .row {{ border-color: #1f2937; }}
    .sh div {{ background: #1f2937; }}
  }}
</style></head><body>
<h1>{meta.get('name', 'Design system')}</h1>
<p class="sub">Generated by the refactoring-ui skill. Scales follow
<em>Refactoring UI</em> ch. 3&ndash;6.</p>
<h2>Color &mdash; &sect;5.2, &sect;5.3.3</h2>{color_html}
<h2>Type scale &mdash; &sect;4.1.1d</h2>{type_html}
<h2>Spacing &mdash; &sect;3.2.2</h2>{space_html}
<h2>Elevation &mdash; &sect;6.2.1</h2><div class="sheets">{shadow_html}</div>
<h2>Radius &mdash; &sect;1.4.3</h2><div class="sheets">{radius_html}</div>
</body></html>
"""


FORMATS = {'v4': ('theme.css', emit_v4), 'v3': ('tailwind.config.js', emit_v3),
           'css': ('tokens.css', emit_css), 'preview': ('preview.html', emit_preview)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('tokens', help='path to design-tokens.json')
    ap.add_argument('--format', choices=list(FORMATS) + ['all'], default='v4')
    ap.add_argument('--out', help='directory to write into (default: stdout)')
    a = ap.parse_args()

    tokens = json.load(open(a.tokens, encoding='utf-8'))
    targets = list(FORMATS) if a.format == 'all' else [a.format]

    for fmt in targets:
        filename, fn = FORMATS[fmt]
        body = fn(tokens)
        if a.out:
            os.makedirs(a.out, exist_ok=True)
            path = os.path.join(a.out, filename)
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(body)
            print(f'wrote {path}', file=sys.stderr)
        else:
            print(body)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
