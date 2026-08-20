# Audit Rubric

> The severity model, finding schema, and sweep procedure for Workflows C (Refine) and D (Audit).
> Load this **first** in either workflow, before any lens reference.

---

## The finding schema

Every finding, whether produced directly or returned by a subagent, uses these fields. Fixed shape is what makes merging and ranking possible.

| Field | Content |
|---|---|
| **Lens** | hierarchy · layout · typography · color · depth · images · finishing |
| **Severity** | P0 · P1 · P2 (below) |
| **Location** | `file:line`, or a named region if the finding came from a screenshot |
| **Rule** | The rule ID, e.g. `§2.3`. **Every finding cites one.** No rule ID means it's an opinion, not a finding |
| **Now** | What the code or render currently does |
| **Proposed** | The specific change, with utilities where applicable |
| **Effort** | S (one-line) · M (one component) · L (systemic or cross-cutting) |
| **Verified** | `rendered` if seen in a screenshot, `code-only` if inferred from source |

Rendered as a table, most severe first:

```
| # | Lens | Sev | Location | Rule | Now | Proposed | Effort |
```

**The rule-ID requirement is the quality gate.** If you cannot name the rule a finding violates, you are reporting taste. Either find the rule or drop the finding — a design review whose items trace to a cited principle is arguable; one that doesn't is just another opinion in the room, which is the thing this skill exists to avoid.

---

## Severity

### P0 — usability is affected

- Hierarchy has collapsed; the user cannot tell what the screen is for. `§2.1`
- Text contrast fails WCAG — under **4.5:1** for normal text, **3:1** for large. `§5.6`
- Information is conveyed by color alone. `§5.7`
- Text over an image is unreadable across part of the image. `§7.2`
- Ambiguous group spacing that could cause a data-entry error. `§3.6`
- Measure far outside **45–75 characters** on body content. `§4.3`
- A destructive action styled as the page's primary action. `§2.8.1`
- Layout breaks or content is inaccessible at a supported viewport.

**Report P0 findings even when the user asked about something else.** They are the one category that overrides scope.

### P1 — consistency is affected

- Off-system values: arbitrary utilities, odd pixel numbers, one-off colors. `§1.5 §3.2 §4.1`
- More than three text colors or more than two font weights. `§2.2.a §2.2.b`
- Grey text on a colored background, or white-at-reduced-opacity text. `§2.3 §2.3.a`
- More than one primary-looking action on a page. `§2.8`
- Inconsistent border radius across components. `§1.4.3`
- Shadows written per component instead of drawn from the elevation set. `§6.2.1`
- Depth cues inconsistent with light-from-above. `§6.1.1`
- Line-height uniform across sizes and widths. `§4.5`
- Uppercase text without letter-spacing. `§4.8.2`
- Icons at the same color as adjacent text. `§2.7.1`
- Mixed font sizes on a line, center-aligned rather than baseline-aligned. `§4.4`

### P2 — polish

- Browser-default bullets, quote marks, form controls. `§8.1`
- Unexploited depth or accent opportunities. `§8.2 §6.4`
- Excess borders that could be shadows, background changes, or space. `§8.5`
- Components rendered exactly as their library ships them. `§8.6`
- Missing background variation on a long page. `§8.3`

**A missing empty state is P0, not P2**, despite living in the Finishing Touches chapter. It is the only state every user is guaranteed to see. `§8.4`

---

## Sweep order

```
hierarchy → layout & spacing → typography → color → depth → images → finishing touches
```

**Not negotiable, and causal rather than conventional:**

- Hierarchy problems change what counts as a spacing problem — content fighting for attention presents simultaneously as a spacing, color and border problem, and none of those fixes work.
- Spacing changes what counts as a border problem — §8.5.3 is literally "add space instead of a border," so unresolved spacing findings generate false border findings.
- Color must settle before depth, because most depth techniques are color decisions in disguise (§6.4.1 is purely a color relationship).
- Finishing touches are meaningless on a broken structure, and several §8.5 techniques become unnecessary once structural work is done.

Auditing out of order produces findings that later findings invalidate, and a report full of items that dissolve on the first fix reads as noise.

**The checklist below is self-contained for the sweep itself.** It carries every item from all seven lenses, each with its rule ID — running it start to finish requires no other file. Load a chapter reference only for two reasons: the user asks *why* a rule exists (`Explain`), or a finding is disputed and needs the full rule text to defend. That keeps the seven-file, load-one-release-one discipline from being a load-bearing assumption about runtime behavior it cannot verify.

---

## Sweep checklist

Run in lens order. Every item cites the rule to reference in a finding; full rule text lives in the chapter file named at each lens heading, needed only for `Explain` or a disputed finding.

### Hierarchy — `02-hierarchy.md`

1. Can you name the single most important element on the screen? `2.1`
2. Are there more than three text colors, or more than two font weights? `2.2.a 2.2.b`
3. Any weight below 400 in UI text? `2.2.b`
4. Any grey text on a colored background, or white-at-reduced-opacity text? `2.3 2.3.a`
5. Is an element accumulating emphasis treatments while a competitor keeps its own? `2.4 2.4.a`
6. Any `label: value` pairs that could be dropped, merged, or demoted? `2.5.1 2.5.2 2.5.3`
7. On spec-style content, is the scanning target the emphasized one? `2.5.4`
8. Are heading sizes inherited from the tag rather than chosen from the rank? `2.6`
9. Icons at the same color as adjacent text? `2.7.1`
10. Faint borders being darkened instead of thickened? `2.7.2`
11. How many primary-looking actions are on the page? More than one is a finding. `2.8 2.8.a`
12. Is a destructive action styled by severity rather than rank? `2.8.1`

### Layout & spacing — `03-layout-spacing.md`

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

### Typography — `04-typography.md`

1. How many distinct font sizes are in use? Are they all on the scale? `4.1 4.1.1d`
2. Is the scale defined in `em`? `4.1.2`
3. Does the UI typeface have enough weights, and is it a text face rather than a display face? `4.2.2 4.2.3`
4. **Measure every paragraph: is it within 45–75 characters (20–35em)?** `4.3`
5. Are paragraphs constrained independently of a wider content area? `4.3.1`
6. Mixed font sizes on one line — baseline-aligned or center-aligned? `4.4`
7. Is line-height uniform across sizes and widths? `4.5 4.5.1 4.5.2`
8. Do large headings still carry body-text line-height? `4.5.2`
9. In link-dense areas, is prose link styling being used? `4.6`
10. Any centered text longer than two or three lines? `4.7.1`
11. Numeric table columns right-aligned? `4.7.2`
12. Any justified text without hyphenation? `4.7.3`
13. Any uppercase text without added letter-spacing? `4.8.2`
14. Large headings that would benefit from tighter tracking? `4.8.1`

### Color — `05-color.md`

1. Is the palette authored in HSL, or in opaque hex? `5.1`
2. Any values transcribed from an HSB picker without conversion? `5.1.1`
3. **Count the greys — are there 8–10?** `5.2.1`
4. Does the primary have 5–10 shades, or only one? `5.2.2`
5. Do semantic states have proper ramps, or improvised colors? `5.2.3`
6. Any `lighten()`/`darken()`/`color-mix()` at the point of use? `5.3`
7. Does the ramp follow **900/500/100 → 700/300 → 800/600/400/200**, and is it perceptually even? `5.3.3`
8. Is the darkest grey chosen against real body text, and the lightest against a real background? `5.3.4`
9. Has the palette grown past its original shade count? `5.3.5`
10. **Does saturation rise toward both ends of every ramp?** `5.4`
11. Do yellow/orange/lime ramps go brown when darkened? `5.4.2`
12. Are the greys pure, or deliberately warm or cool — and is the temperature held at the ends? `5.5 5.5.1`
13. **Measure every text/background pair: 4.5:1 normal, 3:1 large.** `5.6`
14. Any dark saturated blocks that outweigh the page's primary action? `5.6.1`
15. Secondary text inside colored panels — legible and still secondary? `5.6.2`
16. **Any information conveyed by color alone?** `5.7`

### Depth — `06-depth.md`

1. Is light consistently from above — every shadow with a positive Y and zero X offset? `6.1.1`
2. Do raised elements show a light top edge and a shadow below? `6.1.2`
3. Are highlights hand-picked colors, or semi-transparent white? `6.1.2`
4. Are inputs and wells inset — shadow at top, light at bottom? `6.1.3`
5. Are raised-element shadows tight, or large and soft? `6.1.2`
6. **Are shadows drawn from a defined set of five, or written per component?** `6.2.1`
7. Does shadow size track intended z-position — buttons small, dropdowns medium, modals large? `6.2 6.2.a`
8. Do buttons have a pressed state; do draggable items lift? `6.2.2`
9. Where two-part shadows are used, do the two parts do different jobs? `6.3.a`
10. Does the tight contact shadow fade as elevation rises? `6.3.1`
11. In flat or dark interfaces, is depth carried by color relationships? `6.4.1`
12. Any blurred shadows in an otherwise flat design? `6.4.2`
13. Do overlapping images have a background-colored border? `6.5.1`

### Images — `07-images.md`

Skip only after confirming there is no imagery, including icons and avatars.

1. Is the photography good enough to carry the space it occupies? `7.1`
2. Is text over an image consistently readable across the **whole** image? `7.2`
3. If an overlay is used, is it doing the minimum needed? `7.2.2`
4. Was contrast lowered without compensating brightness? `7.2.3`
5. Any text shadow with a non-zero offset? `7.2.5`
6. **Are small icons being displayed at 3–4× their drawn size?** `7.3.1`
7. Are screenshots shrunk to the point of illegibility? `7.3.2`
8. Is the favicon a shrunken full logo? `7.3.3`
9. **Are user-uploaded images constrained with `object-cover` in fixed containers?** `7.4.1`
10. Can a white-background upload bleed into the surface behind it? `7.4.2`

### Finishing touches — `08-finishing-touches.md`

Run only after hierarchy, spacing and typography findings are resolved.

1. Are list bullets, quote marks, links and form controls still browser defaults? `8.1`
2. Would an accent border give a bland card, alert or nav item some identity? `8.2`
3. Does the page have any background variation, or is it uniform throughout? `8.3.1`
4. **Do gradients stay within ~30° of hue?** `8.3.1`
5. Do background patterns or shapes keep low contrast and stay clear of text? `8.3.2 8.3.3`
6. **Does every content-dependent view have a designed empty state?** `8.4`
7. In empty states, is supporting UI hidden rather than disabled? `8.4`
8. Count the borders. Could any be a shadow, a background change, or more space? `8.5`
9. Anything carrying a border *and* a shadow *and* a background change? `8.5.1 8.5.2`
10. Any component rendered as its library default where reinvention would pay? `8.6`

---

## Procedure

### 1. Step 0 — detect

Never audit before detecting the stack (`SKILL.md` → Step 0). Without it you will report a project's deliberate conventions as violations, which destroys the report's credibility faster than missing a finding does.

### 2. Establish what "correct" means here

Before the first lens, answer:

- Does a design system exist? If so, **its rules outrank the book's** on any conflict.
- Which of the **12 systems** (§1.5.3) exist and which are improvised? Missing systems are the highest-leverage L-effort findings.
- What is this surface for? A dense dashboard and a marketing page have different correct answers on spacing (§3.1.2).

### 3. Render and look

Static analysis cannot see measure, real contrast, or how group spacing actually reads. When the project runs:

1. Start the preview, open the page.
2. Screenshot at **1280** and **375**.
3. Judge from pixels.

Mark findings `code-only` when the surface couldn't be rendered. It signals reduced confidence honestly rather than implying verification that didn't happen.

### 4. Sweep

Work the **Sweep checklist** above, lens by lens, in order. It is self-contained — no chapter file needs to be loaded to run it. Open a chapter reference only to explain a rule's *why* or to settle a disputed finding.

### 5. Rank and cut

- Sort by severity, then by effort ascending within a severity.
- **Merge duplicates.** One root cause reported through five symptoms is one finding with five locations.
- **Cut anything you cannot state a failure scenario for.** "This could be better" is not a finding.
- If the list exceeds ~15 items, you are reporting symptoms rather than causes. Look for the systemic finding underneath — usually a missing system from §1.5.3.

---

## Parallel mode

Only when the surface is genuinely large **and** the user agreed. A cold subagent rebuilds context this session already holds, so it pays off across many files, not across one component.

**Dispatch:** one lens per subagent, each given the lens reference, the detected stack, and the finding schema. Each returns findings only — no prose, no recommendations outside the schema.

**Merge:**

1. Deduplicate on `(file, line, rule)`.
2. Where two lenses propose conflicting changes to one element, **the earlier lens in the sweep order wins.**
3. Re-rank globally by severity — subagent-local severity is not comparable across lenses.
4. Drop restatements: findings that survive only as a rephrasing of an earlier one.
5. **Never present raw concatenated subagent output.** Unmerged output is longer than a merged report and worse, which is the opposite of why parallelism was used.

---

## Report format

```markdown
## Design audit — <surface>

**Stack:** <framework>, Tailwind <version>, <design system or "none detected">
**Verified:** rendered at 1280 / 375   ·   or: code-only, project not runnable

### P0 — usability
| # | Lens | Location | Rule | Now | Proposed | Effort |

### P1 — consistency
...

### P2 — polish
...

### Systemic
Findings that are missing systems rather than individual defects.
```

The **Systemic** section is where the report earns its value. Twelve P1 findings about off-scale spacing are one systemic finding — there is no spacing scale — and reporting it that way is the difference between a task list and a diagnosis.

### Language

**Write the report in the user's language.** The rule IDs, utility names and file paths stay as they are.

---

## What not to report

- Anything you cannot tie to a rule ID.
- Deliberate project conventions that merely differ from the book. Note the conflict; don't score it as a defect.
- Findings from a lens with no relevant surface — skip the images lens when there are no images, but confirm first, since **icons and avatars count**.
- Stylistic preferences: a serif choice, a particular hue, a layout you'd have done differently. §1.4 makes personality a legitimate project decision.
- The same finding at twenty locations. Report the pattern once with a count.

## Cross-references

- Per-lens checklists → the audit checklist at the end of each chapter reference
- Symptom-first diagnosis → `14-antipatterns.md`
- Utilities for the Proposed column → `10-tailwind-mapping.md`
- Missing-system findings → `11-design-tokens.md`
- Extensions the book doesn't cover (dark mode, focus, motion) → `15-beyond-the-book.md`
