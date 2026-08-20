# Antipatterns

> Symptom-first lookup: start from what looks wrong, get to the rule.
> Load alongside `13-audit-rubric.md` in Workflows C and D — the rubric gives the procedure, this gives the diagnosis.

The chapter references are organized by principle, which is right for learning and wrong for diagnosis: when something looks off you rarely know which principle it violates. This file inverts the index.

---

## Part 1 — Machine-generated UI

These are the failure modes of LLM-written interfaces specifically. They matter more than the rest of this file for two reasons: they are extremely consistent, and the model producing the interface is usually the one auditing it, so they are the findings most likely to be missed.

**Run this section first when reviewing any AI-generated UI.**

| # | Tell | Why it happens | Rule | Fix |
|---|---|---|---|---|
| 1 | **Indigo/violet primary on a project with no such brand** | Tailwind docs and the entire example corpus use indigo; proximity to examples beats distant instructions | `§1.4.2` | Resolve `{primary}` from the project's actual tokens. If none exist, ask — don't default |
| 2 | **Blue→purple or purple→pink gradients** | Same corpus effect; these gradients are everywhere in generated marketing pages | `§8.3.1` | **Two hues no more than ~30° apart.** Blue→pink is ~200° |
| 3 | **Everything centered** | Center-aligned markup looks balanced in isolation, and generation happens block by block | `§4.7 §4.7.1` | Left-align anything over 2–3 lines. `text-center` on a container leaks to children |
| 4 | **One spacing value everywhere** — `gap-4`, `p-4`, `space-y-4` throughout | Uniform spacing looks tidy in code and destroys grouping | `§3.6` | **Outer > inner.** `space-y-2` within a group, `space-y-6` between |
| 5 | **Emoji as icons** | Zero-dependency and reads as friendly | `§2.7.1 §8.1` | Real icons, contrast-balanced against adjacent text |
| 6 | **Every card carries `shadow-lg`** | Shadow picked for appearance, not for z-position | `§6.2 §6.2.1` | Shadow expresses elevation: `sm` buttons, `md/lg` dropdowns, `2xl` modals |
| 7 | **Border + shadow + background change on the same element** | Each separation added independently, none removed | `§8.5` | Pick one. Usually the background difference alone |
| 8 | **Only two font sizes** — a big one and a small one | Hierarchy carried by size alone | `§2.2` | Add weight and color as levers before adding sizes |
| 9 | **Every action is a filled button** | Semantic styling with no ranking | `§2.8 §2.8.a` | One primary. Secondary outlined, tertiary as a link |
| 10 | **`text-gray-500` on a colored panel** | Grey reads as "de-emphasized" without the mechanism being understood | `§2.3` | Same hue as the background, adjusted S/L |
| 11 | **No empty state** | Generated against imagined populated data | `§8.4` | Design it with the feature. **P0, not polish** |
| 12 | **Arbitrary values** — `p-[13px]`, `text-[15px]` | The requested value wasn't on the scale, so the scale was bypassed | `§1.5 §3.2` | Nearest scale step, or promote to a token. See the justified list in `10-tailwind-mapping.md` |
| 13 | **`items-center` on rows with mixed font sizes** | Vertical centering is the reflex | `§4.4` | `items-baseline` whenever sizes differ |
| 14 | **Uppercase labels with default tracking** | `uppercase` applied alone | `§4.8.2` | `uppercase tracking-wide`, always together |
| 15 | **Full-width text** | No max-width because none was asked for | `§4.3` | `max-w-prose`. **45–75 characters** |
| 16 | **Perfectly proportional responsive scaling** | `text-4xl md:text-6xl` on everything, uniformly | `§3.5` | Large elements shrink **faster** than small ones |
| 17 | **Icons in `currentColor` beside text** | Icon components inherit text color by default | `§2.7.1` | Icons a step or two softer — they cover more area |
| 18 | **Semantic colors used raw** — `text-red-600` for errors | Hue names are what the utility exposes | `§5.2.3` | `--color-danger-600`. Components never name a hue |

**The pattern behind the pattern:** almost every entry is a *local* decision that is individually defensible and wrong in aggregate. Generation is local; design is global. That is the structural reason a generate-only flow needs the audit pass described in `SKILL.md` → *Composing with design generators*.

---

## Part 2 — Symptom → diagnosis

Start from the complaint.

### "It looks busy / noisy / cluttered"

| Check | Rule |
|---|---|
| Is everything the same size, weight and color? | `§2.1` |
| Too little white space overall? | `§3.1` |
| Was spacing added up from tight rather than removed down from loose? | `§3.1.1` |
| Borders on everything? | `§8.5` |
| Multiple elements competing for primary emphasis? | `§2.4 §2.8` |
| Depth effects over-applied? | `§6.1.4` |

### "It looks confusing but I can't say why"

| Check | Rule |
|---|---|
| **Group spacing — is outer greater than inner?** Usually this one | `§3.6 §3.6.a` |
| Headings closer to the section above than below? | `§3.6.a` |
| Mixed font sizes centered rather than baseline-aligned? | `§4.4` |
| Data presented as uniform `label: value` rows? | `§2.5` |
| Depth cues contradicting light-from-above? | `§6.1.1` |

### "It looks amateurish / unfinished / generic"

| Check | Rule |
|---|---|
| Values off the scale, so nothing quite lines up | `§1.5 §3.2` |
| Inconsistent border radius across components | `§1.4.3` |
| Browser-default bullets, checkboxes, quote marks | `§8.1` |
| No accent color anywhere | `§8.2` |
| Uniform background from top to bottom | `§8.3` |
| Pure black text; pure unsaturated greys | `§5.2.1 §5.5` |
| Everything rendered as its library default | `§8.6` |

### "The important thing doesn't stand out"

| Check | Rule |
|---|---|
| **Are you adding emphasis rather than removing it from competitors?** | `§2.4` |
| Does a supporting region have its own background, making it a peer? | `§2.4.a` |
| Multiple primary-looking actions? | `§2.8` |
| Hierarchy carried by size alone? | `§2.2` |
| Section titles sized from their tag rather than their rank? | `§2.6` |

### "The text is hard to read"

| Check | Rule |
|---|---|
| Measure outside **45–75 characters**? | `§4.3` |
| Line-height wrong for the width — wide text at 1.5? | `§4.5.1` |
| Line-height wrong for the size — large headings at 1.5? | `§4.5.2` |
| Font weight below 400? | `§2.2.b` |
| Contrast below **4.5:1** / **3:1**? | `§5.6` |
| Grey text on a colored background? | `§2.3` |
| Uppercase without added tracking? | `§4.8.2` |
| Centered text over 2–3 lines? | `§4.7.1` |
| A headline face used at small size? | `§4.2.3` |

### "The colors look off / washed out / muddy"

| Check | Rule |
|---|---|
| **Saturation held constant across the ramp?** Ends will look grey | `§5.4` |
| Shades generated with `lighten()`/`darken()`? | `§5.3` |
| Yellow/orange/lime ramps going brown when darkened? | `§5.4.2` |
| Semi-transparent white over a colored surface? | `§2.3.a §6.1.2` |
| Two different grey families in one interface? | `§5.5.1` |
| Colors transcribed from an HSB picker without conversion? | `§5.1.1` |
| Only three greys, forcing improvised intermediates? | `§5.2.1` |

### "The layout feels wrong at some screen sizes"

| Check | Rule |
|---|---|
| Percentage widths on elements that shouldn't scale? | `§3.4.1` |
| An element wider at a smaller breakpoint than a larger one? | `§3.4.2` |
| Everything scaled proportionally instead of large-shrinks-faster? | `§3.5` |
| Mobile derived by collapsing desktop rather than designed? | `§3.3.1` |
| Flex children overflowing — missing `min-w-0`? | `§3.4.1` |
| Overlapping elements colliding at narrow widths? | `§6.5` |

### "Depth looks wrong"

| Check | Rule |
|---|---|
| Any shadow with a horizontal offset or negative Y? | `§6.1.1` |
| Inputs and wells reading as raised rather than inset? | `§6.1.3` |
| Raised elements with large soft shadows instead of tight sharp ones? | `§6.1.2` |
| A crisp contact shadow on a high-elevation element? | `§6.3.1` |
| A blurred shadow in an otherwise flat design? | `§6.4.2` |
| Dark UI relying on shadows, where they're invisible? | `§6.4.1` |

### "Images look bad"

| Check | Rule |
|---|---|
| Text legible over part of the image but not all of it? | `§7.2` |
| Small icons displayed at 3–4× their drawn size? | `§7.3.1` |
| Screenshots shrunk to illegibility? | `§7.3.2` |
| Favicon a shrunken full logo? | `§7.3.3` |
| User uploads at intrinsic aspect ratio? | `§7.4.1` |
| White-background uploads bleeding into the surface? | `§7.4.2` |
| Contrast lowered without brightness compensation? | `§7.2.3` |

---

## Part 3 — Overcorrections

Applying a rule too hard. Each is a real failure produced by a correct rule.

| Overcorrection | From over-applying | Correction |
|---|---|---|
| Everything squeezed into a narrow centered column | `§3.3` don't fill the screen | §3.3.3 — don't force it either. Tables need room |
| Secondary text so faint it's unreadable | `§2.5.3` labels are secondary | §2.5.4 — one step apart on spec content, not three |
| An interface gridded with dark hairlines | `§2.7.2` weight for contrast | Thicken **and keep the soft color**. Darkening was the thing being avoided |
| No borders anywhere, nothing separable | `§8.5` fewer borders | Fewer, not none. `§8.5.1–8.5.3` are alternatives, not prohibitions |
| Every heading tiny | `§2.6` titles are often labels | "Often small," not "always small." Rank drives it |
| Enormous white space on a data-dense tool | `§3.1` start with too much | §3.1.2 — density is legitimate when deliberate |
| Twenty-three color shades | `§5.3.5` trust your eyes | Tweaking existing shades is fine; **adding** is what breaks the system |
| Skipping semantic HTML because the default size is wrong | `§2.6` style independently of tag | Keep the tag, change the styling. `sr-only` if it should be invisible |
| Photorealistic bevels and gradients | `§6.1` emulate a light source | §6.1.4 — don't get carried away |

---

## Part 4 — False positives

Not findings. Reporting these costs credibility.

| Looks like a violation | Why it isn't |
|---|---|
| A dense dashboard | Deliberate density is legitimate — `§3.1.2` |
| `max-w-[70ch]` | Justified arbitrary value; `ch` states the measure rule literally — `§4.3` |
| A serif typeface | A personality decision, not an error — `§1.4.1` |
| No shadows anywhere | Flat design is valid; check depth is carried by color instead — `§6.4` |
| Centered hero headline | Centering is correct for short blocks — `§4.7.1` |
| A visually hidden heading | Correct application of `§2.6` |
| Different widths in one content column | Correct application of `§4.3.1` |
| A large red button in a confirmation dialog | Correct — destructive **is** primary there — `§2.8.1` |
| Asymmetric heading margins (`mt-12 mb-4`) | Correct application of `§3.6.a` |
| Two different background colors and no border | Correct application of `§8.5.2` |

---

## Cross-references

- Severity and reporting procedure → `13-audit-rubric.md`
- Full rule text → the chapter reference for that rule's number
- Utilities for proposed fixes → `10-tailwind-mapping.md`
- Systemic fixes for whole classes of finding → `11-design-tokens.md`
