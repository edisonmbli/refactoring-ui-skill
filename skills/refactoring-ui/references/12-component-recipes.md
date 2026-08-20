# Component Recipes

> Book rules assembled into buildable component specs. Load during Workflow B, or when fixing one specific component.
> These are **derivations, not new rules** — every line traces to a rule ID. When a recipe and a chapter reference disagree, the chapter wins.

**Notation.** `{primary}` / `{neutral}` / `{danger}` / `{accent}` are placeholders — resolve from the project's tokens. Sizes and spacing shown are valid scale members but illustrative choices for that example.

---

## Buttons

The action pyramid (`§2.8`) is the whole design. Rank first, then style.

| Rank | Treatment | Rule |
|---|---|---|
| **Primary** | Solid, high-contrast fill | `§2.8.a` |
| **Secondary** | Outline, or low-contrast fill | `§2.8.a` |
| **Tertiary** | Styled as a link | `§2.8.a` |

**One primary per page.** Two means one of them isn't. `§2.8`

```html
<button class="px-4 py-2 rounded-md font-medium
               bg-{primary}-600 text-white
               shadow-sm active:shadow-none">Save changes</button>

<button class="px-4 py-2 rounded-md font-medium
               border border-{neutral}-300 text-{neutral}-700">Preview</button>

<button class="px-2 py-1 font-medium
               text-{neutral}-600 hover:underline">Cancel</button>
```

**Size variants — padding scales faster than font size** (`§3.5.1`). Never derive padding from font size:

```
sm   px-3 py-1.5 text-sm
md   px-4 py-2   text-base
lg   px-6 py-3   text-lg
```

**Depth** (`§6.1.2`, `§6.2`, `§6.2.2`): small tight shadow, not large and soft. Pressed state removes or shrinks it. Any raised highlight is a hand-picked light color, never `bg-white/20`.

**Destructive** (`§2.8.1`): rank honestly. On the page it is usually tertiary — `text-{danger}-600 hover:underline`. The loud `bg-{danger}-600 text-white` treatment belongs in the confirmation dialog, where destroying the thing *is* the primary action.

**Fails as:** every action filled; padding derived in `em`; a large red Delete on a settings page.

---

## Cards

```html
<div class="bg-white rounded-lg p-6 shadow-sm">
```

**Separation** (`§8.5`): pick **one** mechanism. On a `bg-{neutral}-50` page a `bg-white` card needs no border and no shadow — the background difference alone is enough (`§8.5.2`). Border + shadow + background change is three separations doing one job.

**Depth** (`§6.4.1`): lighter than the background reads raised, darker reads inset. This is the primary elevation mechanism in dark mode, where shadows barely register.

**Radius** (`§1.4.3`): the same step as buttons, inputs and modals. Consistency is the rule, not the value.

**Accent** (`§8.2`): `border-t-4 border-{primary}-500` across the top when a set of cards feels bland.

**Internal hierarchy** (`§2.1`): rank the contents. A card where title, body and metadata carry equal weight is the chapter-2 failure in miniature.

**Fails as:** a grid of identical grey boxes; cards with three separation mechanisms; radius that differs from every other component.

---

## Form groups

The spacing is the whole recipe (`§3.6`).

```html
<div class="mb-6">                            <!-- outer: between groups -->
  <label class="block mb-1 text-sm font-medium text-{neutral}-700">Email</label>
  <input class="w-full px-3 py-2 rounded-md
                border border-{neutral}-300 shadow-inner">
  <p class="mt-1 text-sm text-{neutral}-500">We'll never share it.</p>
</div>
```

**`mb-1` inside, `mb-6` between — outer must exceed inner.** Equal spacing makes the label equidistant from its own input and the next one, and the grouping is genuinely undetermined. In a form that means data typed into the wrong field, which is why this is P0 rather than P1. `§3.6 §3.6.a`

**Inputs are inset** (`§6.1.3`): shadow at the top, lighter bottom edge. The sign convention is inverted from raised elements and is the most common place to get depth backwards.

**Width** (`§3.4.2`): `max-w-md`, not a percentage. An input does not benefit from 900px.

**Labels here are required** — `§2.5` is about displaying data, not about form inputs. Accessible labels are untouched by it.

**Custom controls** (`§8.1`): `accent-{primary}-600` is the minimal upgrade from browser-default checkboxes and radios; often enough on its own.

**Fails as:** uniform `space-y-4` down a form; inputs that read as raised; full-width inputs.

---

## Stat blocks and metric cards

Label-value hierarchy (`§2.5.3`) — the data is what matters.

```html
<div>
  <div class="text-sm text-{neutral}-500">Monthly revenue</div>
  <div class="text-3xl font-semibold text-{neutral}-900">$48,200</div>
  <div class="flex items-baseline gap-1 text-sm text-{accent}-600">
    <TrendUpIcon class="w-4 h-4" aria-hidden="true" /> 12.5%
  </div>
</div>
```

- Label demoted by size, contrast and weight together — all three levers are explicitly allowed here. `§2.5.3`
- **`items-baseline`**, not `items-center`, on the mixed-size row. `§4.4`
- **The trend icon is not decoration.** Direction conveyed by color alone is unreadable for red-green colorblind users, and the failure is invisible to everyone else. `§5.7`
- Icon a step softer than the text it sits with. `§2.7.1`

**Inverted case** (`§2.5.4`): on spec-style content where the user scans *for the label*, emphasize the label — `text-{neutral}-900` label, `text-{neutral}-600` value, **one step apart, not three**.

**Fails as:** dashboards where metric names outweigh metrics; trend direction as color alone; centered mixed sizes.

---

## Tables

**Numbers right-aligned** (`§4.7.2`), with `tabular-nums` so digit widths match:

```html
<td class="text-right tabular-nums">$1,284.00</td>
```

**Headers** (`§4.8.2`, `§2.5.3`): `text-xs uppercase tracking-wide text-{neutral}-500` — uppercase and tracking always travel together, and headers are supporting content.

**Separation** (`§8.5`): try alternating row backgrounds or spacing before `divide-y`. If you already have both a background difference and borders, remove the borders.

**Reinvention** (`§8.6`): a column that doesn't need to be sortable can be merged with a related one to create hierarchy. Cells can hold images and color. A table of plain text in uniform columns is a convention, not a requirement.

**Fails as:** left-aligned numeric columns; every cell bordered; a data-rich table rendered as uniform plain text.

---

## Dropdowns and popovers

**Elevation** (`§6.2.a`): medium — `shadow-md` or `shadow-lg`. It sits above the UI but below a modal.

**Reinvention** (`§8.6`): the white-box-with-a-list-of-links image is a convention. It's a floating box — break it into sections, use multiple columns, add supporting text or colorful icons.

```html
<div class="rounded-lg bg-white shadow-lg p-2 grid grid-cols-2 gap-1">
```

**Links inside** (`§4.6`): a dropdown is link-dense, so prose link treatment is overbearing. `font-medium text-{neutral}-900`, not `text-{primary}-600 underline`.

**Fails as:** dropdowns that look glued to the page; every item blue and underlined.

---

## Modals

**Elevation** (`§6.2.a`): large — `shadow-2xl`. This is where you genuinely want to capture attention, and the shadow's job is to separate it from everything behind.

**Contact shadow** (`§6.3.1`): at the highest elevation the tight ambient shadow should be **almost or completely invisible**. A crisp contact shadow makes a floating element look pasted down.

**Width** (`§3.4.2`): `w-full max-w-lg` — one declaration, correct at every viewport. Breakpoint-stepped percentage widths reproduce the wider-at-medium-than-large bug.

**Destructive confirmations** (`§2.8.1`): this is where the loud treatment belongs. `bg-{danger}-600 text-white` on the confirm, tertiary styling on cancel.

**Fails as:** modals at the same elevation as the content behind; percentage widths that jump at breakpoints.

---

## Alerts

The `§5.3.2` component — it exercises both ends of a color ramp at once, which is why the book uses it to pick them.

```html
<div class="border-l-4 border-{danger}-500 bg-{danger}-100 p-4">
  <p class="font-medium text-{danger}-800">Something went wrong</p>
  <p class="text-{danger}-700">Check your connection and try again.</p>
</div>
```

- **Flipped contrast** (`§5.6.1`): dark text on a light tint, not white on a dark fill. White-on-color needs the background surprisingly dark to reach 4.5:1, and a dark saturated block then dominates a page it wasn't meant to dominate.
- Accent border along the side. `§8.2`
- Secondary text stays in the **same color family** — `text-{danger}-700`, never `text-{neutral}-500`. `§2.3`
- Semantic ramp, not a hue name: `--color-danger-*`. `§5.2.3`
- Never color alone — pair with an icon or explicit wording. `§5.7`

**Fails as:** dark saturated banners outweighing page content; grey secondary text on a colored alert.

---

## Empty states

**P0, not polish** (`§8.4`). The only state every user is guaranteed to see.

```html
<div class="text-center py-12">
  <div class="w-16 h-16 mx-auto rounded-full bg-{primary}-100 grid place-items-center">
    <Icon class="w-8 h-8 text-{primary}-600" />
  </div>
  <p class="mt-4 text-lg font-semibold text-{neutral}-900">No projects yet</p>
  <p class="mt-1 text-{neutral}-500">Create your first project to get started.</p>
  <button class="mt-6 px-4 py-2 rounded-md bg-{primary}-600 text-white">New project</button>
</div>
```

- **Hide the surrounding UI.** Tabs, filters, sort controls and search do nothing until content exists. **Conditionally render them — don't disable them.** A disabled filter bar above an empty table is worse than none: it adds noise and states the emptiness twice. `§8.4`
- Icon at its intended size inside a larger shape — **never scaled 3–4×**. `§7.3.1`
- The CTA is the page's primary action here. `§2.8`
- Centered is correct: short, independent blocks. `§4.7.1`

**Fails as:** a bare table with headers and a disabled toolbar; "No results found" as the entire state; an enlarged 16px icon as the illustration.

---

## Navigation

**Emphasize by de-emphasizing** (`§2.4`). This is the chapter's canonical example, and the reflex is wrong: when the active item won't stand out, stop adding treatments to it and soften the inactive ones.

```html
<a class="font-medium text-{neutral}-900">Dashboard</a>   <!-- active -->
<a class="text-{neutral}-400">Reports</a>                 <!-- inactive -->
```

- Accent border marks the active item (`§8.2`) — but if it still doesn't read as active, de-emphasize the others rather than thickening the bar. `§2.4`
- Sidebar: **fixed width** sized to its contents, `w-64 shrink-0`, with `flex-1 min-w-0` on the main region. A nav list gains nothing from 400px, and a percentage sidebar fails in both directions. `§3.4.1`
- If the sidebar competes with the content, **remove its background** rather than escalating the content. `§2.4.a`
- Link treatment: dense context, so weight and color — not prose link styling. `§4.6`

**Fails as:** the eye landing on the sidebar first; percentage-width sidebars; nav labels wrapping at 1024px.

---

## Avatars and avatar groups

**Overlap** (`§6.5`, `§6.5.1`): stacked avatars need an "invisible border" in the background color so they don't clash.

```html
<img class="w-10 h-10 rounded-full object-cover ring-4 ring-white">
```

**The ring must track the actual background.** `ring-white` on a `bg-{neutral}-50` section is visibly wrong — this is the most common way the pattern breaks.

**User uploads** (`§7.4.1`, `§7.4.2`): `object-cover` in a fixed container, never intrinsic aspect ratio. For non-circular thumbnails add `ring-1 ring-inset ring-black/5` so white-background uploads don't bleed into the surface.

**Fails as:** avatar stacks blurring together; stretched profile images; product thumbnails with no edge.

---

## Cross-references

- Full rule text for anything cited → the chapter reference for that number
- Utilities and v3/v4 differences → `10-tailwind-mapping.md`
- Diagnosing an existing component → `14-antipatterns.md`
- Dark mode, focus states, target sizes → `15-beyond-the-book.md`
- Building on shadcn/ui or another component library instead of raw classes → `16-component-libraries.md`
