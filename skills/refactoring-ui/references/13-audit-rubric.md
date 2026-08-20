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

**Context hygiene in Sweep mode:** load exactly one lens reference at a time, accumulate its findings, release it before loading the next. Loading all seven at once defeats the progressive-disclosure design and degrades attention on each.

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

One lens at a time, in order. Each chapter reference ends with its own audit checklist — that is the per-lens procedure.

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
