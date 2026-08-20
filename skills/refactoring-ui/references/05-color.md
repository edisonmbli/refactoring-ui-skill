# Working with Color

> Covers matrix rows **5.1 – 5.7** (22 items). Book chapter: *Working with Color*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

Fourth lens in the sweep. This is the chapter with the highest density of hard numbers, and it is the operational basis for Workflow A — the palette algorithm in §5.3.3, the saturation compensation in §5.4, and the hue rotation in §5.4.2 are what `scripts/generate_palette.py` implements.

**The book gives a complete method and no specific color values.** Every palette shown in it is an illustration. Do not attempt to extract "the book's colors" — they don't exist. Generate them.

---

## 5.1 Ditch hex for HSL

**Rule.** Represent colors in HSL, not hex or RGB.

**Why.** Hex and RGB encode colors in a way that hides their perceptual relationships: two colors that obviously belong to the same family look completely unrelated as hex codes. That makes systematic work almost impossible — you can't tell by reading a value whether it's a lighter version of another, and you can't produce a related color by adjusting a number.

HSL encodes the three attributes the eye actually perceives, so relationships that are visually obvious become arithmetically obvious. "Same color, lighter" becomes "same H, same S, higher L." Every rule in this chapter is stated in HSL because in hex none of them can be stated at all.

**How.** Author colors in HSL. Convert to whatever the output format requires at the end, not at the start.

**Values.** See §5.1.a.

**Tailwind.** v4's `@theme` accepts any CSS color syntax, so HSL can survive into the theme. Modern CSS also supports `hsl(from var(--c) h s calc(l + 10%))`, which makes derived colors expressible directly — though per §5.3, derive shades **once** when building the palette, not at point of use.

**Fails as.** A palette as a list of hex codes with no visible structure; developers unable to tell which of two hex values is the lighter shade without pasting them into a tool.

### 5.1.a The three components

**Rule.** Hue, saturation and lightness each mean something specific.

**Why.** The rules downstream depend on knowing exactly what each axis does — particularly that saturation has no effect at 0% and that lightness is not brightness.

**How.** Read the axes as:

- **Hue** — position on the color wheel, in degrees. It's the attribute that lets two non-identical colors both read as "blue."
- **Saturation** — how colorful or vivid. 0% is grey, 100% is intense. **Without saturation, hue is irrelevant** — rotating hue at 0% saturation changes nothing at all.
- **Lightness** — how close to black or white. 0% is pure black, 100% is pure white, 50% is the pure hue.

**Values.** Hue: **0° red, 120° green, 240° blue**. Saturation: **0% grey → 100% vivid**. Lightness: **0% black, 50% pure hue, 100% white**.

**Tailwind.** —

**Fails as.** Attempts to "warm up" a grey by rotating hue while leaving saturation at 0% — a no-op that looks like a broken tool.

### 5.1.1 HSL vs. HSB

**Rule.** HSL lightness and HSB brightness are different things. Don't confuse them.

**Why.** This bites specifically when moving between design tools and code, because they disagree about which model to use. In HSB, 0% brightness is always black — but 100% brightness is only white when saturation is 0%. At 100% saturation, **HSB 100% brightness equals HSL 100% saturation at 50% lightness**. So a color that reads as "full brightness" in a design tool is a mid-lightness color in CSS, and values copied across without conversion land somewhere unintended.

**How.** Work in HSL for the web. **Design software commonly favors HSB; browsers only understand HSL.** If your tool shows HSB, convert rather than transcribe.

**Values.** HSB(h, 100%, 100%) = HSL(h, **100%**, **50%**).

**Tailwind.** —

**Fails as.** Colors that look right in Figma and washed out in the browser; a palette whose lightness values cluster near 100% because they were read off an HSB picker.

---

## 5.2 You need more colors than you think

**Rule.** Five-color palette generators cannot build a real interface. You need a comprehensive set.

**Why.** The five-perfect-colors model is seductive because it makes the palette a solved problem in one step. But an interface makes dozens of color decisions the model never anticipated: a hover state, a disabled control, a subtle divider, a tinted alert background, a slightly darker panel. Each needs a color that is *related* to one you have and not identical to it. With five values you either compromise repeatedly or improvise — and improvising is exactly what §5.3 exists to prevent.

**How.** Build the three categories in §5.2.1–§5.2.3.

**Values.** See below; totals in §5.2.3.

**Tailwind.** Tailwind's default palette is built on this premise — many families, each with a full ramp. That structure is the point, whether or not you use its specific colors.

**Fails as.** A brand guideline listing five hex codes and an implementation full of one-off colors that appear nowhere in it.

### 5.2.1 Greys

**Rule.** You need **8–10 greys**. Almost everything in an interface is grey.

**Why.** Text, backgrounds, panels, borders, form controls, dividers, icons, disabled states — the overwhelming majority of an interface's surface is neutral. Three or four shades sound sufficient and stop being sufficient quickly: you need something a little darker than one shade and a little lighter than the next, and without it you compromise on every subsequent decision. Ten is the other boundary — enough that you don't feel constrained, not so many that you're deciding between indistinguishable neighbors.

**How.** Build the ramp per §5.3.4. **Start from a very dark grey, not true black** — true black tends to look unnatural on screen — and step up to white.

**Values.** **8–10 shades.** Darkest is a very dark grey, **not #000**.

**Tailwind.** `{neutral}-50` through `{neutral}-900` is this ramp. Which family — gray, slate, zinc, stone, or custom — is a temperature decision, see §5.5.1.

**Fails as.** A palette with three greys and a codebase full of hand-mixed intermediates; pure black text that looks harsh.

### 5.2.2 Primary color(s)

**Rule.** One primary color, maybe two, with **5–10 shades** each.

**Why.** The primary is what makes a product recognizable as itself — the reason Facebook reads as "blue." It carries primary actions, active navigation and brand presence. It needs a full ramp because it appears in contexts with opposite requirements: ultra-light shades work as tinted backgrounds for alerts and highlighted rows, dark shades work as text where the mid shades would fail contrast.

**How.** Pick the base per §5.3.1 and build the ramp per §5.3.3.

**Values.** **1, maybe 2** primaries; **5–10 shades** each.

**Tailwind.** `{primary}-50` … `{primary}-900`. Map it to a semantic name in the theme so components never reference the raw family.

**Fails as.** A brand color available only at one value, so buttons, hover states and tinted backgrounds are all improvised from it.

### 5.2.3 Accent colors

**Rule.** Beyond the primary, you need accent colors for semantic states and for emphasis — each with multiple shades.

**Why.** Some information is inherently categorical and color is the natural encoding: this succeeded, this is a warning, this is new. The primary can't carry those meanings without ambiguity. And if color must *distinguish* similar things — lines on a graph, events on a calendar, tags on a project — the count grows with the data, not with the brand.

**How.** Cover: an attention-getting color for new features (yellow, pink, teal); **red** for destructive confirmation; **yellow** for warnings; **green** for positive trends. Add more where data categorization demands it. Each gets multiple shades even though accents are used sparingly — the sparing use is what makes the wrong shade conspicuous.

**Values.** A complex UI can need **as many as 10 colors with 5–10 shades each**.

**Tailwind.** `{danger}`, `{accent}` and friends, each a full ramp, aliased semantically: `--color-danger-600`, not `--color-red-600`. Components should never name a hue.

**Fails as.** Success and error states improvised from whatever green and red were nearest; a chart with eight series colored by whatever the library defaulted to.

---

## 5.3 Define your shades up front

**Rule.** Define a fixed set of shades in advance. **Never** generate them at point of use with preprocessor functions like `lighten()` or `darken()`.

**Why.** On-the-fly derivation feels systematic — it's a function of a base color, so surely it's consistent. It isn't. Each call site passes a slightly different amount, nobody audits the set, and the result is thirty-five slightly different blues that all look the same and none of which were chosen. It has the form of a system with none of the benefit: no constrained set to choose from, no guarantee two components share a value.

There's a second, subtler failure: `lighten()` and `darken()` move only lightness, so they hit exactly the desaturation problem in §5.4. Derived shades come out washed out even when they're consistent.

**How.** Build the ramp once, by the procedure in §5.3.1–§5.3.4. Reference shades by name thereafter.

**Values.** None.

**Tailwind.** This is what a theme is for. `bg-{primary}-600`, never `bg-[color-mix(...)]` or a Sass function at the call site.

**Fails as.** A stylesheet with dozens of near-identical color values; a design system nobody can enumerate the colors of.

### 5.3.1 Choose the base color first

**Rule.** Start with the base — the middle shade the rest are built around.

**Why.** Building from the middle outward keeps the most-used shade the one you actually chose. Building from an endpoint makes the middle an artifact of interpolation, and the middle is where most of the work happens.

**How.** For primary and accent colors, pick a shade that would **work well as a button background**. That's a concrete, testable target: it must be dark enough for white text and vivid enough to read as intentional.

**Values.** **There are no rules here** — no "start at 50% lightness." Every hue behaves differently and this step is done by eye.

**Tailwind.** This becomes the `500` stop.

**Fails as.** A base picked at an arbitrary lightness that turns out unusable as a button, forcing the whole ramp to be rebuilt.

### 5.3.2 Finding the edges

**Rule.** Pick the darkest and lightest shades next, choosing them by where they'll be used.

**Why.** The endpoints have specific jobs, and choosing them abstractly ("as dark as possible") produces values that are wrong for those jobs. The darkest shade is usually **text**; the lightest is usually a **tinted background**. Choosing against the real use case means the endpoint is correct on first use rather than adjusted later.

**How.** A simple **alert component** exercises both at once — tinted background, colored text on it — which makes it a good place to pick them. Start from the base's hue and adjust saturation and lightness until both read well.

**Values.** No numeric targets; match the base hue, tune S and L.

**Tailwind.** These become `100` and `900` (or `50` and `950` on a longer ramp).

**Fails as.** A lightest shade too saturated to sit behind text; a darkest shade that fails contrast in the one place it was meant for.

### 5.3.3 Filling in the gaps

**Rule.** With base, darkest and lightest fixed, fill the gaps by repeated bisection.

**Why.** Bisection is what makes the ramp perceptually even without arithmetic. Each new shade is chosen as *the visual compromise between its neighbors*, which is a judgment the eye makes reliably — far more reliably than it evaluates an absolute lightness value. And **nine divides well**: it bisects cleanly twice, so the whole ramp is built in two passes.

**How.**

1. Label darkest **900**, base **500**, lightest **100**.
2. Pick **700** and **300** — the midpoints of the two gaps. Each should feel like the perfect compromise between the shades on either side.
3. That opens four new gaps. Fill **800, 600, 400, 200** the same way.

**Values.** **At least 5 shades**, closer to **10** to avoid feeling constrained. **Nine** is the recommended number. Order: **900/500/100 → 700/300 → 800/600/400/200**.

**Tailwind.** Produces exactly Tailwind's `100`–`900` structure. Tailwind also ships `50` and `950`; useful, and built the same way by extending the edges.

**Fails as.** A ramp interpolated linearly in lightness, where the middle shades are perceptually bunched and the ends spread too far apart.

### 5.3.4 What about greys?

**Rule.** Same procedure for greys. The base matters less.

**Why.** Greys have no vivid mid-point to anchor on, so there's no equivalent of "works as a button background." The endpoints carry the constraints instead, and the middle can be interpolated more freely.

**How.** Pick the **darkest grey by choosing the color for the darkest text** in the project, and the **lightest by choosing something that works as a subtle off-white background**. Then fill in as in §5.3.3.

**Values.** Same **8–10** shades from §5.2.1.

**Tailwind.** `{neutral}-50` … `{neutral}-900`.

**Fails as.** A grey ramp anchored on a mid grey, whose darkest value turns out too light for body text.

### 5.3.5 It's not a science

**Rule.** The procedure gets you a good starting palette. Adjust by eye afterward — but don't add shades.

**Why.** No formula fully captures how a color behaves in context; once shades are used at real sizes against real backgrounds, some will want more saturation or a nudge in lightness. **Trust your eyes, not the numbers.**

The discipline is at a different point than people expect. Tweaking an existing shade is fine and expected. **Adding** shades is what destroys the system: the value of a constrained palette is entirely in the constraint, and a palette you keep extending is not a palette. If you aren't diligent about limiting it, you may as well have no color system at all.

**How.** Tweak freely. Before adding a shade, establish that no existing one works — the answer is usually that one does.

**Values.** None.

**Tailwind.** Adjust theme values as needed. Treat adding a new stop as a design-system change, not a component change.

**Fails as.** A palette that started at nine shades and reached twenty-three, each addition individually justified.

---

## 5.4 Don't let lightness kill your saturation

**Rule.** As lightness moves away from 50%, **increase saturation** — otherwise the outer shades look washed out.

**Why.** In HSL, saturation's perceptual effect weakens as lightness approaches 0% or 100%. The same saturation value that reads as vivid at 50% lightness reads as noticeably duller at 90%. So a ramp built by holding saturation constant and varying only lightness — which is what feels systematic, and what `lighten()`/`darken()` do — produces ends that drift toward grey. The colors are numerically consistent and perceptually inconsistent.

It's subtle per shade and compounds across a UI, especially where a light shade covers a large area.

**How.** Raise saturation as you move outward in both directions. If the base is already at or near 100% saturation, you can't raise it further — that's what §5.4.1 and §5.4.2 solve.

**Values.** **Increase saturation as lightness moves away from 50%**, in both directions.

**Tailwind.** Tailwind's default palettes already do this — inspect any family's ramp in HSL and saturation rises toward both ends. Custom ramps must do it explicitly.

**Fails as.** Light tint backgrounds that look grey rather than colored; dark shades that look muddy; a ramp that loses its identity at the ends.

### 5.4.1 Use perceived brightness to your advantage

**Rule.** Every hue has an inherent perceived brightness, independent of its lightness value.

**Why.** Two colors at identical HSL lightness can look very different in brightness — yellow reads as much lighter than blue at the same L. Perceived brightness is a property of the hue itself, arising from how the eye weights the RGB primaries. Crucially it does **not** vary linearly around the wheel: there are **three local minima and three local maxima**, which is what makes §5.4.2 possible.

**How.** Compute it when you need it:

```
perceived brightness = √(0.299r² + 0.587g² + 0.114b²) / 255
```

**Values.** Formula above. Sampling hues at 100% saturation and 50% lightness: local **minima at red, green and blue**; local **maxima at yellow, cyan and magenta**.

**Tailwind.** Implemented in `scripts/check_contrast.py`.

**Fails as.** A categorical palette picked at even hue intervals and equal lightness, where the yellow series dominates and the blue recedes.

### 5.4.2 Changing brightness by rotating hue

**Rule.** Change a color's brightness by **rotating its hue**, not only by changing lightness.

**Why.** Adjusting lightness moves a color toward white or black, and it takes intensity with it — the result is lighter but also visibly closer to grey. Since hues differ in inherent brightness (§5.4.1), rotating toward a brighter hue raises brightness while **saturation stays intact**, so the color stays rich.

This is what makes yellow ramps work. Darkening yellow by lightness alone produces a dull brown; rotating gradually toward orange as lightness drops produces dark shades that feel **warm and rich** rather than muddy.

**How.**

- **To lighten** — rotate toward the nearest bright hue: **60°, 180°, or 300°**.
- **To darken** — rotate toward the nearest dark hue: **0°, 120°, or 240°**.
- Combine with lightness changes; take some of the shift from each.

**Values.** Bright targets **60/180/300°**; dark targets **0/120/240°**. **Never rotate more than 20–30°** — beyond that it stops reading as lighter or darker and starts reading as a different color.

**Tailwind.** Implemented in `scripts/generate_palette.py`. Visible in Tailwind's own ramps: yellow shifts toward orange as it darkens, exactly this technique.

**Fails as.** Yellow, orange and lime ramps whose dark shades are brown; ramps that lose their hue identity at one end.

---

## 5.5 Greys don't have to be grey

**Rule.** True grey is 0% saturation. Most greys in good interfaces are saturated, often heavily.

**Why.** Pure neutral greys read as slightly lifeless and disconnected from everything else on screen. Saturating them ties the neutrals to the palette and gives the interface a consistent atmosphere — it's a large part of why some products feel coherent and others feel assembled.

**How.** Add saturation to the whole grey ramp, in the direction chosen per §5.5.1.

**Values.** True grey = **0% saturation**. Real-world "greys" are frequently saturated heavily.

**Tailwind.** This is the difference between `gray`, `slate`, `zinc`, `stone` and `neutral` — `neutral` is near-pure, `slate` is cool, `stone` is warm. Choosing among them *is* this decision.

**Fails as.** An interface using pure `#808080`-family greys next to a saturated brand color, where the neutrals look dead by comparison.

### 5.5.1 Color temperature

**Rule.** Saturate greys toward blue for cool, toward yellow/orange for warm. Compensate at both ends of the ramp.

**Why.** Same mechanism as light bulbs: "warm white" is yellow-ish, "cool white" is blue-ish, and neither is neutral. The choice sets the emotional temperature of the entire interface, since greys occupy most of it.

The compensation clause is where this is usually got wrong. §5.4 applies to greys too: if saturation is held constant across the ramp, the lightest and darkest greys drift back toward neutral and the temperature becomes inconsistent — warm in the mid-tones, neutral at the ends.

**How.** Pick a direction. Apply it across the ramp. **Increase saturation for the lighter and darker shades** so the temperature holds. How far to push is entirely a taste decision — a little to tip it slightly, a lot to commit.

**Values.** Cool = saturate with **blue**; warm = saturate with **yellow or orange**. Raise saturation at both ends.

**Tailwind.** Choose a family and stay in it — mixing `slate` and `stone` in one interface produces greys that clash in a way that's hard to diagnose. For a custom ramp, verify the endpoint saturation explicitly.

**Fails as.** Greys that feel warm in the mid-range and neutral at the extremes; two components using different grey families, looking subtly mismatched.

---

## 5.6 Accessible doesn't have to mean ugly

**Rule.** Meet WCAG contrast minimums without letting them dictate the design.

**Why.** Contrast requirements are easy for dark text on light backgrounds and get hard as soon as color is involved — and the naive fix (make it darker) has design consequences that push people to skip accessibility rather than solve it. §5.6.1 and §5.6.2 are two techniques that satisfy the ratio without those consequences.

**How.** Check every text/background pair against the thresholds. When a pair fails, apply §5.6.1 or §5.6.2 rather than simply darkening.

**Values.** WCAG minimums: **4.5:1 for normal text (under ~18px)**, **3:1 for large text**.

**Tailwind.** Verify with `scripts/check_contrast.py` across the token matrix, not per component.

**Fails as.** Placeholder text and disabled states that fail contrast; a palette signed off in a design tool and never measured.

### 5.6.1 Flipping the contrast

**Rule.** Instead of light text on a dark colored background, use dark colored text on a light colored background.

**Why.** White text on a colored background needs the color to be **surprisingly dark** to reach 4.5:1 — usually much darker than expected. That creates a hierarchy problem: a dark, saturated block is visually heavy and grabs attention, which is wrong when the element isn't meant to be the page's focus. Accessibility and hierarchy end up in direct conflict.

Flipping resolves it. Dark colored text on a light tint of the same color easily clears the ratio, keeps the color present as support, and is far less in-your-face — so it doesn't compete with the page's real primary action.

**How.** Use the light end of the ramp as the background and the dark end as the text.

**Values.** Same **4.5:1**.

**Tailwind.** `bg-{accent}-100 text-{accent}-800` instead of `bg-{accent}-700 text-white`. This is the standard shape for alerts, badges, tags and secondary buttons — and §5.3.2 is why those two stops were chosen against an alert in the first place.

**Fails as.** Pages with several dark saturated blocks all demanding attention; a warning banner that outweighs the content it's warning about.

### 5.6.2 Rotating the hue

**Rule.** For colored text on a colored background, raise contrast by rotating toward a brighter hue rather than moving toward white.

**Why.** This is the hardest contrast case — secondary text inside a dark colored panel. Adjusting only lightness and saturation means you approach pure white before reaching 4.5:1, and then the secondary text looks the same as the primary text, destroying the hierarchy the color was supporting.

§5.4.1 provides the exit: since hues differ in inherent brightness, rotating toward a brighter hue raises contrast **without** moving toward white. The text stays clearly colored, clearly secondary, and clearly legible.

**How.** Rotate the text color's hue toward **cyan, magenta or yellow**, subject to the same **20–30°** limit from §5.4.2.

**Values.** Bright targets: **cyan, magenta, yellow**. Rotation capped at **20–30°**.

**Tailwind.** Requires a hand-picked value in the theme rather than a stop from the existing ramp — the ramp holds hue constant by construction, which is exactly the constraint being escaped. Note this connects to `02-hierarchy.md` §2.3: same problem, and this is the accessible-contrast version of that fix.

**Fails as.** Secondary text on colored panels that is either illegible or indistinguishable from the primary text; hierarchy lost inside every dark panel in the product.

---

## 5.7 Don't rely on color alone

**Rule.** Color must support information the design already conveys some other way. It can never be the only channel.

**Why.** Color blindness — red-green most commonly — makes color-only encoding unreadable for a substantial share of users. And the failure is invisible to everyone else: metric cards where green means up and red means down look perfectly clear to the person who built them and convey nothing to the person who can't separate the hues. The information isn't degraded, it's absent.

**How.** Two techniques depending on the case:

1. **Add a second channel.** For state and direction, add an icon, an arrow, a sign, or text. A metric card with an up-arrow works for everyone; the color becomes reinforcement.
2. **Differentiate by contrast, not hue.** For multi-series charts, calendars and tag sets, use light-to-dark steps instead of distinct hues. **Distinguishing light from dark is much easier for a colorblind viewer than distinguishing two hues** — and it also survives greyscale printing and low-quality displays.

**Values.** None.

**Tailwind.** For chart series, step one ramp (`{primary}-300` / `-500` / `-700` / `-900`) rather than assigning a different family per series. Pair semantic colors with icons throughout: `text-{danger}-600` alongside an alert icon, never alone.

**Fails as.** Dashboards where trend direction is color-only; charts with a legend nobody can map to the lines; validation states shown as red borders with no message or icon.

---

## Audit checklist for this lens

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

## Cross-references

- Text on colored backgrounds, the hierarchy-side version of §5.6.2 → `02-hierarchy.md` §2.3
- Text color tiers drawn from the grey ramp → `02-hierarchy.md` §2.2.a
- Color as a depth cue → `06-depth.md` §6.4.1
- Colorizing photography to match the palette → `07-images.md` §7.2.4
- Gradient hue limits and accent borders → `08-finishing-touches.md` §8.3.1
- Palette generation, contrast checking, token emission → `11-design-tokens.md`
