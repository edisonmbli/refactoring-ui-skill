# Beyond the Book

> ⚠️ **Nothing in this file is from *Refactoring UI*.** The book was published in 2018 and does not cover any of it.
>
> Everything here is either **derived** from a book rule (marked → with the source rule) or **imported** from outside it (marked ✚). When applying anything from this file, say so — the user is entitled to know which guidance carries the book's authority and which doesn't.

The book's omissions are not oversights so much as scope and date. Dark mode was not yet standard practice; focus states and motion belong to accessibility and interaction design rather than visual design; semantic token layers are a design-systems concern that postdates it. But a skill that stops where the book stops would emit incomplete design systems, so these are covered here — clearly fenced.

---

## Dark mode

→ **Derived from `§6.4.1`, `§5.4`, `§5.5.1`, `§6.1.1`.** The book's principles determine most of the answers; only the framing is new.

### Elevation stops working

In light mode a raised element casts a shadow, because light comes from above (`§6.1.1`). On a dark background a dark shadow is nearly invisible — the mechanism is intact, the contrast isn't.

`§6.4.1` supplies the replacement: **lighter reads as closer, darker reads as further away.** In dark mode that stops being an alternative and becomes the primary elevation mechanism.

```
surface-0   darkest    page background
surface-1   lighter    cards
surface-2   lighter    dropdowns, popovers
surface-3   lightest   modals
```

Shadows may remain for edge definition; they carry no elevation information. **A dark interface that expresses elevation only through shadows has no elevation.**

### Saturation must rise, not fall

`§5.4`: as lightness moves away from 50%, saturation's perceptual effect weakens. Dark surfaces sit far from 50% lightness, so a palette inverted by flipping lightness alone comes out muddy.

**Increase saturation on dark surfaces.** The light-mode ramp cannot simply be reversed.

### Pure black is wrong for the same reason pure black text is

`§5.2.1` says start from a very dark grey rather than true black, because true black looks unnatural. Same on the other side: a `#000` page background makes every surface above it look like it's glowing, and maximizes eye strain.

### Temperature must hold

`§5.5.1` requires saturation compensation at both ends of the grey ramp so the temperature doesn't drift. Dark mode uses the far end of that ramp exclusively, so drift that was invisible in light mode becomes the dominant impression.

### Contrast inverts asymmetrically

`§5.6` thresholds are unchanged — **4.5:1** and **3:1**. But a mid-tone that passes on white often fails on a dark surface, and pure white text on a dark background is frequently *too* much contrast, producing halation. Slightly-off-white body text is usually better. **Re-verify every pair; don't assume the light-mode matrix transfers.**

### Implementation

Tailwind v4: a `@media (prefers-color-scheme: dark)` block plus a `[data-theme]` override, redefining **only the tokens that change**. Semantic tokens (below) are what make this tractable — with primitive tokens alone, every component needs a `dark:` variant.

---

## Semantic token layer

→ **Derived from `§1.5.1`, `§5.2.3`.** The book says define systems in advance and alias by meaning rather than hue; it doesn't specify a two-layer structure.

Two layers:

```
primitive   --color-blue-600, --color-gray-100, --space-4
semantic    --color-action, --color-surface, --color-text-muted
```

**Components reference semantic tokens only.** Primitives exist so semantics have something to point at.

This is what makes theming possible at all: dark mode, brand variants and white-labeling become a remapping of the semantic layer, with no component changes. Without it, `§5.2.3`'s "components should never name a hue" is unenforceable.

Minimum viable semantic set:

```
surface / surface-raised / surface-sunken
text / text-secondary / text-muted        → §2.2.a, the three tiers
border / border-strong
action / action-hover / action-subtle
danger / warning / success / info         → §5.2.3
```

`text` / `text-secondary` / `text-muted` is `§2.2.a`'s three-color limit expressed as tokens — which is the point: the constraint becomes structural rather than a rule someone has to remember.

---

## Focus states

✚ **Imported.** The book covers contrast (`§5.6`) and not relying on color alone (`§5.7`), but never focus.

**Never remove focus indication without replacing it.** `outline: none` with no substitute makes an interface unusable by keyboard.

- Use `:focus-visible`, not `:focus` — it shows the ring for keyboard users and suppresses it on mouse click, which is what people are usually trying to achieve when they remove it.
- The ring needs **3:1** contrast against the adjacent background. `§5.6`'s large-text threshold is the right analogue.
- A ring must not rely on color alone against its surroundings — offset and thickness carry it too. `§5.7`
- Tailwind: `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-{primary}-500`. The offset is what keeps it visible against the component's own fill.

---

## Target sizes

✚ **Imported.** Not addressed by the book.

- **24×24 CSS px** minimum (WCAG 2.2 AA). **44×44** is the comfortable target and Apple's long-standing guidance.
- Padding counts toward the target; the visual icon can be smaller than its hit area.
- This interacts with `§3.5.1`: a small button variant with disproportionately tight padding can fall below the minimum. Check the smallest variant explicitly.

---

## Motion

✚ **Imported.** Not addressed by the book.

- **Honor `prefers-reduced-motion`.** This is not optional; motion triggers vestibular symptoms for some users.
- Interface transitions: **150–200ms**. Longer feels sluggish for direct manipulation.
- Entrances and exits: **200–300ms**.
- Ease-out for entering, ease-in for leaving.
- Motion should confirm a state change, not announce itself — the same restraint `§6.1.4` applies to depth.
- `§6.2.2`'s shadow-based interaction states are the book's closest analogue: express the change, don't decorate it.

---

## Breakpoints

→ **Derived from `§3.3.1`, `§3.5`, `§3.4.2`.** The book gives the method (mobile-first, large shrinks faster, max-width over grid stepping) but names no breakpoints.

Tailwind's defaults are a reasonable system and satisfy `§3.2.1`'s adjacency principle:

```
sm 640   md 768   lg 1024   xl 1280   2xl 1536
```

Two rules from the book that constrain their use:

- **Add a breakpoint when the design breaks, not on a schedule.** `§3.4.2` — an element with a correct max-width often needs no breakpoint at all.
- **Design mobile first** (`§3.3.1`), which is Tailwind's unprefixed-first model. Leading with `lg:` and overriding downward is the inverted, harder path.

---

## Z-index

→ **Derived from `§1.5.3`, `§6.2`.** The book lists 12 systems and z-index isn't among them, but `§6.2`'s virtual z-axis is exactly this in visual form.

A named scale, not ad-hoc integers:

```
base 0   dropdown 10   sticky 20   overlay 30   modal 40   popover 50   toast 60
```

**Keep it aligned with the elevation scale** (`§6.2.1`). An element at modal z-index with dropdown elevation contradicts itself — the same relationship expressed two ways, disagreeing. `z-index: 9999` anywhere is `§1.5` being violated.

---

## Content and internationalization

✚ **Imported**, with one exception.

- **Design for the longest realistic string, not the demo string.** German and Finnish routinely run 30–40% longer than English. This is `§1.3`'s edge-case warning applied to copy.
- **Design the loading and error states with the feature**, exactly as `§8.4` argues for empty states. → derived from `§8.4`.
- Test with real data volumes. The book's own example — "how should this screen look if the user has 2000 contacts?" (`§1.3`) — is precisely this question.
- RTL: `§4.7` says text aligns to the direction of its language. Logical properties (`ps-4` / `pe-4` rather than `pl-4` / `pr-4`) are how that's implemented.

---

## What still isn't covered

Out of scope for this skill. Say so rather than improvising:

- Information architecture and navigation structure
- Interaction and state-machine design
- Data visualization — a separate discipline with its own rules
- Illustration and iconography creation
- Brand identity beyond `§1.4`'s four personality factors
- Content strategy and UX writing beyond `§1.4.4`'s tone

## Cross-references

- Depth via color, the basis of dark-mode elevation → `06-depth.md` §6.4.1
- Saturation compensation → `05-color.md` §5.4
- Grey temperature → `05-color.md` §5.5.1
- Contrast thresholds → `05-color.md` §5.6
- The 12 systems → `01-starting-from-scratch.md` §1.5.3
- Token emission including the semantic layer → `11-design-tokens.md`
