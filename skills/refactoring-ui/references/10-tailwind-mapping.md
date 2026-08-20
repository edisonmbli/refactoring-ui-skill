# Tailwind Mapping

> Aggregates the **103 rules** marked `TW` in `00-coverage-matrix.md` into one lookup, plus the v3/v4 differences and the theme-authoring procedure.
> Load this when translating any rule into code, or when writing/editing a theme.

**Notation.** `{primary}` / `{neutral}` / `{danger}` / `{accent}` are placeholders for the project's own ramps — resolve them from the project's tokens (Step 0), never emit a brace and never default to Tailwind's own palette names unless the project actually uses them.

---

## Why the mapping is this direct

Adam Wathan wrote this book and then wrote Tailwind. The framework is the book's systems expressed as a tool, so most rules have a one-utility translation rather than an interpretation:

| Book system | Tailwind |
|---|---|
| Type scale `12 14 16 18 20 24 30 36 48 60 72` (§4.1.1d) | `text-xs` → `text-7xl`, exactly |
| Spacing scale, 16px base (§3.2.2) | default spacing scale, exactly |
| 9-step color ramps `100`–`900` (§5.3.3) | default ramp structure, exactly |
| 5-level elevation (§6.2.1) | `shadow-sm` → `shadow-2xl` |
| Constrained choice (§1.5) | utility classes as a closed set |

**The corollary matters more than the mapping:** arbitrary-value syntax — `p-[13px]`, `text-[15px]`, `bg-[#4f46e5]` — is Tailwind's escape hatch out of the system, and using it re-creates the exact problem §1.5 exists to solve. Treat every arbitrary value as a finding unless it's on the justified list at the bottom of this file.

---

## v3 vs v4

Detect the version in Step 0. It changes where the theme lives, not what goes in it.

| | v3 | v4 |
|---|---|---|
| Theme location | `tailwind.config.js` | `@theme { }` in CSS |
| Entry point | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| Token form | JS object under `theme.extend` | CSS custom properties |
| Tokens readable at runtime | no | yes — they *are* CSS variables |
| Shadow | `boxShadow` key | `--shadow-*` |
| Opacity syntax | `bg-black bg-opacity-50` (or `/50`) | `bg-black/50` |

**v4:**

```css
@import "tailwindcss";

@theme {
  --color-primary-50:  hsl(...);
  --color-primary-500: hsl(...);
  --color-primary-900: hsl(...);
  --font-sans: "Inter", system-ui, sans-serif;
  --radius-DEFAULT: 0.375rem;
  --shadow-md: 0 4px 6px hsla(0,0%,0%,.2);
}
```

**v3:**

```js
module.exports = {
  theme: {
    extend: {
      colors:    { primary: { 50: 'hsl(...)', 500: 'hsl(...)', 900: 'hsl(...)' } },
      fontFamily:{ sans: ['Inter', 'system-ui', 'sans-serif'] },
      borderRadius: { DEFAULT: '0.375rem' },
      boxShadow: { md: '0 4px 6px hsla(0,0%,0%,.2)' },
    },
  },
}
```

One v4 consequence worth knowing: because tokens are real CSS variables, they're readable from JS and usable in plain CSS outside Tailwind — which makes v4 the better target when the project also has non-Tailwind styling to keep in sync.

---

## Rule → utility

### Ch 1 · Starting from Scratch

| Rule | Utility |
|---|---|
| §1.2.1 Hold the color | Build with `{neutral}` utilities only; introduce `{primary}` last |
| §1.4.1 Font choice | One `--font-sans` decision; add a display face only if the personality needs it |
| §1.4.2 Color | Becomes the `{primary}` hue |
| §1.4.3 Border radius | `--radius-*` set once; **the same step on buttons, inputs, cards, modals** |
| §1.5.1 Define systems in advance | The theme block itself |
| §1.5.3 Systematize everything | All **12** systems have a namespace — check `borderWidth` and `opacity`, the two most often left unsystematized |

### Ch 2 · Hierarchy

| Rule | Utility |
|---|---|
| §2.2 Size isn't everything | `font-semibold` before `text-2xl`; `text-{neutral}-500` before `text-xs` |
| §2.2.a Three text colors | `text-{neutral}-900` / `-500` / `-400`; better as `text-primary` / `text-secondary` / `text-muted` aliases |
| §2.2.b Two font weights | `font-normal`/`font-medium` + `font-semibold`/`font-bold`. **`font-light` and `font-thin` do not belong in UI text** |
| §2.3 No grey on colored bg | `text-{primary}-200` on a `bg-{primary}-700` panel — same family, not `text-{neutral}-400` |
| §2.3.a Not white-at-opacity | `text-{primary}-200`, never `text-white/60`. Opacity is for overlays and dividers |
| §2.4 Emphasize by de-emphasizing | Move inactive items `text-{neutral}-700` → `-400` instead of stacking treatments on the active one |
| §2.4.a At section scale | Remove `bg-{neutral}-100` from the sidebar rather than adding `shadow-lg` to the content |
| §2.5.3 Labels are secondary | `text-sm text-{neutral}-500` label above `text-3xl font-semibold text-{neutral}-900` value |
| §2.5.4 When to emphasize a label | `text-{neutral}-900` label, `text-{neutral}-600` value — **one step apart, not three** |
| §2.6 Visual ≠ document hierarchy | `<h1 class="text-base font-semibold">` is fine; `sr-only` to hide visually while keeping semantics |
| §2.7.1 Contrast for weight | `text-{neutral}-400` icon beside `text-{neutral}-900` text. **Watch `currentColor` icon components** — they inherit and silently undo this |
| §2.7.2 Weight for contrast | `border-2 border-{neutral}-200`, not `border border-{neutral}-400` |
| §2.8 / §2.8.a Action pyramid | fill / outline / link — see the button recipe in `12-component-recipes.md` |
| §2.8.1 Destructive actions | `text-{danger}-600 hover:underline` on the page; `bg-{danger}-600 text-white` in the confirmation |

### Ch 3 · Layout and Spacing

| Rule | Utility |
|---|---|
| §3.1 Too much white space | Raise `p-*` / `gap-*` a step or two before touching type or color |
| §3.1.1 Remove, don't add | Start at `p-12`/`gap-12` and step **down** |
| §3.2 / §3.2.3 Use the system | `gap-4` → `gap-6` → `gap-8`. **Never `gap-[22px]`** |
| §3.2.1 25% adjacency | Custom scales must be checked against it explicitly |
| §3.2.2 The scale | Tailwind's default spacing steps, 0.25rem units |
| §3.3 Don't fill the screen | `max-w-xl mx-auto` on the content wrapper, not the outer container |
| §3.3.1 Shrink the canvas | Base utilities = mobile; `sm:`/`md:`/`lg:` = relaxations. Leading with `lg:` is the inverted path |
| §3.3.2 Thinking in columns | `grid grid-cols-1 lg:grid-cols-3`, form spanning two |
| §3.4 Grids are overrated | `grid-cols-12` is available, not mandatory |
| §3.4.1 Not all elements fluid | `flex` + `w-64 shrink-0` sidebar + `flex-1 min-w-0` main. **`min-w-0` is required** or flex children overflow |
| §3.4.2 Max-width, not breakpoints | `w-full max-w-md mx-auto`. `w-1/2 md:w-2/3` reproduces the bug |
| §3.5 Relative sizing | `text-xl md:text-5xl` heading + `text-sm md:text-lg` body — two independent decisions |
| §3.5.1 Within elements | `px-3 py-1.5 text-sm` / `px-4 py-2 text-base` / `px-6 py-3 text-lg`. **Never `px-[1em]`** |
| §3.6 / §3.6.a Ambiguous spacing | `space-y-2` within a group, `space-y-6` between. Headings `mt-12 mb-4` — asymmetric on purpose |

### Ch 4 · Designing Text

| Rule | Utility |
|---|---|
| §4.1 Type scale | `text-xs` → `text-9xl`. **No `text-[15px]`** |
| §4.1.1d The scale | `text-xs` 12 · `sm` 14 · `base` 16 · `lg` 18 · `xl` 20 · `2xl` 24 · `3xl` 30 · `4xl` 36 · `5xl` 48 · `6xl` 60 · `7xl` 72 |
| §4.1.2 Avoid em | Tailwind's type utilities are rem-based. Risk enters via custom CSS and component libraries |
| §4.2.1 Play it safe | Default `font-sans` is close to the book's system stack |
| §4.3 Line length | `max-w-prose` (~65ch), or `max-w-[70ch]` — **one of the few justified arbitrary values** |
| §4.3.1 Wider content | `max-w-5xl` container with `<p class="max-w-prose">` inside |
| §4.4 Baseline, not center | **`items-baseline`, not `items-center`, whenever a flex row mixes font sizes** |
| §4.5 / §4.5.1 / §4.5.2 Line-height | `leading-normal` narrow · `leading-loose` wide · `leading-none`/`leading-tight` on display headings |
| §4.6 Not every link needs color | prose `text-{primary}-600 underline` · dense `font-medium text-{neutral}-900` · ancillary `text-{neutral}-600 hover:underline` |
| §4.7 Align | `text-left` default; every other alignment needs a reason |
| §4.7.1 Don't center long text | Watch `text-center` on a container leaking into children |
| §4.7.2 Right-align numbers | `text-right` + `tabular-nums` |
| §4.7.3 Hyphenate justified | `text-justify hyphens-auto` — **never `text-justify` alone**; needs `lang` on the document |
| §4.8 / §4.8.1 Tighten headlines | `text-5xl tracking-tight` |
| §4.8.2 All-caps | **`uppercase tracking-wide` always travel together** |

### Ch 5 · Working with Color

| Rule | Utility |
|---|---|
| §5.1 HSL | v4 `@theme` accepts HSL directly, so it survives into the theme |
| §5.2.1 Greys | `{neutral}-50` … `-900`, 8–10 stops |
| §5.2.2 Primary | `{primary}-50` … `-900`, aliased semantically |
| §5.2.3 Accents | `--color-danger-600`, **not `--color-red-600`. Components never name a hue** |
| §5.3 Define shades up front | No `color-mix()` or Sass functions at the call site |
| §5.3.3 Ramp construction | Produces Tailwind's `100`–`900` structure; `50`/`950` extend the edges the same way |
| §5.3.4 Greys | Darkest anchored on real body text, lightest on a real background |
| §5.4 Saturation compensation | Tailwind's defaults already do it; **custom ramps must do it explicitly** |
| §5.4.2 Hue rotation | Visible in Tailwind's yellow ramp shifting toward orange as it darkens |
| §5.5 / §5.5.1 Grey temperature | `gray` / `slate` (cool) / `zinc` / `stone` (warm) / `neutral` (near-pure). **Choosing among them *is* the temperature decision — never mix two in one interface** |
| §5.6 Contrast | Verify across the token matrix, not per component |
| §5.6.1 Flip the contrast | `bg-{accent}-100 text-{accent}-800` instead of `bg-{accent}-700 text-white` |
| §5.6.2 Rotate the hue | Needs a hand-picked theme value — the ramp holds hue constant by construction |
| §5.7 Don't rely on color alone | Chart series step **one** ramp (`{primary}-300/-500/-700/-900`), not one family per series |

### Ch 6 · Creating Depth

| Rule | Utility |
|---|---|
| §6.1.1 Light from above | **Every default shadow has a positive Y and zero X offset.** That is this rule |
| §6.1.2 Raised | `shadow-sm` + `ring-1 ring-inset` in a hand-picked light color, or `border-t` a step lighter. **Not `bg-white/20`** |
| §6.1.3 Inset | `shadow-inner` + `border-b` a step lighter. **Sign convention is inverted from raised — most common place to get depth backwards** |
| §6.2 / §6.2.a Elevation | `shadow-sm` buttons · `shadow-md`/`lg` dropdowns · `shadow-2xl` modals |
| §6.2.1 Elevation system | `shadow-sm` → `shadow-2xl`. Book's raw values in `06-depth.md` §6.2.1 |
| §6.2.2 Interaction | `shadow-sm active:shadow-none`; `shadow-lg` on the dragged item |
| §6.3 / §6.3.a Two-part shadows | Tailwind's defaults are already two comma-separated shadows |
| §6.3.1 Elevation fade | Tight shadow's relative weight shrinks from `shadow-sm` to `shadow-2xl`. Custom scales must replicate it |
| §6.4.1 Depth with color | `bg-white` card on `bg-{neutral}-100` page. **Primary elevation mechanism in dark mode** |
| §6.4.2 Solid shadows | `shadow-[0_2px_0_0_var(--color-{neutral}-300)]` — justified arbitrary value; better as a named theme elevation |
| §6.5 Overlap | Negative margins (`-mt-16`) or `relative` + `z-*`. **Verify at mobile widths** |
| §6.5.1 Overlapping images | `ring-4 ring-white` on avatar stacks — **must track the actual background color** |

### Ch 7 · Working with Images

| Rule | Utility |
|---|---|
| §7.2 Text needs consistent contrast | No utility fixes this — **the image must change, not the text color**. Pick from the four below |
| §7.2.2 Overlay | `bg-black/50` layer, or better `bg-gradient-to-t from-black/70` so only the text region darkens |
| §7.2.3 Lower contrast | `contrast-75 brightness-110`, or bake into the asset for hero images |
| §7.2.4 Colorize | `grayscale contrast-75` + `bg-{primary}-700 mix-blend-multiply` |
| §7.2.5 Text shadow | `[text-shadow:0_0_20px_rgb(0_0_0_/_0.6)]` — **zero X *and* zero Y** |
| §7.3.1 Don't scale up icons | `<div class="w-12 h-12 rounded-lg bg-{primary}-100 grid place-items-center"><Icon class="w-6 h-6" /></div>` |
| §7.4.1 Control shape and size | `w-full h-48 object-cover object-center`. Prefer `<img>` over a background image — keeps `alt` |
| §7.4.2 Prevent bleed | `shadow-inner`, or `ring-1 ring-inset ring-black/5`. **Never a solid border** |

### Ch 8 · Finishing Touches

| Rule | Utility |
|---|---|
| §8.1 Supercharge defaults | `list-none` + flex rows for icon bullets; `accent-{primary}-600` for the minimal form-control upgrade |
| §8.2 Accent borders | `border-t-4` card · `border-l-4` alert · `border-b-2` active tab · `w-16 h-1 bg-{primary}-500` under a headline |
| §8.3 Decorate your backgrounds | All three options share one constraint: **keep contrast low** so nothing competes with content |
| §8.3.1 Background color | `bg-{neutral}-50` alternating sections; `bg-gradient-to-br from-{primary}-500 to-{primary}-700`. **Cross-family gradients need the ~30° hue check** |
| §8.3.2 Pattern | Inline SVG data URI; verify legibility at the smallest text size on it |
| §8.3.3 Shape | Absolute SVG, low opacity, `pointer-events-none`, `aria-hidden="true"` |
| §8.4 Empty states | **Conditionally render surrounding controls, don't disable them** |
| §8.5 / §8.5.1 Fewer borders | Try `shadow-sm` before `border`. `ring-1 ring-black/5` is the semi-transparent middle ground |
| §8.5.2 Two backgrounds | `bg-white` on `bg-{neutral}-50`. **Needs a fine-grained grey ramp — coarse ramps are why this fails** |
| §8.5.3 Extra spacing | `space-y-8` instead of `divide-y` |
| §8.6 Think outside the box | `peer` + `peer-checked:` for selectable cards; `grid grid-cols-2` inside a dropdown panel |

---

## Arbitrary values: the justified list

Every arbitrary value is a finding **except** these, where the arbitrary syntax expresses the rule more directly than any scale step:

| Pattern | Why justified | Rule |
|---|---|---|
| `max-w-[70ch]` | `ch` states the measure constraint literally | §4.3 |
| `shadow-[0_2px_0_0_...]` | Zero-blur solid shadows aren't in the default scale | §6.4.2 |
| `[text-shadow:0_0_20px_...]` | No text-shadow utilities ship by default | §7.2.5 |

In all three cases, promoting the value into the theme as a named token is better still. Anything else — `p-[13px]`, `text-[15px]`, `bg-[#4f46e5]`, `w-[347px]` — is §1.5 being violated.

---

## Detecting the version

```bash
grep -r '@import "tailwindcss"' --include=*.css .   # v4
grep -r '@tailwind base'        --include=*.css .   # v3
grep -E '"tailwindcss":' package.json               # version range
```

If both patterns appear, the project is mid-migration — ask before writing theme code either way.

## Cross-references

- Why constrained sets work → `01-starting-from-scratch.md` §1.5
- Full rule text for anything above → the chapter ref named in the section heading
- Component-level assembly → `12-component-recipes.md`
- Arbitrary values as an audit finding → `13-audit-rubric.md`
- Theme authoring end to end → `11-design-tokens.md`
