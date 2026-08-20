# Component Library Adaptation

> How to translate the book's placeholders and rules into a component library's own token contract, instead of the class-per-usage-site model in `12-component-recipes.md`. Load when Step 0 detects a component library with its own theme contract.
> Today this covers **shadcn/ui**, the common case for this skill's audience. Other libraries (MUI, Chakra, Ant Design) belong here too, as their own section, if a real need for them shows up — not as separate files.

---

## Why this needs its own file

Raw Tailwind has one resolution model: a class string at every usage site (`12-component-recipes.md`'s recipes). shadcn/ui has a different one: a **centralized CSS-variable theme** — `--primary`, `--radius`, and friends, defined once in `globals.css`, consumed by every generated component through its `cva` variant definitions.

Applying the raw-Tailwind recipes verbatim to a shadcn project doesn't fail loudly — it produces two color systems that quietly drift apart: one inside `components/ui/*.tsx`'s own variants, one hand-added wherever a `className` override reached for a Tailwind utility instead of a variable. The fix isn't a new rule; it's translating the same rules into the layer shadcn actually reads from.

---

## Detecting shadcn/ui (extends Step 0)

- **`components.json` at the repo root is the reliable signal** — a `components/ui/` folder alone isn't, other setups name folders the same way. Read two fields from it:
  - `tailwind.baseColor` — which Tailwind neutral family (`slate` / `gray` / `zinc` / `neutral` / `stone`) the CSS variables were generated from. **This is the book's §5.5.1 grey-temperature decision, already made at scaffold time** — don't re-ask it, read it.
  - `style` — `default` or `new-york`. Affects the default radius and component density; new-york runs tighter and squarer.
- The variables themselves live wherever `components.json`'s `tailwind.css` points — usually `app/globals.css` — inside `:root { }` and `.dark { }`.
- **Check the value syntax before writing anything.** Tailwind v3 shadcn stores bare HSL triplets (`222.2 47.4% 11.2%`) consumed as `hsl(var(--x))` at the point of use; Tailwind v4 shadcn stores full color functions (`oklch(0.205 0 0)`) consumed directly via `@theme inline`. Writing a full `oklch()` into a v3 variable, or a bare triplet into a v4 one, silently breaks every component reading it.

---

## The variable contract

| shadcn variable | Book/skill placeholder | Notes |
|---|---|---|
| `--background` / `--foreground` | `{neutral}`-50 / `{neutral}`-900 | page canvas and default text |
| `--card` / `--card-foreground` | `{neutral}`-50 (or white) / `{neutral}`-900 | usually one step off `--background` — §8.5.2's two-background separation, pre-wired |
| `--popover` / `--popover-foreground` | same slot as card | dropdowns, popovers |
| `--primary` / `--primary-foreground` | `{primary}`-600 / on-primary text | shadcn's un-customized default is a near-black/near-white pair, **not a brand hue** — see below |
| `--secondary` / `--secondary-foreground` | `{neutral}`-100 / `{neutral}`-900 | the outline-button slot, not `{primary}` at reduced weight |
| `--muted` / `--muted-foreground` | `{neutral}`-100 / `{neutral}`-500 | the book's grey-secondary-text slot, §2.2.a |
| `--accent` / `--accent-foreground` | **not** this skill's `{accent}` | a hover/selected-state highlight (menu rows, dropdown items) — see the collision note below |
| `--destructive` / `--destructive-foreground` | `{danger}`-600 / on-danger text | |
| `--border` / `--input` | `{neutral}`-200 / `{neutral}`-300 | `--input` usually reads a step stronger than a plain divider |
| `--ring` | focus ring, often aliased to `--primary` | verify it doesn't vanish against a `--primary`-filled button — same-color ring on same-color fill is invisible |
| `--radius` | the project's one radius decision, §1.4.3 | v4 derives `sm`/`md`/`lg`/`xl` from it with `calc()`; v3 templates repeat the calc per component |

**Naming collision worth stating plainly:** this skill's `{accent}` placeholder means a semantic state ramp — warning, success, info (`05-color.md` §5.2.3). shadcn's `--accent` means a neutral hover background. **Never resolve `{accent}` from `--accent`.** shadcn ships no warning/success/info variables by default — add `--success` / `--warning` / `--info` (each with its own `-foreground`) following the exact pattern the existing pairs use, rather than repurposing `--accent` for a job it was never built for.

---

## Defaults worth overriding

An un-customized shadcn init is itself a recognizable look, the same way `bg-indigo-600` on `bg-gray-50` is the recognizable AI-generated one (`SKILL.md`, Reading the reference files). Specifically:

1. **`--primary` defaults to a near-black/near-white pair — not a hue.** Left alone, every "primary" button in the project is monochrome. This is the single most common tell that a shadcn project never got a brand color; resolve it through Workflow A like any other primary ramp, don't ship the scaffold default.
2. **`--radius` at its scaffold value** (`0.5rem` default style, `0.625rem` new-york) is instantly recognizable to anyone who has seen a few shadcn sites. Not wrong on its own — §1.4 makes radius a legitimate personality choice — but it should be a choice, not an unexamined default.
3. **Separation defaults to borders, not shadows or background shifts.** shadcn's card, table and input components lean on `--border` almost everywhere out of the box, which is the opposite of §8.5's ordering (try a shadow, try a background change, before a border). Also a legitimate choice — but check it was made, not inherited.
4. **The `baseColor` grey family**, left at whatever `components.json` set at scaffold time. Fine if it matches the project's intended temperature (§5.5.1); worth a deliberate check if the project has since acquired a different personality.

---

## Editing boundary — where a change actually belongs

shadcn has three layers, and reaching for the wrong one first is the most common way a project ends up with two color systems instead of one:

1. **A token value changes** (a color, the radius, a spacing default) → edit the CSS variable in `globals.css`. Never re-declare the value in a `className` override — that's the off-system-value finding (`13-audit-rubric.md`, §1.5 / §3.2) applied to a component library instead of raw Tailwind.
2. **A genuinely new variant** (a button rank the library doesn't ship — a quiet tertiary-link treatment, say) → add a `cva` variant inside `components/ui/button.tsx` itself, once, next to the existing ones. Not copy-pasted at every call site.
3. **One-off composition** — spacing, layout, a single instance's width — → a `className` override via `cn()` at the usage site. This is the only layer where a per-instance class is the correct answer.

Swapping 1 and 3 is the failure mode: a color hand-patched into a `className` at one call site while the component's own `cva` definition still points at the old variable. Both are "correct" by different local readings and the project now has no single source of truth for that color.

---

## Action pyramid in shadcn's own vocabulary

`12-component-recipes.md`'s button ranks map directly onto the `Button` component's `variant` prop — use the prop; rebuilding the recipe in raw classes on top of a shadcn `Button` fights the library instead of using it.

| Rank (§2.8) | shadcn `variant` |
|---|---|
| Primary | `default` |
| Secondary | `outline` or `secondary` |
| Tertiary | `link` or `ghost` |
| Destructive confirmation (§2.8.1) | `destructive` — confirmation dialogs only, never the page-level action |

---

## Cross-references

- Placeholder resolution order → `SKILL.md` → Reading the reference files
- Raw-Tailwind class recipes, for projects without a component library → `12-component-recipes.md`
- Grey temperature and semantic ramps → `05-color.md` §5.5.1 §5.2.3
- Off-system values as an audit finding → `13-audit-rubric.md`
- v3/v4 variable syntax and theme authoring → `10-tailwind-mapping.md`, `11-design-tokens.md`
