# Working with Images

> Covers matrix rows **7.1 – 7.4.2** (14 items). Book chapter: *Working with Images*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

Sixth lens in the sweep. Skip it entirely when the surface has no imagery — but check first, because icons and avatars count and are the most commonly mishandled cases.

The chapter has a recurring theme: **images are the part of a design you control least**, so most of the work is building enough structure that they can't do damage.

---

## 7.1 Use good photos

**Rule.** Bad photography ruins a design regardless of how good everything else is.

**Why.** Photography occupies large areas and carries strong quality signals, so it dominates perceived quality. And unlike spacing or type, it cannot be fixed downstream — no amount of layout skill compensates for a bad photo. Taking great photos isn't about an expensive camera; it's lighting, composition and color, which are skills that take years.

**How.** Two options: **hire a professional photographer** when the project needs specific images, or **use high quality stock photography** when the needs are more generic — including free sources like Unsplash.

Never design using placeholder images intending to shoot replacements on a phone later. **It never works** — the design was tuned to images of a quality the replacements won't have.

**Values.** None.

**Tailwind.** —

**Fails as.** A polished layout undermined by amateur photography; a design that looked good in the mockup and shipped with real photos that broke it.

---

## 7.2 Text needs consistent contrast

**Rule.** When text over an image is hard to read, **the problem is the image, not the text**.

**Why.** This is the diagnostic that unlocks the whole section. The usual response is to try text colors — white doesn't work, black doesn't work, nothing works — and conclude the combination is impossible. It is, but for a reason that has nothing to do with the text: photographs are dynamic, with very light and very dark regions in the same frame. Any single text color succeeds against part of the image and fails against another.

Since the text is one color and the background is many, no text-side change can fix it. **Reduce the image's dynamics** and the problem becomes solvable.

**How.** Four techniques, §7.2.2–§7.2.5, usable in combination.

**Values.** None.

**Tailwind.** —

**Fails as.** Hero headlines legible on the left of the image and invisible on the right; endless cycling through text colors and weights with no combination working.

### 7.2.1 The problem with background images

**Rule.** The mechanism: photos have many very light and very dark areas, so white text is lost in light regions and dark text is lost in dark regions.

**Why.** Stated explicitly because the fix follows directly from it — you're reducing dynamic range, and each technique below is a different way to do that.

**How.** Establish which regions are failing before choosing a technique. If only a small area is problematic, §7.2.5 preserves the most of the image; if the whole frame is dynamic, §7.2.2 or §7.2.3.

**Values.** None.

**Tailwind.** —

**Fails as.** Applying a heavy overlay to fix a problem confined to one corner, flattening the whole photograph unnecessarily.

### 7.2.2 Add an overlay

**Rule.** Put a semi-transparent overlay between the image and the text.

**Why.** It compresses the image's range toward one end, so the text has a consistent relationship with everything behind it. Direction matters and follows from which text color you want: **black tones down the light areas** and helps light text stand out; **white brightens the dark areas** and helps dark text stand out.

**How.** Choose the overlay color from the text color, then set opacity to the minimum that makes the text consistently readable.

**Values.** None.

**Tailwind.** A `bg-black/50` layer positioned absolutely over the image, text above it. A gradient overlay (`bg-gradient-to-t from-black/70`) is often better — it darkens only where the text sits and leaves the rest of the photo intact.

**Fails as.** Overlays at 70%+ opacity that obliterate the image, raising the question of why there's a photo at all.

### 7.2.3 Lower the image contrast

**Rule.** Reduce the contrast of the image itself.

**Why.** More control than an overlay. The compromise with an overlay is that it lightens or darkens the **whole** image rather than the problem areas; lowering contrast attacks the dynamic range directly, which is the actual problem, and preserves more of the image's character.

**How.** Lower the contrast, then **adjust brightness to compensate** — reducing contrast changes how light or dark the image feels overall, and skipping the compensation produces a flat grey photo.

**Values.** None.

**Tailwind.** `contrast-75 brightness-110` as filter utilities, or bake it into the asset. Baking is preferable for hero images — it avoids a paint-time filter on a large image.

**Fails as.** Contrast reduced without brightness compensation, leaving a washed-out grey photograph.

### 7.2.4 Colorize the image

**Rule.** Tint the image with a single color.

**Why.** Reduces the image to one hue's worth of variation, which makes text contrast predictable — and simultaneously **makes a background image pair more nicely with your existing brand colors**, solving a compositional problem alongside the legibility one.

**How.** Some photo software has this as a first-class feature. If yours doesn't, three steps:

1. **Lower the image contrast**, to balance things out.
2. **Desaturate the image**, to remove existing color.
3. **Add a solid fill** using the **multiply** blend mode.

**Values.** **Three steps, in order.** Blend mode: **multiply**.

**Tailwind.** `grayscale contrast-75` on the image with a `bg-{primary}-700 mix-blend-multiply` layer above it.

**Fails as.** A tint applied without desaturating first, where residual color fights the tint and produces muddy results.

### 7.2.5 Add a text shadow

**Rule.** A text shadow raises contrast only where it's needed. It should look like a **subtle glow**, not a shadow.

**Why.** The other three techniques modify the whole image. A text shadow is local — it darkens or lightens only immediately around the glyphs, so the image keeps more of its dynamics. That makes it the right choice when the photograph is the point.

The glow requirement is what makes it invisible: an offset shadow reads as a shadow and looks dated, while a large blur with no offset reads as the text simply being easier to see.

**How.** **Large blur radius, no offset of any kind.** Still reduce the overall image contrast — combining the two means you can reduce it **a little less** than you'd otherwise need.

**Values.** **Large blur radius. Zero offset.**

**Tailwind.** `[text-shadow:0_0_20px_rgb(0_0_0_/_0.6)]` or a theme-defined text-shadow utility. Note the zero X **and** zero Y — an offset here is the whole failure.

**Fails as.** Hard offset text shadows that look like 2005; text shadows used alone on a very dynamic image, which isn't enough.

---

## 7.3 Everything has an intended size

**Rule.** Every image asset is drawn for a size. Using it far from that size degrades it — **in both directions**.

**Why.** Everyone knows scaling bitmaps up produces fuzziness. That's the obvious case and it's not the interesting one. The rule generalizes: assets encode a level of detail appropriate to their intended size, and that detail is wrong at other sizes whether the format is vector or raster. §7.3.1–§7.3.3 are three failures people commit while believing they're being safe.

**How.** Match asset to intended size, or redraw.

**Values.** None.

**Tailwind.** —

**Fails as.** Assets reused at whatever size the layout wanted.

### 7.3.1 Don't scale up icons

**Rule.** Don't enlarge small icons. Vector doesn't help.

**Why.** The reasoning that traps people is correct as far as it goes: SVG is resolution-independent, so quality won't degrade. True — and irrelevant. Icons **drawn at 16–24px** are drawn with the detail appropriate to that size, and blown up **3× or 4×** they lack detail and feel **disproportionately chunky**. The strokes that read as crisp at 16px read as heavy slabs at 64px. It's a drawing problem, not a rendering problem.

**How.** If small icons are all you have, **enclose the icon in another shape and give that shape a background color**. The icon stays near its intended size while the composite fills the larger space.

**Values.** Icons drawn at **16–24px** should not be scaled to **3–4×**.

**Tailwind.** `<div class="w-12 h-12 rounded-lg bg-{primary}-100 flex items-center justify-center"><Icon class="w-6 h-6 text-{primary}-600" /></div>` — the standard feature-icon pattern, and this rule is its origin.

**Fails as.** Landing page feature sections with 64px icons that look clumsy; empty-state illustrations that are one enlarged UI icon.

### 7.3.2 Don't scale down screenshots

**Rule.** Don't shrink a full-size screenshot to fit a smaller space.

**Why.** Shrinking preserves detail count while removing the space to render it, so the result crams far too much into far too little. The arithmetic is brutal: shrink by **70%** and the **16px** font in your app becomes a **4px** font in the screenshot. Visitors squint at text they can't read — so the screenshot fails at the one job it had.

**How.** Three options:
1. **Take the screenshot at a smaller screen size** — the tablet layout, say — and give it plenty of space so it needs less shrinking.
2. **Take a partial screenshot**, so it fits in less space at full scale.
3. **Draw a simplified version** of the UI with details removed and small text replaced by simple lines. This communicates the big-picture design without tempting anyone to read it.

**Values.** **70%** reduction turns **16px** text into **4px** text.

**Tailwind.** —

**Fails as.** Product pages with unreadable app screenshots; feature sections where the screenshot is decorative because nobody can parse it.

### 7.3.3 Don't scale down icons, either

**Rule.** Icons drawn for large sizes turn to mush when shrunk.

**Why.** The symmetric failure to §7.3.1: detail intended for a large canvas cannot survive into a small one, and the renderer's attempt produces choppy, fuzzy results. **Favicons are the most extreme case** — shrink a logo drawn at **128px** to favicon size and the browser tries to render all that detail in a **16px** square, turning it to mush.

**How.** **Redraw a simplified version at the target size**, so you control the compromises instead of leaving them to the browser.

**Values.** **128px** logo → **16px** favicon is the canonical failure.

**Tailwind.** —

**Fails as.** An unrecognizable favicon; a logo used at 20px in a nav bar as an indistinct smudge.

---

## 7.4 Beware user-uploaded content

**Rule.** With user-uploaded images you have none of the usual controls — no contrast tuning, no color adjustment, no cropping to the right frame.

**Why.** Every other rule in this chapter assumes you choose the image. Here you don't, and users will supply images at any aspect ratio, any quality, any background color. You will always be at their mercy to some extent, but structural defenses limit the damage.

**How.** §7.4.1 and §7.4.2.

**Values.** None.

**Tailwind.** —

**Fails as.** A layout that looks perfect with curated seed data and breaks on real user content.

### 7.4.1 Control the shape and size

**Rule.** Never display user images at their intrinsic aspect ratio. Fix the container and crop.

**Why.** Intrinsic ratios **throw off the layout**, and the damage compounds with quantity — a grid of images at mixed ratios has no alignment anywhere. Fixing the container makes the layout independent of what users upload.

**How.** **Center the image inside a fixed container and crop out whatever doesn't fit.** Easy with CSS: make it a background image and set **`background-size: cover`**.

**Values.** None.

**Tailwind.** `<img class="w-full h-48 object-cover object-center">` — the modern equivalent, and preferable to a background image because it keeps the `alt` text. `object-cover` is `background-size: cover`.

**Fails as.** Card grids where every card is a different height; avatars stretched to squares; a profile header ruined by a panoramic upload.

### 7.4.2 Prevent background bleed

**Rule.** When an upload's background matches your UI background, the image loses its shape. Fix it with a **subtle inner box shadow** — not a border.

**Why.** A user uploading a white-background product photo onto your white card produces an image with no discernible edge; it bleeds into the surface and looks broken.

The reason the obvious fix is wrong: **borders often clash with the colors in the image**. A border is a hard line in a color you chose without knowing the image, and against some uploads it will fight. An inner shadow defines the edge without asserting a color — **most people will barely even realize the shadow is there**.

**How.** Subtle inner box shadow on the image container. If you dislike the slight inset look that produces, a **semi-transparent inner border** works well too — semi-transparent so it takes on the image's own colors rather than imposing one.

**Values.** None.

**Tailwind.** `shadow-inner` on the container, or `ring-1 ring-inset ring-black/5` for the semi-transparent variant. Both defeat bleed without committing to a color.

**Fails as.** Product grids where white-background photos have no edges; a solid grey border clashing with every second upload.

---

## Audit checklist for this lens

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

## Cross-references

- Text over images is a contrast problem → `05-color.md` §5.6
- Colorizing to match the palette → `05-color.md` §5.2.2
- Inner shadows and the light-from-above rule → `06-depth.md` §6.1.3
- Overlapping images and invisible borders → `06-depth.md` §6.5.1
- Icons as heavy elements needing contrast balance → `02-hierarchy.md` §2.7.1
- Illustrations in empty states → `08-finishing-touches.md` §8.4
