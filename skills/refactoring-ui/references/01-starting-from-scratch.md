# Starting from Scratch

> Covers matrix rows **1.1 – 1.5.3** (17 items). Book chapter: *Starting from Scratch*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

This chapter is process rather than product, so it is **not part of the audit sweep** — you cannot audit a finished interface for how it was made. It governs Workflow B (Build) and supplies the reasoning behind Workflow A (Tokens): §1.5 is the argument for why design systems exist at all, and every scale in `03`, `04`, `05` and `06` is an instance of it.

---

## 1.1 Start with a feature, not a layout

**Rule.** Begin by designing a real piece of functionality. Do not begin with the shell.

**Why.** "Designing the app" usually means designing the shell — top nav or sidebar, navigation left or right, contained or full-width, where the logo goes. Every one of those questions is genuinely unanswerable at the start, because an app is a collection of features and the shell's job is to serve them. Until a few features exist, there is no information with which to decide, so the work feels frustrating and stuck. That frustration is a signal that the sequence is wrong, not that the designer is bad at it.

**How.** Pick one concrete piece of functionality and design just that. A flight search, for example, needs a departure city field, a destination city field, a departure date, a return date, and a search button. Start there. The shell may turn out to be far smaller than expected — Google's worked out to almost nothing.

**Values.** None.

**Tailwind.** Build the component in isolation before the page frame exists.

**Fails as.** Days spent on navigation patterns before a single feature is designed; a beautiful shell wrapped around content that doesn't fit it.

---

## 1.2 Detail comes later

**Rule.** In early exploration, don't make low-level decisions about typefaces, shadows or icons.

**Why.** Those decisions matter eventually and are noise now — they consume the attention that structural exploration needs, and they're being made against a layout that is about to change anyway. Working in high fidelity makes them almost impossible to resist, which is why the environment matters as much as the intent.

**How.** If ignoring detail in the browser or a design tool is hard, change the medium. Jason Fried's method is paper and a thick Sharpie: obsessing over small details simply isn't possible at that stroke width, which makes it fast to explore many layout ideas.

**Values.** None.

**Tailwind.** —

**Fails as.** An hour on a typeface for a layout that gets discarded; three shadow variations compared before the content is settled.

### 1.2.1 Hold the color

**Rule.** Resist color even when moving to higher fidelity. Design in grayscale first.

**Why.** Color is the easiest way to fake hierarchy — it can make a weak structure look temporarily acceptable, which hides the structural problem until later. Removing it forces spacing, contrast and size to do all the work, and those are the levers that actually carry hierarchy (`02-hierarchy.md` §2.1). It's harder, and it produces a clearer interface with a strong hierarchy that is then easy to enhance with color.

**How.** Build in greys until the hierarchy reads correctly without color. Add color afterward, as reinforcement.

**Values.** None.

**Tailwind.** Build with `{neutral}` utilities only, then introduce `{primary}`. This also surfaces §5.7 violations early — anything that stops being understandable in grayscale was relying on color alone.

**Fails as.** A layout that falls apart when the brand color is removed; hierarchy carried entirely by a blue that turns out to be needed elsewhere.

### 1.2.2 Don't over-invest

**Rule.** Sketches and wireframes are disposable. Leave them behind once the decision is made.

**Why.** The whole point of low fidelity is speed — getting to the real thing sooner. Polishing a wireframe converts it from a thinking tool into an artifact worth defending, which is exactly the wrong relationship to it. Users can't do anything with a static mockup.

**How.** Use them to explore, then drop them. Don't maintain them.

**Values.** None.

**Tailwind.** —

**Fails as.** A meticulously maintained wireframe set that has drifted out of sync with the product; reluctance to change a design because of how long the mockup took.

---

## 1.3 Don't design too much

**Rule.** Don't design every feature before implementation. It's better if you don't.

**Why.** Working out how every feature interacts and how every edge case looks is genuinely hard in the abstract — and the abstract is the only place you're doing it. *How should this screen look with 2000 contacts? Where does the error message go? How does the calendar render two events at the same time?* These are answerable by building and looking, and close to unanswerable by imagining. Trying to settle them with a design tool and imagination alone is a setup for frustration.

**How.** §1.3.1 and §1.3.2.

**Values.** None.

**Tailwind.** —

**Fails as.** A comprehensive design spec that survives contact with implementation for about a week.

### 1.3.1 Work in cycles

**Rule.** Design a simple version of the next feature, build it, iterate on the working thing, then return to design mode for the next one.

**Why.** Design problems are much easier to fix in an interface you can actually use than to anticipate in advance. Unexpected complexity will surface during implementation — **that's the point**, not a failure of the design phase. Building early means your imagination doesn't have to carry the whole load.

**How.**
1. Design a simple version of the next feature.
2. Once the basic design is good, make it real.
3. Iterate on the working version until no problems remain.
4. Return to design mode for the next feature.

**Values.** None.

**Tailwind.** Designing in the browser collapses steps 1 and 2, which is part of why it's fast — and why the constrained scales matter, since typing values keeps you on the system where dragging does not (`03-layout-spacing.md` §3.2.3).

**Fails as.** A long design phase followed by an implementation phase that invalidates most of it.

### 1.3.2 Be a pessimist

**Rule.** Don't imply functionality in a design that you aren't ready to build. Design the smallest useful version.

**Why.** The failure mode is specific and expensive. Design a comment system with file attachments because attachments seem desirable later; discover mid-implementation that attachments are far more work than expected; and now there's no time to finish, so **the entire commenting system sits unshipped** while priorities move. A comment system without attachments would have been better than no comment system — but because attachments were in the design from day one, there's nothing to fall back to.

**How.** Expect new features to be hard to build. Design the smallest shippable version; if part of it is a nice-to-have, **design it later**. Building the simple version first guarantees you always have something to ship.

**Values.** None.

**Tailwind.** —

**Fails as.** Features stalled at 90% because a peripheral capability turned out to be the hard part; mockups showing functionality that never ships.

---

## 1.4 Choose a personality

**Rule.** Every design has a personality. Decide it deliberately — it's determined by a few concrete factors, not by feel.

**Why.** "Personality" sounds abstract and unactionable, which is why non-designers skip it and end up with a design that has one anyway, unchosen. In practice it reduces to four decisions — typeface, color, border radius, language — each concrete and each independently adjustable. Naming them converts a vague aspiration into four choices.

**How.** Decide §1.4.1–§1.4.4 explicitly. Use §1.4.5 if you don't have a gut feeling.

**Values.** **Four factors:** font, color, border radius, language.

**Tailwind.** These four map almost directly onto theme configuration — font family, primary hue, default radius. This is why the Workflow A interview asks about personality before generating anything.

**Fails as.** A product that feels generic; a banking app that reads playful and a consumer app that reads bureaucratic, neither on purpose.

### 1.4.1 Font choice

**Rule.** Typography is a large part of how a design feels.

**Why.** Typefaces carry cultural associations that arrive before any content is read.

**How.** Match the face to the intended feel:
- **Serif** — elegant, classic.
- **Rounded sans-serif** — playful.
- **Neutral sans-serif** — plain; use when other elements should carry the personality.

**Values.** None. Selection heuristics are in `04-typography.md` §4.2.

**Tailwind.** One `--font-sans` decision in the theme, plus a display face only if the personality needs it.

**Fails as.** A children's product in a corporate grotesque; a legal product in a rounded sans.

### 1.4.2 Color

**Rule.** Pay attention to how colors feel to you rather than to color psychology.

**Why.** There's a lot of science on color psychology, but choosing colors from psychology alone isn't practical — much of the decision is simply what looks good to you. Where the associations help is in explaining *why* a color feels right, after the fact, which is useful when you need to defend or refine a choice.

**How.** Common associations: **blue** is safe and familiar, and nobody ever complains about it; **gold** suggests expensive and sophisticated; **pink** is more fun and less serious.

**Values.** None.

**Tailwind.** Becomes the `{primary}` hue. Building the ramp from it is `05-color.md` §5.3.

**Fails as.** A palette justified entirely by a psychology chart; or the opposite, a brand color with no articulable rationale when it needs adjusting.

### 1.4.3 Border radius

**Rule.** Corner rounding has an outsized effect on feel. Whatever you pick, **stay consistent**.

**Why.** It's a small detail with a large impact, and unlike typeface or color it's applied to nearly every element, so it accumulates. The consistency requirement is the harder half: **mixing square and rounded corners in one interface almost always looks worse than committing to either**. Inconsistent radius is one of the most reliable signals of an unsystematic design.

**How.** Pick one and apply it everywhere:
- **Small radius** — fairly neutral, communicates little on its own.
- **Large radius** — playful.
- **No radius** — serious, formal.

**Values.** **Three positions:** small (neutral), large (playful), none (formal). Consistency is the invariant, not the value.

**Tailwind.** Set `--radius-*` once in the theme and use the same step throughout. Buttons, inputs, cards and modals sharing a radius is the whole rule. A radius scale is legitimate — small elements often need less than large ones — but it must be a scale, not per-component improvisation.

**Fails as.** `rounded-lg` cards containing `rounded-sm` buttons next to `rounded-full` avatars and square inputs, with no rule behind any of it.

### 1.4.4 Language

**Rule.** Word choice shapes personality as much as any visual property.

**Why.** Not a visual design technique, but words are everywhere in an interface, so their tone is inescapable — and choosing the right ones is as important as choosing the right color or typeface, arguably more. An impersonal tone reads official and professional; friendlier, more casual language makes a site feel friendlier.

**How.** Decide the register and hold it across buttons, empty states, errors and confirmations. Tone drifts fastest in error messages and edge-case copy, which are usually written last and by someone else.

**Values.** None.

**Tailwind.** —

**Fails as.** A warm, casual marketing site whose in-app errors read like a stack trace; inconsistent voice across a product.

### 1.4.5 Deciding what you actually want

**Rule.** When you have no gut feeling, look at the other sites your intended audience already uses.

**Why.** The audience's existing expectations are a better guide than introspection, and they're observable. If the sites they use are mostly serious, that's probably the register. If they're playful with some humor, that may be the better direction.

**How.** Survey what the audience uses. **Don't borrow too heavily from direct competitors** — you don't want to look like a second-rate version of something else.

**Values.** None.

**Tailwind.** This is the reference-site question in the Workflow A interview. Where a URL is offered, the browser tools can extract the actual font stack and primary color as a starting point — the systematized version of `04-typography.md` §4.2.5.

**Fails as.** A design derived from a single competitor; a personality chosen from the founder's taste with no relation to the audience.

---

## 1.5 Limit your choices

**Rule.** Choose from a small predefined set instead of an unlimited pool. This is the book's central method.

**Why.** Unlimited options sound like freedom and function as paralysis. Designing without constraints makes decisions torture because **there is always more than one right choice**, and no way to feel confident in any of them. The concrete demonstration: a row of buttons with different background colors that are almost impossible to tell apart. None would be a bad choice — which is exactly why the decision can't be made.

The questions this produces are endlessly repeatable and individually unimportant: 12px or 13px? 10% or 15% shadow opacity? 24px or 25px avatar? Medium or semibold? 18px or 20px bottom margin? Each is unanswerable and each recurs constantly.

**How.** §1.5.1–§1.5.3.

**Values.** None.

**Tailwind.** Tailwind is this rule implemented as a tool. Utility classes are a constrained set by construction, and arbitrary-value syntax (`p-[13px]`) is the escape hatch that reintroduces the problem — which is why every reference file bans it.

**Fails as.** Repeated agonizing over decisions that don't matter; different values chosen for the same situation on different days.

### 1.5.1 Define systems in advance

**Rule.** Do the hard work of picking values **once**, not every time you design something.

**Why.** Front-loading the decision converts an unbounded choice into a bounded one at every future call site. More work up front, far less decision fatigue afterward — and consistency arrives as a side effect rather than as a discipline anyone has to maintain.

**How.** Don't open the color picker for a new blue — choose from **8–10 shades** picked ahead of time. Don't nudge a font size a pixel at a time — define a restrictive type scale in advance and take future sizes from it.

**Values.** **8–10 shades** per color. Full ramp construction in `05-color.md` §5.3.3; type scale in `04-typography.md` §4.1.1d.

**Tailwind.** This is what the theme block is for. Everything in Workflow A is this rule.

**Fails as.** A color picker open in a design tool; a "design system" that documents components but not values.

### 1.5.2 Designing by process of elimination

**Rule.** With a constrained set, decide by comparison: guess the middle, test both neighbors, re-center if an outer option wins.

**Why.** This works only because a proportional scale guarantees adjacent options look **noticeably different** (`03-layout-spacing.md` §3.2.1). Given that, two of three options are usually *obviously* bad, and the decision becomes trivial rather than agonizing. On a linear scale with imperceptible steps the method degenerates, which is the practical argument for the 25% rule.

**How.** Sizing an icon against a scale of 12/16/24/32:
1. Guess the one that will look best — say 16px.
2. Try the values on either side, 12px and 24px.
3. If both outer options are obviously wrong, the middle one is the answer.
4. If an outer option looks best, re-center on it and compare again.

**Values.** Illustrative scale: **12, 16, 24, 32px**.

**Tailwind.** `w-4` → try `w-3` and `w-6` → decide. Fast in the browser precisely because the set is finite.

**Fails as.** Sliding a value continuously looking for an optimum that doesn't exist; a decision that takes ten minutes and gets revisited next week.

### 1.5.3 Systematize everything

**Rule.** Approach design with a system-focused mindset. Look for new systems as you make new decisions.

**Why.** The more systems in place, the faster you work and the less you second-guess yourself. The generalization: **try to avoid making the same minor decision twice** — the second occurrence is the signal that a system is missing.

**How.** Build systems for: **font size, font weight, line height, color, margin, padding, width, height, box shadows, border radius, border width, opacity** — and anything else where you find yourself laboring over a low-level decision.

You don't have to define all of it ahead of time. Introduce systems as decisions arise.

**Values.** The book's list, in full: **font size · font weight · line height · color · margin · padding · width · height · box shadow · border radius · border width · opacity**. **12 systems.**

**Tailwind.** Every one has a theme namespace. Note which are commonly left unsystematized in practice — **border width** and **opacity** are the two most often improvised, and `02-hierarchy.md` §2.7.2 depends on border width being systematic.

**Fails as.** A design system covering color and type only, with spacing, radius, border width and opacity improvised per component.

---

## Build-time checklist

Not an audit lens. Use during Workflow B.

1. Is there a real feature being designed, or is this the shell? `1.1`
2. Are low-level details being decided before the structure is settled? `1.2`
3. Does the hierarchy hold up in grayscale? `1.2.1`
4. Is anything being designed that isn't going to be built now? `1.3.2`
5. Have all four personality factors been decided — font, color, radius, language? `1.4`
6. **Is border radius consistent across every component?** `1.4.3`
7. Does every value come from a defined scale? `1.5.1`
8. Which of the **12 systems** exist, and which are being improvised? `1.5.3`

## Cross-references

- Grayscale-first as a hierarchy technique → `02-hierarchy.md` §2.1
- The 25% rule that makes elimination work → `03-layout-spacing.md` §3.2.1
- Type scale construction → `04-typography.md` §4.1
- Font selection heuristics → `04-typography.md` §4.2
- Palette construction → `05-color.md` §5.3
- Elevation system → `06-depth.md` §6.2.1
- Interview and token emission → `11-design-tokens.md`
