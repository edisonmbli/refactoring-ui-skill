# Design Tokens

> The procedure for **Workflow A**: interview → generate → verify → emit.
> Load this whenever the task is establishing a design system, or filling gaps in a partial one.

**What the book supplies and what it doesn't.** *Refactoring UI* gives a complete **method** for building every scale a design system needs — and **not one specific color value**. Every palette pictured in it is an illustration. Do not try to extract "the book's colors"; generate them with the algorithm the book actually specifies.

Fully specified by the book: the palette construction order (§5.3.3), saturation compensation (§5.4), hue rotation (§5.4.2), grey temperature (§5.5.1), contrast thresholds (§5.6), the type scale (§4.1.1d), the spacing scale (§3.2.2), the elevation scale (§6.2.1), font weights (§2.2.b), line-height behavior (§4.5), radius as a personality decision (§1.4.3), and the full list of **12 systems** to build (§1.5.3).

Not in the book, and covered in `15-beyond-the-book.md`: concrete color values, dark mode, the semantic token layer, breakpoints, z-index, motion, focus rings.

---

## Step 1 — Interview

Four rounds maximum, batched, every question skippable. If the user says "just pick for me," take the defaults in the table and go straight to Step 2 — say which defaults you took.

**Ask in the user's language.**

| Round | Question | Default if skipped |
|---|---|---|
| **1 · Context** | What is the product and who uses it? Any existing brand color, typeface, or logo to work from? | none — generate from scratch |
| **2 · Personality** (§1.4) | Three axes: serious ↔ playful · classic ↔ modern · dense ↔ spacious | neutral-modern, spacious |
| **3 · Technical** | Confirm the Step 0 detection: framework, Tailwind version, dark mode needed? | as detected; dark mode yes |
| **4 · Reference** (§1.4.5, §4.2.5) | Any sites whose look you admire? (a URL is enough) | none |

**Round 2 maps to concrete decisions** — this is what makes personality actionable rather than vague (§1.4):

| Axis | Effect |
|---|---|
| serious ↔ playful | radius (§1.4.3): none → small → large; and typeface class (§1.4.1) |
| classic ↔ modern | serif vs neutral sans (§1.4.1); grey temperature (§5.5.1) |
| dense ↔ spacious | which region of the spacing scale is the working default (§3.1.2) |

**Round 4 is worth offering explicitly.** With a URL, the browser tools can read the reference site's actual font stack and computed primary color and use them as a starting point — the systematized version of §4.2.5's "steal from people who care." Extract as a *starting point* to adjust, never as a palette to copy; §1.4.5 warns specifically against looking like a second-rate version of something else.

**Don't ask about:** the type scale, the spacing scale, the elevation scale, or the number of shades. The book settles all four, and offering them as choices invites worse answers than the defaults.

---

## Step 2 — Generate

### Colors

```bash
python3 scripts/generate_palette.py --base '#4f46e5' --name primary
python3 scripts/generate_palette.py --grey --temperature cool --extended --name neutral
python3 scripts/generate_palette.py --base '#dc2626' --toward cool --name danger
```

What the script implements, and why each flag exists:

| Flag | Rule | Notes |
|---|---|---|
| `--base` | §5.3.1 | The 500 stop. Rule of thumb: a color that works as a button background |
| `--lightest` / `--darkest` | §5.3.2 | Defaults 96% / 21%. Book says pick these against real use — darkest is text, lightest is a tinted background |
| `--strength` | §5.4 | Saturation compensation. The book states the *direction* only; 0.55 is our curve. `0` disables, `1.0` preserves chroma exactly |
| `--cap` | §5.4.2 | Hue rotation limit, default 20°. **The book's ceiling is 20–30°** — the script warns above 30 |
| `--toward` | §5.4.2 | Tie-break. From red (0°), yellow (60°) and magenta (300°) are exactly equidistant and produce visibly different ramps. `cool` keeps light reds pink; `warm` makes them peachy |
| `--temperature` | §5.5.1 | `cool` leans blue, `warm` leans yellow/orange, `neutral` is true grey |
| `--extended` | — | Adds stops 50 and 950. Worth it for neutrals, which need surface headroom |

**Ramp counts** (§5.2): **8–10 greys**, **5–10 shades** per primary, ramps for each semantic accent. A complex UI can need **as many as 10 colors × 5–10 shades**.

**No Python available?** The algorithm is hand-executable — it is only bisection plus two adjustments:

1. Pick the base by eye; call it **500**.
2. Pick darkest **900** and lightest **100** against real uses. An alert component exercises both at once (§5.3.2).
3. **700** = the visual midpoint of 900↔500. **300** = the midpoint of 500↔100.
4. **800, 600, 400, 200** = the midpoints of the four gaps that just opened.
5. At each step, **raise saturation** as lightness moves away from 50% (§5.4).
6. At each step, **rotate hue** toward 60/180/300 to lighten or 0/120/240 to darken, **never more than 20–30°** (§5.4.2).

Say you did it by hand — the values will be less even than the script's.

### The other scales

These are settled by the book. Copy them; don't re-derive.

| System | Value | Rule |
|---|---|---|
| Type | `12 14 16 18 20 24 30 36 48 60 72` px | §4.1.1d |
| Spacing | `4 8 12 16 24 32 48 64 96 128 192 256 384 512 640 768` px | §3.2.2 |
| Weights | **two only**: 400 or 500, plus 600 or 700 | §2.2.b |
| Line-height | 1 / 1.25 / 1.5 / 2 — chosen per context, never globally | §4.5 |
| Elevation | **five**: `0 1px 3px` · `0 4px 6px` · `0 5px 15px` · `0 10px 24px` · `0 15px 35px`, all `hsla(0,0%,0%,.2)` | §6.2.1 |
| Radius | one decision from §1.4.3, applied to every component |
| Border width | 1px and 2px — §2.7.2 needs this to be systematic | §1.5.3 |

Check the remaining items on the **12 systems** list (§1.5.3) before declaring the system complete: font size · font weight · line height · color · margin · padding · width · height · box shadow · border radius · border width · opacity. **Border width and opacity are the two most often forgotten.**

---

## Step 3 — Verify

```bash
python3 scripts/check_contrast.py --matrix design-tokens.json
```

Declare in `pairs` every **text-on-background** combination the UI actually produces, and check them as a matrix rather than per component (§5.6). Thresholds: **4.5:1** normal text, **3:1** large. The script exits non-zero on any failure, so it can gate a build.

**Declare only real text pairs.** Decorative borders and dividers do not belong in the matrix — they aren't text, and §2.7.2 says a soft 1px border is the *desired* look. Darkening one to hit a ratio is the overcorrection listed in `14-antipatterns.md` Part 3.

**When a pair fails, don't reflexively darken.** The book gives two better moves:

- **§5.6.1 flip the contrast** — dark colored text on a light tint of the same color, instead of light text on a dark fill. White-on-color needs the background surprisingly dark, and a dark saturated block then dominates a page it wasn't meant to dominate.
- **§5.6.2 rotate the hue** — for colored text on a colored background, rotate toward cyan/magenta/yellow to gain contrast without approaching white, which would erase the distinction from primary text.

**One tension worth naming.** §2.2.a wants three text tiers — dark, grey, lighter grey — and §5.6 sets a floor on how light the third can be. Where they collide, **contrast wins**: tertiary text still has to be readable. In practice this means the muted tier often sits at the ramp's 600 stop rather than 400 or 500. Expect it; it is not a flaw in either rule.

---

## Step 4 — Emit

```bash
python3 scripts/emit_tokens.py design-tokens.json --format all --out ./design
```

**Five deliverables. Not four, not six.**

| # | File | Purpose |
|---|---|---|
| 1 | `design-tokens.json` | Source of truth. Two layers, primitive + semantic |
| 2 | `theme.css` (v4) or `tailwind.config.js` (v3) | Emitted for the **detected** version — never both |
| 3 | `tokens.css` | Framework-neutral custom properties, for projects not on Tailwind and for CSS outside it |
| 4 | `DESIGN.md` | **Human-readable system manual** — written by you, not the script |
| 5 | `preview.html` | Swatches, type scale, spacing, elevation, radius. Publishable as an Artifact for the team |

### The two layers

```
primitive   --color-primary-600   raw scale values
semantic    --color-action        meaning, referencing primitives via {dot.path}
```

**Components reference semantic tokens only.** This is what makes dark mode and rebranding a remap instead of a rewrite, and it is what makes §5.2.3's "components should never name a hue" enforceable. Minimum semantic set in `15-beyond-the-book.md`.

### DESIGN.md is the deliverable that matters most

The script can't write it, and it's what a non-designer actually uses. **In the user's language.** It should carry:

- The personality decisions from Round 2, and what each one produced.
- Each scale, with **when to use which step** — not just the values.
- The three text tiers and the two weights, stated as limits (§2.2.a, §2.2.b).
- The action pyramid: one primary, some secondary, some tertiary (§2.8).
- Grouping spacing: outer must exceed inner (§3.6).
- What is *not* in the system, and what to do when something is missing — which is to add a token deliberately, **not** to write an arbitrary value.
- The rule from §5.3.5: tweaking an existing shade is fine; **adding** shades is what destroys the system.

---

## Filling gaps in an existing system

The common case, and different from building from scratch. Step 0 found a system; it is incomplete.

1. **Inventory against the 12 systems** (§1.5.3). Which exist, which are improvised?
2. **Never overwrite.** The existing system's conventions outrank the book's on any conflict.
3. **Adopt its vocabulary.** If it names greys `slate`, extend `slate` — don't introduce `neutral` alongside it.
4. **Report the gap as one systemic finding**, not as many instances. Twelve off-scale spacing values are one finding: there is no spacing scale.
5. **Generate only the missing scale.** If spacing exists and elevation doesn't, emit elevation alone.

---

## Cross-references

- Why constrained systems work, and the 12-system list → `01-starting-from-scratch.md` §1.5
- Personality → `01-starting-from-scratch.md` §1.4
- Text tiers and weights → `02-hierarchy.md` §2.2
- Spacing scale → `03-layout-spacing.md` §3.2
- Type scale and fonts → `04-typography.md` §4.1, §4.2
- Palette algorithm, in full → `05-color.md` §5.3, §5.4
- Elevation scale → `06-depth.md` §6.2.1
- v3/v4 theme syntax → `10-tailwind-mapping.md`
- Semantic layer, dark mode, breakpoints, z-index → `15-beyond-the-book.md`
