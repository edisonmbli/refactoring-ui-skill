# Hierarchy

> Covers matrix rows **2.1 – 2.8.1** (20 items). Book chapter: *Hierarchy is Everything*.
> Every rule below follows the same six-part shape: **Rule · Why · How · Values · Tailwind · Fails as**.
> "Fails as" is what the violation looks like in the wild — use it to diagnose from a symptom.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps — resolve them from the project's tokens, never emit a brace or a literal Tailwind default palette name. Full convention in `SKILL.md` → *Reading the reference files*.

Hierarchy is the first lens in the audit sweep. Findings here outrank every other lens, because a hierarchy problem changes what counts as a problem everywhere else: content that is fighting for attention will read as a spacing problem, a color problem and a border problem simultaneously, and none of those fixes will work.

---

## 2.1 Not all elements are equal

**Rule.** Visual hierarchy — how important each element *appears* relative to the others — is the primary mechanism by which an interface reads as "designed." Establish it before touching anything decorative.

**Why.** The intuition that design quality comes from styling is wrong, and it is the reason non-designers feel blocked: styling seems to require talent they don't have. But the dominant variable is relational, not aesthetic. Take an interface where everything competes for attention and deliberately push secondary and tertiary content back, and the result improves immediately — with the color scheme, typeface and layout completely unchanged. That is the proof that the effect is structural.

**How.**
1. Enumerate what's on the surface and sort into three tiers: what the user came for, what supports it, what merely needs to exist.
2. Give tier 1 whatever emphasis it needs — usually less than you'd expect, once tiers 2 and 3 are properly suppressed.
3. Push tiers 2 and 3 back using the levers in §2.2 (size, weight, color) before adding anything.
4. Only then apply color, depth and polish.

If you cannot name the single most important element on a screen, the design has no hierarchy yet and no amount of styling will supply one.

**Values.** **Three tiers** is the working maximum — beyond three the distinctions stop being perceptible.

**Tailwind.** Not a utility-level rule — it's the ranking decision that determines which utilities you then reach for.

**Fails as.** A screen where everything is the same size, the same weight and the same color; described as "busy," "noisy," "flat," "like a wall of text," or "it has all the right content but looks unfinished."

---

## 2.2 Size isn't everything

**Rule.** Don't make font size carry the hierarchy by itself. Use weight and color to do the same work.

**Why.** Size is one-dimensional and runs out fast. If size is the only lever, emphasis forces primary content to grow until it's disproportionate, and de-emphasis forces secondary content to shrink until it's genuinely hard to read. Weight and color express importance without either cost — and a heavier weight often communicates importance *better* than a larger size, because it reads as intent rather than as scale.

**How.**
- To emphasize: increase weight first, then size. A bolder primary element lets you keep the font size reasonable.
- To de-emphasize: soften the color first, then reduce the size. A softer color loses far less readability than a smaller size does.
- Reach for size last, not first.

**Values.** See 2.2.a and 2.2.b for the two constrained sets.

**Tailwind.** `font-semibold` / `font-bold` before `text-2xl`; `text-{neutral}-500` before `text-xs`.

**Fails as.** Headlines that feel oversized for their container; captions, metadata and helper text at 11–12px that require leaning toward the screen; a design where zooming out makes everything look better.

### 2.2.a Three text colors

**Rule.** Use two or three text colors, not more.

**Why.** Color-based hierarchy only works if the steps are distinguishable at a glance. Four or five greys produce differences the eye resolves as inconsistency rather than as ranking.

**How.** Assign by tier and stay assigned:
- **Dark** — primary content (an article's headline, a card's title, a data value).
- **Grey** — secondary content (a publication date, a byline, a label).
- **Lighter grey** — tertiary content (a footer copyright, a timestamp, a disclaimer).

**Values.** **3 text colors maximum.** Which stops on the ramp is project-dependent — commonly the 900/500/400 region against a light background, but that follows from the ramp built in `05-color.md`, not from this rule.

**Tailwind.** `text-{neutral}-900` / `text-{neutral}-500` / `text-{neutral}-400`. Semantic aliases are better: `text-primary` / `text-secondary` / `text-muted` mapped once in the theme.

**Fails as.** Five or six distinct greys across one page, usually because each was picked in isolation for its own component; reads as sloppiness, not as hierarchy.

### 2.2.b Two font weights

**Rule.** Two weights are enough for UI work: a normal weight and a heavier one. Never use a weight below 400 for interface text.

**Why.** Weight has the same distinguishability constraint as color. And weights under 400 are actively harmful at UI sizes — thin strokes lose definition on small text and become a legibility problem rather than a hierarchy tool.

**How.** Pick one normal weight and one emphasis weight and use only those. If you're tempted to de-emphasize with a lighter weight, use a lighter color or a smaller size instead — that's what those levers are for.

**Values.**
- Normal: **400 or 500** — which of the two is project-dependent, following the typeface's optical weight.
- Emphasis: **600 or 700**.
- **Never below 400** in UI text. Large display headings are the only exception.
- **Two weights total.**

**Tailwind.** `font-normal` (400) or `font-medium` (500) as the base; `font-semibold` (600) or `font-bold` (700) for emphasis. `font-light` (300) and `font-thin` (100) should not appear in interface text.

**Fails as.** Light-weight body text that looks elegant in a mockup and washes out on a real display; or four or five weights in one interface, where the 500/600 distinction is invisible and only adds font payload.

---

## 2.3 Don't use grey text on colored backgrounds

**Rule.** Lightening text to grey de-emphasizes it on white, but not on a colored background. Hand-pick a new color derived from the background instead.

**Why.** This is the most commonly misdiagnosed rule in the chapter. What makes grey-on-white work is not that the text is *grey* — it's that the text moved **closer to the background color**, reducing contrast. On white, "closer to the background" and "greyer" happen to be the same direction, which hides the real mechanism. On a blue background, grey moves *away* from the background in hue while reducing contrast unevenly, and the text reads as dirty rather than as secondary.

**How.**
1. Take the background color's hue.
2. Keep that hue fixed.
3. Adjust saturation and lightness until the text sits at the contrast you want.

The result is a color in the same family as the background — a desaturated, lighter or darker relative of it — which is why it reads as intentional.

**Values.** Same hue as the background; saturation and lightness tuned by eye. HSL makes this tractable, which is one of the reasons `05-color.md` insists on it: same `H`, different `S`/`L`.

**Tailwind.** Extend the theme with the derived value rather than reaching for a grey utility. On a `bg-{primary}-700` panel, secondary text wants something like `text-{primary}-200`, not `text-{neutral}-400` — a same-family shade from the ramp you already built.

**Fails as.** Secondary text on a colored card, banner or sidebar that looks muddy, dirty or "wrong" without an obvious cause; a colored panel where the supporting copy seems to belong to a different design.

### 2.3.a Why not white at reduced opacity

**Rule.** Don't produce the softer color by lowering the opacity of white.

**Why.** Two separate failures. First, semi-transparent white *does* reduce contrast, but it also drains saturation from the underlying color, so the text reads as dull, washed out, or disabled — it looks broken rather than secondary. Second, and worse, the background shows *through* the text. Over a flat color that's merely dull; over an image or a pattern, the pattern is visible inside the letterforms and legibility collapses.

**How.** Hand-pick an opaque color, as in §2.3. This is worth the extra step precisely because it survives being placed over anything.

**Values.** Opacity on text: avoid. Opacity on overlays and scrims: fine — that's a different job (see `07-images.md`).

**Tailwind.** Prefer `text-{primary}-200` over `text-white/60`. The opacity modifier is right for overlays and dividers, not for text hierarchy.

**Fails as.** Text on a hero image that becomes unreadable exactly where the image is busiest; secondary text on a colored button that looks like the button is disabled.

---

## 2.4 Emphasize by de-emphasizing

**Rule.** When the element you want to highlight refuses to stand out, stop adding emphasis to it and remove emphasis from its competitors.

**Why.** Emphasis is relative, not absolute. There is no property you can add to an element that makes it prominent in isolation — prominence is a ratio against its surroundings. When you've already given an element a distinct color and it still doesn't read as active, you've hit the ceiling of what addition can do, and every further addition makes the interface louder without making it clearer.

**How.**
1. Notice that you're stacking treatments on one element with diminishing returns — that's the signal.
2. Identify what it's competing with.
3. Soften those: lower their contrast, reduce their weight, mute their color.
4. Re-check. The target usually now stands out without any change to itself at all.

**Values.** None — this is a direction of attack, not a measurement.

**Tailwind.** Instead of piling `font-bold text-{primary}-600 bg-{primary}-50 border-l-4` onto the active nav item, move the inactive items from `text-{neutral}-700` to `text-{neutral}-400` and leave the active one alone.

**Fails as.** An active navigation state that doesn't feel active despite carrying three or four distinguishing treatments; a "call to action" that keeps growing louder in successive revisions while the page gets noisier and the CTA no clearer.

### 2.4.a The same move at section scale

**Rule.** Apply the technique to whole regions, not only to individual elements.

**Why.** Regions compete for attention exactly like elements do, and a region's competitive weight is dominated by its background treatment. A sidebar with its own background color reads as a peer of the main content; it will fight the content no matter how the content is styled internally.

**How.** When a supporting region competes with the primary one, remove *its* distinguishing treatment — drop the background color and let it sit directly on the page background — rather than escalating the primary region.

**Values.** None.

**Tailwind.** Remove `bg-{neutral}-100` from the sidebar container rather than adding `shadow-lg` and a heavier background to the content area.

**Fails as.** A layout where the eye lands on the sidebar first; a dashboard where filter panels and navigation feel as important as the data.

---

## 2.5 Labels are a last resort

**Rule.** When presenting data, don't default to the `label: value` format. Try to eliminate the label first.

*(This is about displaying data, not about form inputs. Form fields need accessible labels — that requirement is untouched.)*

**Why.** `label: value` grants both halves the same visual weight, and it does so uniformly across every row. That mechanically forbids hierarchy — you cannot emphasize what matters when the format guarantees each datum is presented identically to its neighbors. The label is usually the less interesting half, so the format spends half of every row's attention budget on the wrong thing.

**How.** In order of preference: drop the label (§2.5.1) → fold it into the value (§2.5.2) → keep it but demote it (§2.5.3). Invert only in the specific case in §2.5.4.

**Values.** None.

**Tailwind.** —

**Fails as.** Profile pages, detail views and card bodies that read as a database dump; a list of rows where nothing draws the eye and the user has to read all of it to find anything.

### 2.5.1 You might not need a label at all

**Rule.** When the format or the context already identifies the data, drop the label.

**Why.** Users decode data types from shape without conscious effort. `janedoe@example.com` is self-evidently an email address; `(555) 765-4321` is a phone number; `$19.99` is a price. Labeling these adds words that carry no information while consuming hierarchy.

Context does the same work when format doesn't. "Customer Support" listed beneath a person's name in an employee directory needs no "Department:" prefix — the position and the surrounding content make the relationship unambiguous.

**How.** For each label, ask whether removing it would create real ambiguity for someone who understands the page. If not, remove it, and spend the recovered space and attention on styling the value.

**Values.** None.

**Tailwind.** —

**Fails as.** "Email: jane@example.com", "Phone: (555) 765-4321", "Price: $19.99" — three labels that tell the reader nothing they didn't already know.

### 2.5.2 Combine labels and values

**Rule.** When a value isn't fully clear alone, add the clarifying word *into* the value rather than putting it in a separate label.

**Why.** A label and its value are one unit of meaning; splitting them across two styled elements forces you to style two things and makes both harder to rank. Merged into a single phrase, the whole unit takes one styling decision, and the number — the part that matters — can be emphasized within it.

**How.** Rewrite as a phrase.
- "In stock: 12" → **"12 left in stock"**
- "Bedrooms: 3" → **"3 bedrooms"**

The clarifying word can then be styled down within the phrase while the figure stays prominent.

**Values.** None.

**Tailwind.** `<span class="font-semibold text-{neutral}-900">12</span> <span class="text-{neutral}-500">left in stock</span>` — one line, two ranks.

**Fails as.** Spec lists and product cards where every row is a colon; e-commerce inventory and property listings that read like form output.

### 2.5.3 Labels are secondary

**Rule.** When you genuinely need a label, style it as supporting content. The data is what matters.

**Why.** Labels are needed when several similar values must be told apart at a glance — a dashboard of metrics, a stat row. But "needed for disambiguation" is a much smaller role than "equal partner," and styling it as an equal partner puts the reader's attention on the word rather than the number they came for.

**How.** Demote the label by any combination of: smaller size, lower contrast, lighter weight. The value keeps the dark color and the heavier weight.

**Values.** All three levers may be used together; that combination is explicitly endorsed here.

**Tailwind.**
```html
<div>
  <div class="text-sm text-{neutral}-500">Monthly revenue</div>
  <div class="text-3xl font-semibold text-{neutral}-900">$48,200</div>
</div>
```

**Fails as.** Dashboards where the metric names are as prominent as the metrics; KPI cards you have to read twice to extract the numbers from.

### 2.5.4 When to emphasize a label

**Rule.** Invert the relationship when the user is scanning *for the label* rather than for the value.

**Why.** Hierarchy should match the search task. On an information-dense specification page, someone checking a phone's dimensions is scanning for the word "depth," not for "7.6mm" — they don't know the value yet, so the value is not a findable target. Here the label is the navigational element and the value is the payload.

**How.** Give the label a darker color and the value a slightly lighter one. Keep the gap small — the value is still important information and must not be pushed into the background the way a label is in §2.5.3.

**Values.** Project-dependent, but the spread is the point: a darker label and a *slightly* lighter value is usually the whole adjustment. Don't reuse the full contrast spread from §2.5.3, inverted.

**Tailwind.** `text-{neutral}-900` on the label, `text-{neutral}-600` on the value — one step apart, not three.

**Fails as.** Technical spec tables where finding a given property means reading every row; or the over-correction, where values are so faint the table becomes useless once the row is found.

---

## 2.6 Separate visual hierarchy from document hierarchy

**Rule.** Choose elements for their semantics and style them for the visual hierarchy you actually need. The two decisions are unrelated.

**Why.** Browsers give heading elements progressively smaller default sizes, which trains an expectation that `h1` means "big." That default is reasonable for documents — articles, documentation — where the heading structure *is* the visual structure. In application UI it misleads. A page titled *Manage Account* is correctly marked up as `h1`, but the title is not what the user came for; the account controls are. Sizing it to match the tag's default steals attention from the content it introduces.

Most section titles in an application behave as **labels**, not as headings: they exist to tell you what a region contains, and the region's content should dominate. That means section titles are frequently small.

**How.**
1. Pick the tag from the document outline — real, correct semantics.
2. Pick the styling from the visual rank — independently.
3. Where content is self-explanatory, a title may be present in the markup for screen readers and **visually hidden entirely**.

Keeping semantics correct is not optional; this rule decouples styling from it, it does not license skipping it.

**Values.** None. Section titles at `text-sm` or `text-base` are common and correct.

**Tailwind.** `<h1 class="text-base font-semibold text-{neutral}-900">` is a perfectly good page title. For the hidden case use `sr-only`, which keeps the element in the accessibility tree while removing it visually.

**Fails as.** A settings page whose word "Settings" is the largest thing on screen; an application that reads like a document; or the inverse failure — `<div>` used for a heading because a real heading "would look too big," which breaks the accessibility tree to solve a styling problem.

---

## 2.7 Balance weight and contrast

**Rule.** Emphasis tracks **surface area**. Understanding that lets you rebalance elements whose weight you can't change.

**Why.** Bold text feels emphasized because within the same space, more pixels belong to the glyphs and fewer to the background. That's the whole mechanism — and it generalizes past text. Anything that covers more surface area within its footprint reads as heavier, whether or not it has a "weight" property. Once you see emphasis as an area effect, contrast becomes the counterweight you can always reach for.

**How.** Two symmetrical moves, §2.7.1 and §2.7.2.

**Values.** None.

**Tailwind.** —

**Fails as.** Elements that feel mismatched in prominence with no obvious cause, typically icon-plus-text pairs and border-heavy layouts.

### 2.7.1 Using contrast to compensate for weight

**Rule.** Icons — solid ones especially — are heavy. Lower their contrast to balance them against adjacent text.

**Why.** An icon covers far more of its box than a letterform covers of its own, so an icon set in the same color as neighboring text will dominate that text. And unlike text, an icon has no weight axis to turn down. Contrast is the only available lever, and it works because it directly counteracts the area effect: fewer effective "on" pixels, perceptually.

**How.** Give the icon a softer color than the text it accompanies. Outline icons need less correction than solid ones, since they already cover less area.

**Values.** Project-dependent — typically one to two stops down the neutral ramp from the text color. The invariant is the direction (softer), not the distance.

**Tailwind.** `<span class="text-{neutral}-900">Archived</span>` paired with `<Icon class="text-{neutral}-400" />`. Watch for `currentColor` icon components, which inherit the text color and silently reintroduce the imbalance.

**Fails as.** Menu and list rows where the icons are the first thing you see and the labels the second; icon-and-label pairs that feel unbalanced without an obvious reason.

### 2.7.2 Using weight to compensate for contrast

**Rule.** The reverse move: when a low-contrast element is too faint, add weight instead of adding contrast.

**Why.** The area relationship runs both ways. A 1px border in a soft color often disappears; darkening it to compensate makes the whole design feel harsh and noisy, because a dark hairline is a high-contrast edge and the eye reads hard edges as loud. Thickening the border raises its surface area — and therefore its presence — while keeping the soft color that made the design feel calm.

**How.** Increase the border width and keep the soft color. Same logic applies to any element too subtle to register: make it bigger before you make it darker.

**Values.** **1px → 2px** is usually the whole fix.

**Tailwind.** `border-2 border-{neutral}-200` rather than `border border-{neutral}-400`.

**Fails as.** Dividers and section rules that vanish; or the over-correction, an interface gridded with dark hairlines that feels harsh and cluttered.

---

## 2.8 Semantics are secondary

**Rule.** Don't style actions purely by what they mean. Style them by where they sit in the page's importance pyramid.

**Why.** Semantic styling — save is green, delete is red, cancel is grey — assigns visual weight by category rather than by importance, so a rarely-used destructive action can end up as prominent as the page's main action. Every page has an action hierarchy: normally **one true primary action**, a couple of secondary actions, and a few tertiary ones. Communicating that hierarchy is what makes a page's action area legible; semantics ride on top of it, they don't replace it.

**How.**
1. List every action on the page.
2. Identify the single primary action. If you find two, one of them probably isn't.
3. Sort the rest into secondary and tertiary.
4. Apply the treatments in 2.8.a, then layer semantic color within them.

**Values.** **One primary action per page**; a couple of secondary; a few tertiary.

**Tailwind.** See 2.8.a.

**Fails as.** Toolbars and page headers with four or five solid, equally-weighted buttons; a form whose Cancel button is as visually loud as its Submit.

### 2.8.a The three treatments

**Rule.** Each rank has a treatment.

**Why.** The ranks must be *discriminable*, which means the steps between them should differ in kind, not merely in shade. Fill → outline → link is a difference in kind; three fills at three saturations is not.

**How.**
- **Primary — obvious.** Solid, high-contrast background color.
- **Secondary — clear but not prominent.** An outline style, or a low-contrast background color.
- **Tertiary — discoverable but unobtrusive.** Styled as a link.

**Values.** **Three ranks.** A fourth is almost always two ranks that should be merged.

**Tailwind.**
```html
<button class="bg-{primary}-600 text-white ...">Save changes</button>
<button class="border border-{neutral}-300 text-{neutral}-700 ...">Preview</button>
<button class="text-{neutral}-600 hover:underline ...">Cancel</button>
```

**Fails as.** Every action rendered as a filled button; or three ranks distinguished only by fill color, where the difference between secondary and tertiary is invisible at a glance.

### 2.8.1 Destructive actions

**Rule.** Severity is not prominence. A destructive action gets the treatment its *rank* calls for, not the treatment its danger suggests.

**Why.** "Dangerous, therefore big and red" inverts the goal. Making a rarely-used destructive action the loudest thing on screen both wrecks the page's hierarchy and draws the eye toward the action you'd least like clicked by accident. The correct place for emphatic destructive styling is the confirmation step — where destroying the thing genuinely *is* the primary action, and where the loud treatment then reinforces rather than distorts the hierarchy.

**How.**
1. Rank the destructive action honestly. On most pages it is secondary or tertiary — style it accordingly.
2. Put the emphatic red primary treatment inside the confirmation dialog.

This gives the pattern two properties at once: the page stays calm, and the moment of real consequence gets full weight.

**Values.** None.

**Tailwind.** On the page: `text-{danger}-600 hover:underline` (tertiary) or `border border-{danger}-300 text-{danger}-700` (secondary). In the confirmation dialog: `bg-{danger}-600 text-white`.

**Fails as.** A settings page dominated by a large red Delete Account button; destructive-red used as an attention-getter for actions that aren't destructive at all.

---

## Audit checklist for this lens

Run in this order when sweeping. Each item cites the rule to reference in a finding.

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

## Cross-references

- Grey ramps, colo{danger}-background text derivation, and contrast targets → `05-color.md`
- Group spacing, which frequently reads as a hierarchy problem → `03-layout-spacing.md` §3.6
- Type scale and the sizes referenced here → `04-typography.md` §4.1
- Button, card and stat-block specifications → `12-component-recipes.md`
