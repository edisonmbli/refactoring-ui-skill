# Layout and Spacing

> Covers matrix rows **3.1 – 3.6.a** (18 items). Book chapter: *Layout and Spacing*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

Second lens in the audit sweep. Spacing findings come after hierarchy because hierarchy changes what counts as a spacing problem — but they come before everything else, because spacing fixes routinely dissolve complaints that present as color, border or "it just looks cluttered" problems.

---

## 3.1 Start with too much white space

**Rule.** Give every element more room than feels necessary. Space is the cheapest available improvement to almost any interface.

**Why.** Breathing room reads as confidence and lets hierarchy operate — elements that are crowded compete regardless of how they're styled. It is also the fix that requires no taste: you don't have to know what looks good to add space, which makes it the highest-yield move available to someone who doesn't trust their eye.

**How.** Before adjusting anything else on a cramped screen, multiply the spacing and reassess. Most "this looks amateurish" reports are resolved here.

**Values.** None — this is a direction, quantified by §3.2.

**Tailwind.** Raise padding and gap by a step or two on containers before touching typography or color.

**Fails as.** An interface described as cramped, cluttered, dense, or "too much on the screen" when the actual content volume is modest.

### 3.1.1 White space should be removed, not added

**Rule.** Start with far too much space and subtract, rather than adding until it stops looking bad.

**Why.** The two procedures converge on different answers, and this is the mechanism behind most under-spaced UI. Adding space terminates the moment the design stops looking *actively wrong* — that threshold sits well below the point where it looks good. Subtracting terminates when removing more would hurt, which lands at the actual optimum. Same person, same taste, different stopping rule, consistently different result.

There's a second effect: an element examined in isolation looks over-spaced at a value that turns out to be about right once the full interface is assembled. Judging in isolation biases you low, so starting high corrects for it.

**How.** Set spacing to something obviously excessive. Remove one scale step at a time. Stop at the step before it starts feeling tight.

**Values.** None.

**Tailwind.** Practical version: start at `p-12` / `gap-12` and step down through the scale, rather than starting at `p-2` and stepping up.

**Fails as.** Every element having exactly the minimum spacing needed to avoid looking broken — a design that is nowhere wrong and nowhere good.

### 3.1.2 Dense UIs have their place

**Rule.** Density is legitimate, but only as a deliberate decision.

**Why.** Some interfaces genuinely need a lot of information visible simultaneously — a monitoring dashboard, a trading screen, a data grid — and there the busyness is worth paying for. The failure isn't density; it's density arrived at by default, because spacing was added rather than removed and nobody chose anything.

**How.** If the design is dense, be able to say why. If the answer is "it just came out that way," it's §3.1.1, not a density decision.

**Values.** None.

**Tailwind.** A dense surface should use a consistently tighter set of steps from the same scale — not abandon the scale.

**Fails as.** A marketing page as dense as an admin console; or a genuinely information-dense tool spaced like a landing page, forcing constant scrolling.

---

## 3.2 Establish a spacing and sizing system

**Rule.** Choose every spacing and sizing value from a small predefined set. Never nitpick between arbitrary neighbors.

**Why.** Deliberating 120px vs 125px is unwinnable — the options are indistinguishable, so there's no basis for a decision and no confidence in the outcome. It is slow at best, and at worst it produces designs whose inconsistency is visible even when no individual value is wrong. A constrained set converts an open search into a choice among a few clearly different options.

**How.** Adopt the scale in §3.2.2 (or the project's existing one) and take every margin, padding, width and height from it.

**Values.** See §3.2.1 and §3.2.2.

**Tailwind.** Tailwind's spacing scale is this system. The rule in practice: **no arbitrary values** — `p-[13px]` is the violation. If nothing on the scale fits, that's a signal about the scale or the layout, not a license.

**Fails as.** A stylesheet containing 17px, 23px and 38px; components that look subtly misaligned with no single identifiable error.

### 3.2.1 A linear scale won't work

**Rule.** "Everything is a multiple of 4px" is not a system. The scale must account for the **relative** difference between adjacent values.

**Why.** Perception of size is proportional, not absolute. At the small end — icon sizes, button padding — a few pixels is a large proportion: 12px → 16px is a **33%** increase, plainly visible. At the large end, the same absolute change is imperceptible: a card from 500px to 520px is **4%**, roughly **eight times** less significant than the small-end jump. A linear scale therefore offers dozens of indistinguishable options exactly where you least need them, and reintroduces the 120-vs-125 problem it was supposed to solve.

**How.** Space the scale proportionally: tight increments at the bottom, progressively wider ones going up.

**Values.** **No two adjacent values closer than about 25%.** This is the test for whether a scale is usable.

**Tailwind.** Tailwind's spacing scale is linear in its raw units but is *used* proportionally — the steps people actually reach for (2, 4, 6, 8, 12, 16, 24, 32) satisfy the 25% rule. Custom scales must be checked against it explicitly.

**Fails as.** A design system with a 4px-multiple token for every value from 4 to 96, which developers then pick from arbitrarily — a system in name only.

### 3.2.2 Defining the system

**Rule.** Build the scale from factors and multiples of a sensible base.

**Why.** 16px is the right base for two independent reasons: it divides cleanly (0.25×, 0.5×, 0.75× all land on whole pixels), and it is the default font size in every major browser, so the scale stays aligned with type. Deriving from a base rather than choosing values freely means the whole scale is one decision instead of sixteen.

**How.** Take multiples and factors of 16, packed at the low end and progressively further apart going up.

**Values.** The book's scale — **16px base**:

```
4   8   12   16   24   32   48   64   96   128   192   256   384   512   640   768
```

As multiples of 16: 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 40, 48.

Note the proportional spacing in action: the first steps advance by 4px, and the last by 128px.

**Tailwind.** These map onto Tailwind's default spacing steps `1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160, 192` (0.25rem units). The identity is not a coincidence — Tailwind is this book's scale in code form.

**Fails as.** A hand-rolled scale that looks systematic but fails the 25% test somewhere in the middle, usually between 16 and 24.

### 3.2.3 Using the system

**Rule.** Pick from the scale and test neighbors. Don't compute.

**Why.** With a proportional scale, adjacent options look meaningfully different, so the correct one is identifiable by comparison rather than by measurement. This is the process-of-elimination method from `01-starting-from-scratch.md` §1.5.2 applied to space.

**How.** Guess a value. If it's not enough, take the next step up — it's usually right. This is also why designing in the browser is faster than dragging in a design tool: typing a number keeps you on the system, dragging does not.

**Values.** None.

**Tailwind.** `gap-4` → `gap-6` → `gap-8`. Never `gap-[22px]`.

**Fails as.** Developers computing spacing from a formula, or nudging values one pixel at a time in devtools and committing the result.

---

## 3.3 You don't have to fill the whole screen

**Rule.** Available canvas is not an obligation. If the content needs 600px, give it 600px.

**Why.** Large design canvases invite you to fill them, and the result is content spread thinner than it should be — wider than optimal reading measure, elements pushed apart until their relationships stop reading. Extra space around the edges costs nothing; unnecessary width costs comprehension.

This applies within a page as well as to the page. One full-width element — a navigation bar, say — does not oblige the rest of the layout to match. Give each region the width its own content wants.

**How.** Size each region from its contents, not from the viewport. Don't widen something to match a neighbor.

**Values.** Illustrative: **600px** for a focused form is fine on a 1400px screen.

**Tailwind.** `max-w-xl mx-auto` inside a full-width section. Constraint belongs on the content wrapper, not the outer container.

**Fails as.** Dashboards where cards stretch across an ultrawide monitor and rows become unreadable; forms whose inputs are 1200px wide; text running the full width of the browser.

### 3.3.1 Shrink the canvas

**Rule.** When designing something small is hard on a large canvas, make the canvas small. Design mobile first.

**Why.** Real constraints beat remembered ones. On a wide canvas, restraint is a continuous act of will; on a narrow one, it's enforced. And the direction matters: mobile-first forces you to decide what's essential, which is exactly the ranking work hierarchy needs, whereas desktop-first starts from abundance and later asks what to cut — a harder question, answered under pressure.

**How.** Start at roughly a **400px** canvas and design the mobile layout. Then take it to a larger screen and relax whatever felt like a compromise. You'll usually change less than you expect.

**Values.** ~**400px** starting canvas.

**Tailwind.** Matches Tailwind's unprefixed-first model: base utilities are the mobile layout, `sm:` / `md:` / `lg:` are the relaxations. Leading with `lg:` and overriding downward is the inverted, harder path.

**Fails as.** Desktop layouts that collapse awkwardly on phones because the mobile case was derived rather than designed; hidden-on-mobile content that turns out to have been essential.

### 3.3.2 Thinking in columns

**Rule.** When something works best narrow but looks unbalanced in a wide context, split it into columns instead of widening it.

**Why.** This dissolves a false trade-off. The layout wants to use the space; the component wants to stay narrow. Widening sacrifices the component; leaving it narrow sacrifices the composition. A second column uses the space with *different* content — supporting text, help, context — so the form keeps its optimal width and the composition balances.

**How.** Identify content already adjacent to the component (descriptions, help text, section explanation) and move it into a parallel column rather than stacking it above.

**Values.** None.

**Tailwind.** `grid grid-cols-1 lg:grid-cols-3` with the form spanning two columns and supporting text in the third — a common settings-page shape, and this rule is why.

**Fails as.** Settings forms with 900px-wide text inputs; a narrow form marooned in a sea of empty space with its help text crammed above it.

### 3.3.3 Don't force it

**Rule.** The converse: don't cram content into a small area either.

**Why.** "Don't fill the screen" is not "use as little space as possible." Both directions are the same error — letting the container drive the content instead of the reverse.

**How.** If the content needs room, give it room.

**Values.** None.

**Tailwind.** —

**Fails as.** Over-corrected layouts where everything is squeezed into a narrow centered column regardless of what it is — data tables inside `max-w-2xl`.

---

## 3.4 Grids are overrated

**Rule.** A 12-column grid is a useful simplification, not a law. Outsourcing every layout decision to it does more harm than good.

**Why.** Strip away the terminology and a grid system is one thing: fluid, percentage-based widths chosen from a constrained set. In a 12-column grid each column is **8.33%**, and an element is "on the grid" when its width is some multiple of that including gutters. That's genuinely useful — but it is a statement that *everything scales with the viewport*, and that is frequently false.

**How.** Use the grid where fluid width is what you want. Where it isn't, don't.

**Values.** 12-column grid = **8.33%** per column.

**Tailwind.** `grid-cols-12` is available and fine. It is not the only permitted layout, and Flexbox with a fixed sidebar is often more correct.

**Fails as.** Layouts where every element's width is a percentage; a codebase where changing one column count breaks three unrelated components.

### 3.4.1 Not all elements should be fluid

**Rule.** Size an element by what it contains. Fixed width where the content has an optimal size; fluid where it genuinely should scale.

**Why.** The sidebar case makes it concrete. Give a sidebar 3 columns (25%) and the main area 9 (75%), and both failure directions appear: widen the viewport and the sidebar grows too, consuming space the main content would have used better — a navigation list does not benefit from 400px. Narrow the viewport and the sidebar drops below its usable minimum, producing awkward wrapping or truncation. The sidebar's ideal width is a function of its contents and is essentially constant; expressing it as a percentage of the viewport asserts a relationship that doesn't exist.

**How.** Fixed width on the sidebar, optimized for its contents. Main content flexes into the remainder and runs its own internal grid. Applies inside components too — don't use a percentage unless you want the thing to scale.

**Values.** None; derive the fixed width from content.

**Tailwind.** `flex` with `w-64 shrink-0` on the sidebar and `flex-1 min-w-0` on the main region. `min-w-0` matters — without it flex children refuse to shrink below their content and overflow.

**Fails as.** Sidebars with 300px of dead space on wide monitors; navigation labels wrapping to two lines at 1024px; percentage-width icons.

### 3.4.2 Don't shrink an element until you need to

**Rule.** Give elements a max-width and let them shrink only when the viewport falls below it. Don't step widths at breakpoints.

**Why.** Because grid widths are fluid, breakpoint-stepped percentages produce a contradiction. Take a login card at 6 columns (50%) on large screens, widened to 8 columns (~67%) on medium because 50% felt narrow. Since both are percentages of different viewport widths, there is a range where the card is **wider on medium screens than on large ones**. The user experiences the card growing as the window shrinks. And the underlying question was never asked: if 500px is the right width for this card, why should it ever be anything else while there's room?

**How.** Set the optimal width as a max-width. Let it fill available space below that. No breakpoint stepping.

**Values.** Illustrative: **500px** optimal for a login card.

**Tailwind.** `w-full max-w-md mx-auto` — one declaration, no breakpoints, correct at every size. Compare `w-1/2 md:w-2/3`, which reproduces the bug exactly.

**Fails as.** Modals and cards that jump width at breakpoints; an element measurably larger at 900px than at 1100px.

---

## 3.5 Relative sizing doesn't scale

**Rule.** Don't encode size relationships between elements in relative units and expect them to hold across screen sizes.

**Why.** The relationship is not stable, so encoding it encodes something false. Concretely: 18px body copy with 45px headlines suggests defining the headline as **2.5em**. On small screens the body drops to 14px to control measure — and 2.5em now computes to **35px**, far too large for a phone. The right small-screen headline is somewhere around **20–24px**, i.e. **1.5–1.7×** the body. That is a completely different ratio, which means there was never a fixed ratio to capture.

The generalizable form: **elements that are large on large screens must shrink faster than elements that are already small.** The gap between small and large elements should be less extreme on small screens. Proportional scaling preserves that gap and is therefore wrong at both ends.

**How.** Set sizes independently per breakpoint. Shrink big things more aggressively than small things.

**Values.** Desktop **18px** body / **45px** headline (2.5×) → mobile **14px** body / **20–24px** headline (**1.5–1.7×**).

**Tailwind.** `text-xl md:text-5xl` on the headline with `text-sm md:text-lg` on the body — two independent decisions. This is why Tailwind's responsive type utilities are per-breakpoint rather than ratio-based.

**Fails as.** Hero headlines that overflow or dominate on phones; `clamp()` and viewport-unit typography tuned to look right at two sizes and wrong between them.

### 3.5.1 Relationships within elements

**Rule.** The same applies inside a single component. Don't derive a component's padding from its font size.

**Why.** em-based padding does work in the narrow sense — buttons scale and keep their proportions. But preserved proportion is the wrong goal. Uniform scaling is a zoom: the large button is a magnified small button, and it reads that way. What makes a large button feel genuinely large is **disproportionately generous** padding, and what makes a small button feel small is disproportionately tight padding. Independent control is what produces that, and em-derived padding forecloses it.

**How.** Set padding per size variant from the spacing scale. Accept that the ratios differ between variants — that's the feature.

**Values.** Book's example: **16px** font, **16px** horizontal padding, **12px** vertical padding. Larger variants get proportionally more padding, smaller ones proportionally less.

**Tailwind.** `px-3 py-1.5 text-sm` / `px-4 py-2 text-base` / `px-6 py-3 text-lg` — note the horizontal padding grows faster than the font size. `px-[1em]` is the anti-pattern.

**Fails as.** Button size variants that feel like the same button at different zoom levels; small buttons with too much padding and large ones looking cramped.

---

## 3.6 Avoid ambiguous spacing

**Rule.** Whenever spacing alone conveys grouping, the space **around** a group must be greater than the space **within** it.

**Why.** When groups are explicitly separated — a border, a background — membership is unambiguous. Without a separator, proximity is the only signal, and proximity is relative: an element belongs to whatever it is closest to. If the gap below a label equals the gap below its input, the label is equidistant from its own input and the next one, and the grouping is genuinely undetermined by the visual. The reader resolves it from content, which costs effort — and in a form, can mean typing the right data into the wrong field.

This one rule accounts for a large share of "it looks confusing but I can't say why" reactions, because the confusion is real and the cause is invisible.

**How.** For any spacing-grouped set, measure inner and outer gaps and confirm outer > inner by a clear margin. Increase the outer gap in preference to tightening the inner one.

**Values.** None numerically, but the ordering is **strict**: outer > inner, and the difference must be perceptible — one scale step is usually the minimum.

**Tailwind.** `space-y-2` inside a form group, `space-y-6` between groups. The violation is a single uniform `space-y-4` over a mixed list.

**Fails as.** Forms where labels appear to belong to the field above; content that reads as one undifferentiated list when it has structure.

### 3.6.a The four places it shows up

**Rule.** The same error recurs in four distinct contexts. Check all four.

**Why.** It's easy to fix in forms, where it's most discussed, and miss the others — the mechanism is identical but the appearance differs enough to escape notice.

**How.** Check each:

1. **Form groups.** Space below the label must be smaller than space below the input. The most common instance.
2. **Headings above sections.** A heading needs more space above it than below it, or it appears to belong to the preceding section. Very common in long-form content and documentation.
3. **Bulleted lists.** When the gap between bullets equals the line-height of a wrapped bullet, a two-line item is indistinguishable from two items. Set list spacing relative to line-height, not independently.
4. **Horizontal groups.** Identical logic on the horizontal axis — a row of labeled controls, a toolbar of button groups, breadcrumbs. Space between groups must exceed space within them.

**Values.** None.

**Tailwind.**
- Form: `<label class="mb-1">` inside a `<div class="mb-6">`.
- Heading: `mt-12 mb-4` — asymmetric on purpose.
- List: `space-y-3` where `leading-relaxed` makes wrapped lines ~1.625 apart.
- Horizontal: `flex gap-2` within a group, `gap-8` between groups.

**Fails as.** Documentation where headings look attached to the wrong section; lists that read as twice as many items as they contain; toolbars where button grouping is invisible.

---

## Audit checklist for this lens

1. Is the design cramped relative to its content volume? `3.1`
2. Was spacing added up from tight, or removed down from loose? `3.1.1`
3. If dense, is the density deliberate? `3.1.2`
4. Any off-scale values — arbitrary-value utilities, odd pixel numbers? `3.2 3.2.3`
5. Does the project's scale pass the **25%** adjacency test? `3.2.1`
6. Is content stretched to fill the viewport rather than sized to itself? `3.3`
7. Was the mobile layout designed, or derived by collapsing desktop? `3.3.1`
8. Is anything widened past its optimum that could become columns? `3.3.2`
9. Are fixed-size elements (sidebars, icons, cards) given percentage widths? `3.4 3.4.1`
10. Any element wider at a smaller breakpoint than a larger one? `3.4.2`
11. Do large elements shrink faster than small ones on mobile? `3.5`
12. Is component padding em-derived from font size? `3.5.1`
13. **For every spacing-grouped set: is outer > inner?** Check forms, headings, lists, and horizontal groups. `3.6 3.6.a`

## Cross-references

- Why constrained systems work at all → `01-starting-from-scratch.md` §1.5
- Ambiguous spacing frequently presents as a hierarchy problem → `02-hierarchy.md` §2.1
- Type scale, which shares the 25% logic → `04-typography.md` §4.1
- Spacing as an alternative to borders → `08-finishing-touches.md` §8.5.3
- Emitting the scale as tokens → `11-design-tokens.md`
