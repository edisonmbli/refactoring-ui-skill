# Designing Text

> Covers matrix rows **4.1 – 4.8.2** (28 items). Book chapter: *Designing Text*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

Third lens in the sweep. Typography carries more of an interface's perceived quality than any other single system, and it is also where off-system values accumulate fastest — text appears everywhere, so every unsystematic decision gets multiplied.

---

## 4.1 Establish a type scale

**Rule.** Define a fixed set of font sizes in advance and use only those.

**Why.** Two independent costs. Inconsistency: without a system it is normal to find every pixel value between 10px and 24px used *somewhere* in an interface, differences too small to read as intentional and large enough to read as sloppy. And speed: every text element becomes an open-ended decision, repeated hundreds of times.

**How.** Adopt the scale in §4.1.1d, or the project's existing one, and take every font size from it.

**Values.** See §4.1.1d.

**Tailwind.** `text-xs` through `text-9xl` is a type scale. The rule in practice: no `text-[15px]`.

**Fails as.** A stylesheet with 13px, 15px and 17px all present; text that looks inconsistent between components built at different times.

### 4.1.1 Choosing a scale

**Rule.** A linear scale fails here for the same reason it fails for spacing: small jumps matter at the bottom of the scale, not at the top.

**Why.** Identical proportional argument as `03-layout-spacing.md` §3.2.1. The difference between 12px and 14px is significant and worth having; the difference between 46px and 48px is not worth the time it takes to decide.

**How.** Either a modular scale (§4.1.1a) or a hand-picked one (§4.1.1d). The book recommends hand-picked for interface work; the reasoning is in §4.1.1b and §4.1.1c.

**Values.** None.

**Tailwind.** —

**Fails as.** A "type system" that is 2px increments from 10 to 32.

#### 4.1.1a Modular scales

**Rule.** A modular scale multiplies a base size by a fixed ratio, compounding upward.

**Why.** It is mathematically clean and produces harmonically related sizes, which is genuinely attractive for long-form content where few sizes are needed.

**How.** Start from a sensible base (**16px** is standard, being the browser default), apply the ratio to get the next size, apply it again to that result, and so on.

**Values.** Common ratios: **4:5** (a major third), **2:3** (a perfect fifth), **1:1.618** (the golden ratio).

**Tailwind.** Expressible as a custom scale, but see the two objections below before choosing one.

**Fails as.** —

#### 4.1.1b You end up with fractional values

**Rule.** First objection: compounding a ratio produces non-integer pixel sizes.

**Why.** Browsers handle subpixel rounding differently from one another, so fractional sizes can render inconsistently across engines and produce off-by-one differences.

**How.** If you use a modular scale anyway, **round the values yourself** when defining the scale rather than leaving the browser to do it.

**Values.** A 16px base at a 4:5 ratio yields **31.25px, 39.063px, 48.828px** and similar.

**Tailwind.** Define rounded values in the theme, not the raw ratio output.

**Fails as.** Type that shifts by a pixel between Chrome and Safari; scale values with three decimal places checked into a config file.

#### 4.1.1c You usually need more sizes

**Rule.** Second objection, and the more serious one: modular scales are too sparse for interface design.

**Why.** The ratio determines the gaps, and for UI those gaps land wrong. A rounded **3:4** scale gives **12, 16, 21, 28** — and in practice you will want something between 12 and 16, and something between 16 and 21, because UI has more distinct text roles than an article does. The tempting fix is a tighter ratio like **8:9**, but at that point you are selecting a ratio because it happens to emit the sizes you already knew you wanted, which is the hand-picked approach with extra steps.

**How.** For interface design, go to §4.1.1d.

**Values.** 3:4 rounded → **12, 16, 21, 28**. Tighter alternative: **8:9**.

**Tailwind.** —

**Fails as.** A modular scale in the design system plus a growing collection of one-off sizes in the codebase for everything it didn't cover.

#### 4.1.1d Hand-crafted scales

**Rule.** For interface design, pick the sizes by hand.

**Why.** No subpixel rounding to manage, and total control over which sizes exist rather than delegating that to a formula. Constrained enough to speed up decisions, complete enough that no useful size is missing.

**How.** Use the book's scale, or the project's, and stop adding to it.

**Values.** The book's recommended scale, which aligns with the spacing system in `03-layout-spacing.md` §3.2.2:

```
12   14   16   18   20   24   30   36   48   60   72
```

**Tailwind.** Identical to Tailwind's default type scale: `text-xs` (12) · `text-sm` (14) · `text-base` (16) · `text-lg` (18) · `text-xl` (20) · `text-2xl` (24) · `text-3xl` (30) · `text-4xl` (36) · `text-5xl` (48) · `text-6xl` (60) · `text-7xl` (72). Again not a coincidence.

**Fails as.** Re-deriving a scale from scratch when Tailwind already ships this one.

### 4.1.2 Avoid em units

**Rule.** Don't build a type scale in `em`. Use `px` or `rem`.

**Why.** `em` is relative to the current font size, so it compounds through nesting and silently produces computed sizes that are not on your scale. Concretely: an element at **1.25em** renders at **20px**; inside it, `1em` now equals 20px, so a nested element at **.875em** computes to **17.5px** — a value that appears nowhere in the system and that nobody chose. The scale still exists in the config and no longer describes the rendered page.

**How.** Define the scale in `px` or `rem`. Both are absolute with respect to nesting. `rem` additionally respects the user's browser font-size setting, which is the accessibility-preferable default.

**Values.** 1.25em → **20px**; nested .875em → **17.5px**, off-scale.

**Tailwind.** Tailwind's type utilities are `rem`-based, so this is handled by default. The risk enters through custom CSS and component libraries that use `em`.

**Fails as.** Nested cards or list items whose text is subtly the wrong size; typography that drifts as component nesting deepens.

> **Note (line length uses em deliberately).** §4.3 specifies measure in `em`, and that is correct — there you *want* the width to track the font size, because measure is a character-count constraint. The prohibition is on `em` for font sizes, where compounding is the problem.

---

## 4.2 Use good fonts

**Rule.** Developing real typographic judgment takes years. Until then, use selection heuristics.

**Why.** The quality signals in a typeface are numerous and subtle, and evaluating them directly is a skill with a long ramp. The heuristics below are proxies — they don't teach you to see quality, but they reliably narrow thousands of options to a few dozen good ones, which is enough to ship.

**How.** Apply §4.2.1 through §4.2.5 as filters.

**Values.** None.

**Tailwind.** Font families belong in the theme (`--font-sans` in v4, `theme.fontFamily` in v3), defined once.

**Fails as.** A typeface chosen because its name looked appealing in a dropdown.

### 4.2.1 Play it safe

**Rule.** For UI, a fairly neutral sans-serif is the safe default.

**Why.** Neutral faces don't compete with content and are legible across the wide size range an interface demands. If you don't trust your taste, the system font stack is safer still — users are already accustomed to it, it needs no download, and it matches the host platform.

**How.** Something Helvetica-like, or the system stack.

**Values.** The book's system stack:

```
-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue
```

**Tailwind.** Close to Tailwind's default `font-sans`. Use it as-is unless there's a reason not to.

**Fails as.** A display or condensed face used for body text and controls.

### 4.2.2 Ignore typefaces with less than five weights

**Rule.** Filter to families with many weights.

**Why.** Not universally true, but a strong proxy: a family drawn in many weights represents far more work, and that investment usually shows in the details. It is also directly practical — §2.2.b needs at least two well-drawn weights, and the hierarchy levers get thin without them.

**How.** Most font directories filter by number of styles. Set the threshold to **10+** to account for italics.

**Values.** **≥5 weights**, i.e. **10+ styles** with italics. On Google Fonts this removes about **85%** of the library, leaving **fewer than 50** sans-serifs.

**Tailwind.** Load only the weights actually in use — two, per §2.2.b.

**Fails as.** A family with regular and bold only, forcing synthetic weights or a second typeface.

### 4.2.3 Optimize for legibility

**Rule.** Typefaces are drawn for a purpose. Match the purpose to the use.

**Why.** The design differences are systematic, not incidental. Faces intended for headlines have **tighter letter-spacing and shorter x-heights** — economical and striking at large sizes. Faces intended for small sizes have **wider letter-spacing and taller x-heights** — more open, more distinguishable per glyph. A headline face used for UI body text is small, tight and cramped exactly where legibility matters most.

**How.** Avoid condensed faces and short x-heights for main UI text. Judge by looking at lowercase letters at your actual body size, not at a large specimen.

**Values.** None.

**Tailwind.** —

**Fails as.** A brand typeface pushed from the logo into the interface, producing body text that is technically on-brand and hard to read.

### 4.2.4 Trust the wisdom of the crowd

**Rule.** Popular fonts are usually good fonts. Sort by popularity.

**Why.** Popularity aggregates the judgment of many people who *do* have typographic training. It's an inherited-taste shortcut, and it's especially useful outside the neutral-sans category — choosing a serif with personality is a genuinely hard call where the aggregate is a strong prior.

**How.** Sort by popularity in the directory and choose from the top.

**Values.** None.

**Tailwind.** —

**Fails as.** Hours lost scrolling a font directory; an obscure choice with poor hinting or an incomplete character set.

### 4.2.5 Steal from people who care

**Rule.** Inspect the typefaces used by sites you admire.

**Why.** Strong design teams hold strong typographic opinions and will have chosen faces the safe heuristics would never surface. Borrowing their conclusions is free.

**How.** Devtools on the sites you like; note the family and how it's used.

**Values.** None.

**Tailwind.** —

**Fails as.** —

### 4.2.6 Developing your intuition

**Rule.** These heuristics are scaffolding. Attention builds the real skill.

**Why.** Once you start looking closely at typography on well-designed sites, the ability to judge a face arrives faster than expected — the heuristics are for the interim.

**How.** Keep noticing.

**Values.** None.

**Tailwind.** —

**Fails as.** —

---

## 4.3 Keep your line length in check

**Rule.** Set paragraph width for reading, not to fit the layout. **45–75 characters per line.**

**Why.** Line length governs the return sweep — the eye's jump from the end of one line to the start of the next. Long lines make that jump long and error-prone, and re-reading or skipping a line is the result. Too short is also bad: the sweep happens so often it becomes the dominant motion. The 45–75 band is where neither problem dominates.

The common failure is not deciding at all: the paragraph inherits the container's width, which was set for something else entirely.

**How.** Constrain the paragraph's width directly. `em` is the practical unit here because it tracks font size, and measure is fundamentally about characters, not pixels.

**Values.** **45–75 characters**, i.e. **20–35em**. Somewhat over 75 can work but is explicitly risky territory; **stay in 45–75** to be safe.

**Tailwind.** `max-w-prose` is ~65 characters and lands in the band. `max-w-2xl` on a text block is a good approximation. The `ch` unit is also available: `max-w-[70ch]` — one of the few arbitrary values that is justified, since it expresses the rule directly.

**Fails as.** Blog posts and documentation running the full browser width; marketing copy at 120 characters per line; readers reporting they lose their place.

### 4.3.1 Dealing with wider content

**Rule.** When paragraphs share a content area with images or wide components, constrain the paragraphs anyway.

**Why.** The instinct is that everything in one column should share one width — mixed widths feel inconsistent. But measure is a reading constraint and image width is a presentation constraint; they are unrelated, and the visual result of honoring both is consistently more polished than the result of forcing them to match.

**How.** Let the content area be as wide as its widest element needs. Give the paragraphs their own narrower max-width inside it.

**Values.** Same **45–75 characters** for the text.

**Tailwind.** A `max-w-5xl` article container with `<p class="max-w-prose">` inside it; figures and code blocks use the full width.

**Fails as.** Documentation where prose is as wide as the code samples; case studies whose text stretches to match a hero image.

---

## 4.4 Baseline, not center

**Rule.** When different font sizes sit on the same line, align them by baseline, not by vertical center.

**Why.** The baseline is the line letters rest on, and the eye already uses it as the alignment reference for all reading — it is perceived whether or not it is drawn. Centering two different sizes offsets their baselines, so the text is aligned by a reference the reader isn't using while being misaligned on the one they are. Centered mixed sizes therefore look subtly wrong without an identifiable cause.

The error scales with proximity: with a lot of space between the two pieces of text it may not catch your eye, but when they're close together the misalignment becomes obvious.

**How.** Align on the baseline. In a flex row, that's an explicit alignment value rather than the default.

**Values.** None.

**Tailwind.** `flex items-baseline` instead of `items-center` whenever the row mixes sizes — a card title beside smaller actions, a large number beside its unit, a heading beside a timestamp. `items-center` remains right when sizes match, or when aligning to non-text elements like avatars and icons.

**Fails as.** Card headers where the title and its actions look slightly off; a large metric with a small unit label that never quite sits right.

---

## 4.5 Line-height is proportional

**Rule.** The "1.5 is a good line-height" advice is a starting point, not a constant. Line-height depends on both line length and font size.

**Why.** Line spacing exists to make the return sweep reliable — its correct value is therefore a function of how difficult that sweep is, and difficulty varies. One value applied everywhere is right in one context and wrong in the others.

**How.** Combine §4.5.1 and §4.5.2 — the two factors act simultaneously, occasionally in opposite directions.

**Values.** ~**1.5** is the starting point, not the answer.

**Tailwind.** `leading-*` utilities, chosen per context rather than set once globally.

**Fails as.** A global `line-height: 1.5` applied to headlines and captions alike.

### 4.5.1 Accounting for line length

**Rule.** Line-height and line length are **proportional**. Wider text needs taller line-height.

**Why.** The longer the line, the further the eye travels horizontally on the return sweep, and the easier it is to land on the wrong line. More vertical separation makes the target line easier to identify. If you have ever re-read a line or skipped one, the line-height was too short for the measure.

**How.** Narrow columns take a shorter line-height; wide ones need more. If the text is wide enough to need a line-height near 2, consider whether §4.3 should have constrained it instead.

**Values.** Narrow content ≈ **1.5**; wide content up to **2**.

**Tailwind.** `leading-normal` (1.5) for constrained measures; `leading-loose` (2) for wide ones.

**Fails as.** Full-width text at 1.5 that is measurably hard to read; documentation where readers repeatedly lose their place.

### 4.5.2 Accounting for font size

**Rule.** Line-height and font size are **inversely** proportional. Larger text needs *less* relative line spacing.

**Why.** At small sizes the eye needs help finding the next line, so extra leading matters. As text grows, the lines themselves become easy to distinguish and the help stops being necessary. Past a certain size, proportional leading is actively harmful — a headline at 1.5 breaks into disconnected lines rather than reading as one unit.

**How.** Reduce line-height as size increases. Large headlines can go to **1** with no loss.

**Values.** Large headline text: line-height of **1** is fine.

**Tailwind.** `text-5xl leading-none` or `leading-tight` on display headings; `text-sm leading-relaxed` on small text. Note this is one of the details §9.1.2 predicts you'll discover by rebuilding interfaces — tightened heading line-height is a top offender.

**Fails as.** Multi-line hero headlines that look airy and disconnected; small print at `leading-tight` that reads as a solid block.

---

## 4.6 Not every link needs a color

**Rule.** Link styling designed to make a link stand out in prose is overbearing in link-dense interfaces.

**Why.** In a paragraph of non-link text, a link is an exception and needs to announce itself. In a UI where most things are links, that treatment inverts: what was a distinguishing signal becomes the default state, the page turns into a field of colored text, and no link stands out from any other. The treatment's value came from its rarity.

**How.** Scale emphasis with the link's actual importance:
- **In prose** — a clear treatment. The link is genuinely exceptional.
- **In link-dense UI** — subtler: a heavier font weight or a darker color, no link color.
- **Ancillary links** — no default emphasis at all. Add an underline or color change **only on hover**. Anyone who tries will find them; they don't compete with the primary path.

**Values.** None.

**Tailwind.** Prose: `text-{primary}-600 underline`. Dense UI: `font-medium text-{neutral}-900`. Ancillary: `text-{neutral}-600 hover:underline`.

**Fails as.** Navigation and tables where every cell is blue; a page where the important action is indistinguishable from a dozen incidental links.

---

## 4.7 Align with readability in mind

**Rule.** Text aligns to the direction of its language. For English and most languages, that means left-aligned by default.

**Why.** A consistent left edge gives the eye a fixed return target on every sweep. Other alignments move that target, which is affordable for a couple of lines and expensive beyond that.

**How.** Left-align by default; use other alignments only in the specific cases below.

**Values.** None.

**Tailwind.** `text-left` is the default; `text-center`, `text-right` and `text-justify` are the exceptions and each needs a reason.

**Fails as.** Centered paragraph text; right-aligned form labels making the label-to-input distance vary per row.

### 4.7.1 Don't center long form text

**Rule.** Centering suits headlines and short independent blocks. Past two or three lines, left-align.

**Why.** Centered text has a ragged left edge, so the return target moves on every line and the eye must locate it each time. With two or three lines the cost is trivial and the symmetry is worth it; beyond that it compounds.

**How.** If a centered block runs long, the best fix is usually to **rewrite it shorter** rather than switch it to left-aligned — this preserves the centered composition and improves the copy. When one of several centered blocks is too long, shortening it also makes the set feel more consistent.

**Values.** **Two to three lines** is the limit for centered text.

**Tailwind.** `text-center` on a hero headline and subhead; `text-left` once the body begins. Watch for `text-center` on a section container leaking into everything inside it.

**Fails as.** Centered marketing paragraphs running five or six lines; a feature grid where each card's centered description wraps to four ragged lines.

### 4.7.2 Right-align numbers

**Rule.** Numbers in a table are right-aligned.

**Why.** Right alignment puts the decimal point — and every digit place — in a consistent column, so magnitude is readable from digit count alone and values can be compared without reading them. Left-aligned numbers scatter the decimal across the column and force digit-by-digit comparison.

**How.** Right-align numeric columns. Tabular figures help further where the typeface offers them, keeping digit widths equal.

**Values.** None.

**Tailwind.** `text-right` on numeric `<td>` and its `<th>`. Add `tabular-nums` for fixed-width digits.

**Fails as.** Financial tables where spotting the largest value requires reading every row; totals that don't line up with the column above them.

### 4.7.3 Hyphenate justified text

**Rule.** If you justify text, enable hyphenation at the same time.

**Why.** Justification works by stretching the spaces between words to force both edges flush. Without hyphenation the renderer can only stretch spaces, so lines with few long words develop large, uneven gaps — visible rivers of white space through the paragraph. Hyphenation gives the renderer somewhere else to take up slack.

**How.** Set both properties together, always. Justification is worth it mainly when mimicking print — a magazine or newspaper look. Left-aligned works well in those contexts too, so this is largely preference.

**Values.** None.

**Tailwind.** `text-justify hyphens-auto` — never `text-justify` alone. `hyphens-auto` needs a `lang` attribute on the document to apply the right dictionary.

**Fails as.** Justified paragraphs with visible white rivers; a single short word stretched across an entire line.

---

## 4.8 Use letter-spacing effectively

**Rule.** Default to leaving letter-spacing alone. Two situations justify changing it.

**Why.** The type designer set the spacing deliberately, for the sizes and purpose the family was drawn for, and they had far more information about the letterforms than you do. Adjusting it is a correction for using a face outside its intended context — which means the two valid cases are exactly the two context mismatches below.

**How.** §4.8.1 and §4.8.2 only.

**Values.** None.

**Tailwind.** `tracking-*` utilities, used sparingly.

**Fails as.** Letter-spacing tweaked by feel across an interface; body text with added tracking "for elegance."

### 4.8.1 Tightening headlines

**Rule.** When using a text-optimized family for headlines, reduce its letter-spacing.

**Why.** This is the §4.2.3 distinction seen from the other side. A family like **Open Sans** is drawn for legibility at small sizes, so its built-in letter-spacing is wider than a headline family like **Oswald**. At large sizes that generous spacing reads as loose and slightly unfinished. Tightening it approximates the condensed look of a purpose-built headline face.

The reverse does not work: headline faces rarely function at small sizes even with letter-spacing added, because the problem there is x-height and stroke contrast, which spacing cannot fix.

**How.** Apply a negative tracking value to large headings only. Leave body text alone.

**Values.** Book's examples: **Open Sans** (text-optimized, wider spacing) vs **Oswald** (headline-optimized, tighter). Tighten headlines; **never loosen a headline face to make it work small**.

**Tailwind.** `text-5xl tracking-tight` on display headings. `tracking-tighter` for very large sizes.

**Fails as.** Large headings that look loose and slightly amateur; a condensed headline face used at 14px with added tracking to compensate.

### 4.8.2 Improving all-caps legibility

**Rule.** Increase letter-spacing on all-caps text.

**Why.** Default letter-spacing is optimized for sentence case — one capital followed by mostly lowercase. Lowercase carries a lot of visual variety: letters like **n, v, e** sit entirely within the x-height, letters like **y, g, p** have descenders below the baseline, and letters like **b, f, t** have ascenders above it. Word shape comes from that variety and the eye reads it directly.

All-caps discards it. Every letter is the same height, word shape disappears, and the letters must be distinguished individually — a task the default tight spacing makes harder. Extra tracking restores separation between glyphs.

**How.** Whenever text is uppercased, add letter-spacing. Treat it as part of the uppercase treatment, not an optional refinement.

**Values.** None numerically, but it is not optional.

**Tailwind.** `uppercase tracking-wide` — the two utilities travel together. Common on small labels, table headers and eyebrow text, which is also where §2.5.3 usually applies, so these often combine: `text-xs uppercase tracking-wide text-{neutral}-500`.

**Fails as.** Uppercase section labels and table headers that are hard to scan; a logotype set in caps at default spacing.

---

## Audit checklist for this lens

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

## Cross-references

- Font weights and text colors as hierarchy levers → `02-hierarchy.md` §2.2
- Why section headings are often small → `02-hierarchy.md` §2.6
- The 25% adjacency logic shared with spacing → `03-layout-spacing.md` §3.2.1
- Responsive type sizing, which does not scale proportionally → `03-layout-spacing.md` §3.5
- Emitting the type scale as tokens → `11-design-tokens.md`
