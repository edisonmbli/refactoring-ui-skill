# Creating Depth

> Covers matrix rows **6.1 – 6.5.1** (17 items). Book chapter: *Creating Depth*.
> Six-part shape per rule: **Rule · Why · How · Values · Tailwind · Fails as**.

**Notation.** In `Values`, **bold numbers are the book's invariants** and apply as written; unbolded values are illustrative. In `Tailwind`, `{primary}` / `{neutral}` / `{danger}` are placeholders for the project's own ramps. Full convention in `SKILL.md` → *Reading the reference files*.

Fifth lens in the sweep. Depth comes after color because most depth techniques are color decisions in disguise — a shadow is a dark color, a raised edge is a light one, and §6.4.1 is purely a color relationship. Auditing depth before the palette is settled produces findings that the palette work then invalidates.

Nearly all of this chapter follows from **one** physical rule, §6.1.1. Learn that and the rest is derivation.

---

## 6.1 Emulate a light source

**Rule.** Depth in an interface comes from mimicking how light interacts with real objects. It is one rule, not a collection of effects.

**Why.** Elements that feel raised off the page or inset into it look like they required elaborate technique. They don't — they require understanding a single fundamental about light direction, after which every raised or inset treatment is derivable rather than memorized.

**How.** Determine the **profile** you want the element to have, then mimic how a light source would interact with that shape. §6.1.2 and §6.1.3 work the two standard profiles.

**Values.** None.

**Tailwind.** —

**Fails as.** Shadows and highlights applied by imitation, producing elements that are lit inconsistently within one interface.

### 6.1.1 Light comes from above

**Rule.** Light comes from above. Every depth cue follows from that single fact.

**Why.** The real-world reference makes it obvious. On a panelled door, the panels read as raised even in a flat photograph — because the top edge is lighter, being angled toward the sky and catching more light, while the bottom edge is darker, being angled away and catching less. The only physical arrangement that produces those edges is a raised panel, so that is what the brain perceives.

A cabinet with inset panels shows the inverse: a shadow at the top, because the lip above blocks the light, and a lighter bottom edge, because it is angled upward toward the sky. Same lighting, opposite geometry, opposite cues.

Interfaces work identically because the perceptual system is the same one. This is why depth cues cannot be applied arbitrarily — a light bottom edge with a shadow above it *means* inset, and applying it to something meant to be raised produces an element that reads as wrong without an identifiable cause.

**How.**
- **Raised** — top edge lighter, bottom edge darker, shadow cast below.
- **Inset** — shadow at the top, bottom edge lighter.

**Values.** None. **Light from above** is the invariant.

**Tailwind.** Every default shadow utility has a positive Y offset. That is this rule, and it's why shadows with negative or zero Y offset look wrong outside deliberate special cases.

**Fails as.** Shadows offset upward or sideways; a "raised" card with a light bottom edge; inconsistent light direction across components.

### 6.1.2 Raised elements

**Rule.** For a raised element with flat top and bottom edges: reveal the top edge, hide the bottom, and cast a small sharp shadow below.

**Why.** The reasoning is geometric. With both edges flat, it's physically impossible to see both at once. **People generally look slightly downward at their screens**, so the natural view reveals the top edge and hides the bottom. Rendering both — a light top edge *and* a visible bottom edge — depicts an impossible object.

The top edge faces upward, so it catches more light and is lighter than the button's face. Then, because a raised element blocks light from reaching the area beneath it, there's a shadow below.

**How.**

1. **Light the top edge.** A top border or an inset box shadow with a slight vertical offset, slightly lighter than the face.
2. **Choose that lighter color by hand.** Don't use semi-transparent white — **overlaying white sucks the saturation out of the underlying color**. Same failure as `02-hierarchy.md` §2.3.a, same fix.
3. **Cast a shadow below.** A small dark box shadow with a slight vertical offset, so it appears only below the element.
4. **Keep the blur tight.** A couple of pixels is plenty; these shadows should have **fairly sharp edges** — look at the shadow cast by the bottom of a wall outlet or a window frame.

**Values.** Blur: **a couple of pixels**. Vertical offset: slight, positive. Both edges visible simultaneously: **impossible, never render both**.

**Tailwind.** `shadow-sm` with an inset highlight via `ring-1 ring-inset` in a hand-picked light color, or a `border-t` one step lighter than the face. Not `bg-white/20`.

**Fails as.** Buttons with large soft shadows that float rather than sit; raised elements whose highlight is desaturated white, making the fill look faded.

### 6.1.3 Inset elements

**Rule.** For an element recessed into the page: light the bottom lip and shadow the top.

**Why.** Same reasoning inverted. Looking slightly downward at a well, **only the bottom lip is visible** — and it faces toward the sky, so it is lighter. The area above the well blocks light from reaching the top of the recess, so there is a shadow there.

**How.**

1. **Light the bottom lip.** A bottom border, or an inset shadow with a **negative** vertical offset.
2. **Shadow the top.** A small dark inset box shadow with a **positive** vertical offset — positive so the shadow sits at the top and doesn't poke through at the bottom.

This treatment applies to anything that should read as recessed: wells, **text inputs**, and **checkboxes**.

**Values.** Bottom lip: negative vertical offset. Top shadow: **positive** vertical offset.

**Tailwind.** `shadow-inner` plus a `border-b` one step lighter. Note the sign convention differs from raised elements — this is the most common place to get depth backwards.

**Fails as.** Text inputs that read as raised rather than recessed; wells with the shadow on the wrong edge, which registers as wrong without being identifiable.

### 6.1.4 Don't get carried away

**Rule.** Borrow visual cues from the real world. Don't pursue photo-realism.

**Why.** Once the simulation is understood it's tempting to keep tuning, and the exercise is genuinely fun — but in practice it produces interfaces that are **busy and unclear**. Depth is a tool for communicating relationships, and past a certain fidelity it stops communicating and starts decorating.

**How.** Use the minimum depth that conveys the relationship. Stop there.

**Values.** None.

**Tailwind.** —

**Fails as.** Skeuomorphic detailing that adds nothing; elements with four stacked shadows and two gradients to simulate a material nobody needed identified.

---

## 6.2 Use shadows to convey elevation

**Rule.** Shadows position elements on a virtual z-axis. Use them to express elevation, not as decoration.

**Why.** Shadow size and blur read directly as distance: **small shadows with a tight blur** make an element feel only slightly raised, **larger shadows with a higher blur** make it feel much closer to the user. And that reads as importance — **the closer something feels to the user, the more it attracts their focus**. So elevation is a hierarchy lever, and picking shadows by appearance rather than by intended z-position wastes it.

**How.** Decide where the element should sit on the z-axis, then assign the shadow that expresses it. Never the reverse.

**Values.** Small/tight = slightly raised. Large/blurred = close to the user.

**Tailwind.** `shadow-sm` … `shadow-2xl` is a z-axis, not a set of styles.

**Fails as.** Every card carrying the same shadow regardless of role; a modal with the same elevation as a button.

### 6.2.a The three canonical uses

**Rule.** Three reference points anchor the scale.

**Why.** They map the abstract z-axis onto decisions people actually make, and they're chosen because the required focus differs at each level.

**How.**
- **Small** — buttons. Noticed, but not dominating the page.
- **Medium** — dropdowns. Sitting a bit further above the rest of the UI.
- **Large** — modal dialogs. Where you really want to capture attention.

**Values.** None.

**Tailwind.** `shadow-sm` on buttons, `shadow-md`/`shadow-lg` on dropdowns and popovers, `shadow-2xl` on modals.

**Fails as.** Dropdowns that look glued to the page; modals that don't separate from the content behind them.

### 6.2.1 Establishing an elevation system

**Rule.** Define a fixed set of shadows. **Five is plenty.**

**Why.** Same argument as every other system in the book (`01-starting-from-scratch.md` §1.5): a fixed set removes the unanswerable question and produces consistency for free. Five is enough because there are only so many meaningfully distinct z-positions in an interface — beyond that the differences stop being perceptible and reintroduce the problem.

**How.** Define the smallest and largest shadow, then fill the middle with shadows that increase **fairly linearly**. Note this differs from color and spacing, which bisect proportionally — elevation increases linearly.

**Values.** The book's five-step scale, all at `hsla(0, 0%, 0%, .2)`:

```
0 1px 3px    hsla(0,0%,0%,.2)
0 4px 6px    hsla(0,0%,0%,.2)
0 5px 15px   hsla(0,0%,0%,.2)
0 10px 24px  hsla(0,0%,0%,.2)
0 15px 35px  hsla(0,0%,0%,.2)
```

**Five levels.** Every value has a **zero horizontal offset** — light from directly above (§6.1.1).

**Tailwind.** Maps onto `shadow-sm` / `shadow` / `shadow-md` / `shadow-lg` / `shadow-xl` / `shadow-2xl`. Tailwind's defaults use the two-part construction from §6.3, which the book's single-shadow scale above does not — both are valid; §6.3 is the refinement.

**Fails as.** Shadows written inline per component; twelve distinct shadow values across a codebase; a shadow with a horizontal offset that lights that one element from the side.

### 6.2.2 Combining shadows with interaction

**Rule.** Shadows communicate interaction state by moving elements on the z-axis.

**Why.** It makes state changes physically legible rather than merely conventional. Lifting a dragged item off the page communicates both that it's been picked up and that it can be moved — one cue doing two jobs.

**How.**
- **Dragging** — add a shadow when the user clicks an item in a sortable list. It pops forward above the others and makes draggability clear.
- **Pressing** — switch to a smaller shadow, or remove it entirely, so the button feels pressed into the page.

This also **solves the selection problem**: don't think about what the shadow should look like, think about where the element should sit on the z-axis, and assign accordingly.

**Values.** None.

**Tailwind.** `shadow-sm active:shadow-none` on buttons; `shadow-lg` applied to the dragged item.

**Fails as.** Buttons with no pressed state; drag interactions where the dragged item is indistinguishable from the list.

---

## 6.3 Shadows can have two parts

**Rule.** A two-shadow treatment is two shadows doing two different jobs — not random experimentation.

**Why.** Inspecting a well-made shadow often reveals two, and it looks like fiddling until you know what each is for. The physical basis: a real object casts a large soft shadow from the direct light source **and** sits in a small dark region underneath where even ambient light struggles to reach. Those are separate phenomena with different shapes, and a single CSS shadow cannot express both.

The payoff is control. With one shadow, making the near-edge definition crisp forces the whole shadow to be heavy. Splitting the jobs lets you keep the large shadow **subtle** while keeping the shadow near the element's edges **well defined**.

**How.** See §6.3.a.

**Values.** None.

**Tailwind.** Tailwind's default shadows are built this way — inspect `shadow-lg` and you'll find two comma-separated shadows.

**Fails as.** Single shadows that are either too heavy overall or too vague at the edges, with no setting that fixes both.

### 6.3.a The two jobs

**Rule.** One large soft shadow, one tight dark one.

**Why.** Each corresponds to a distinct physical effect, which is why the parameters differ the way they do.

**How.**
- **First shadow** — larger and softer, with a **considerable vertical offset and large blur radius**. Simulates the shadow cast behind an object by a direct light source.
- **Second shadow** — tighter and darker, with **less vertical offset and a smaller blur radius**. Simulates the shadowed area *underneath* the object, where ambient light has trouble reaching.

**Values.** Shadow 1: large offset, large blur, softer. Shadow 2: small offset, small blur, darker.

**Tailwind.** `box-shadow: 0 10px 20px rgb(0 0 0 / 0.15), 0 3px 6px rgb(0 0 0 / 0.10)` — the general shape.

**Fails as.** Two shadows with similar parameters, which is just one shadow rendered twice.

### 6.3.1 Accounting for elevation

**Rule.** As elevation increases, make the **tight** shadow more subtle.

**Why.** Physically grounded, and testable on your desk: as an object lifts away from a surface, the small dark contact shadow from absent ambient light fades. Holding it constant across elevations produces high shadows that look wrong — the object reads as both far from the surface and touching it.

**How.** The tight shadow should be **quite distinct at your lowest elevation** and **almost or completely invisible at your highest**. The large soft shadow grows over the same range.

**Values.** Tight shadow: distinct at lowest elevation → **almost or completely invisible** at highest.

**Tailwind.** Visible in Tailwind's own scale — the second shadow shrinks in relative weight from `shadow-sm` to `shadow-2xl`. Custom elevation scales must replicate it.

**Fails as.** A modal with a crisp contact shadow, making a supposedly floating element look pasted down.

---

## 6.4 Even flat designs can have depth

**Rule.** Flat design means no shadows or gradients — it does not mean no depth. Effective flat designs still convey depth by other means.

**Why.** "Flat" describes a rejection of effects that mimic real-world light, not a rejection of spatial relationships. Interfaces still need to communicate what's above what. Removing shadows removes one vocabulary, not the requirement.

**How.** §6.4.1 and §6.4.2.

**Values.** None.

**Tailwind.** —

**Fails as.** Flat interfaces where nothing has any spatial relationship and every surface reads at the same level.

### 6.4.1 Creating depth with color

**Rule.** Lighter elements feel closer; darker elements feel further away.

**Why.** Consistent with §6.1.1 — surfaces angled toward a light source above receive more light, so lightness reads as proximity. The relationship holds most reliably **between shades of the same color**, where lightness is the only variable.

**How.** Make an element **lighter than the background** to feel raised; **darker than the background** to feel inset like a well. This applies to non-flat designs too — color is another tool for conveying distance, usable alongside shadows rather than instead of them.

**Values.** None. Requires the ramp from `05-color.md` §5.3.

**Tailwind.** On a `bg-{neutral}-100` page, a `bg-white` card reads raised and a `bg-{neutral}-200` well reads inset. This is also the primary elevation mechanism in **dark mode**, where shadows are nearly invisible — see `15-beyond-the-book.md`.

**Fails as.** A dark-background interface using shadows for elevation, where nothing separates; cards the same color as their background, held apart by a border alone.

### 6.4.2 Using solid shadows

**Rule.** Short, vertically offset shadows with **no blur radius at all**.

**Why.** Zero blur reads as a graphic device rather than a simulation of light, so it lifts an element without breaking the flat aesthetic. It borrows the *position* cue from shadow language while discarding the *softness* that reads as realism.

**How.** Short offset, vertical only, **no blur**.

**Values.** **Zero blur radius.** Short vertical offset.

**Tailwind.** `shadow-[0_2px_0_0_var(--color-{neutral}-300)]`. One of the few justified arbitrary values, since the default scale is all blurred — better still, add it to the theme as a named elevation.

**Fails as.** A flat design with a soft-blurred shadow, which reads as an inconsistency rather than a choice.

---

## 6.5 Overlap elements to create layers

**Rule.** Overlapping elements is one of the most effective ways to create depth.

**Why.** Overlap is the strongest available depth cue because it's unambiguous: if A occludes B, A is in front. Unlike shadows it doesn't rely on lighting conventions, and unlike color it doesn't depend on relative lightness. It also produces layered composition, which reads as considered rather than as a stack of boxes.

**How.** Three patterns:
- **Cross a background transition** — offset a card so it straddles two different backgrounds, instead of containing it entirely within one.
- **Exceed the parent** — make an element taller than its parent so it overlaps on both sides.
- **Small components too** — carousel controls sitting over the edge of the carousel.

**Values.** None.

**Tailwind.** Negative margins (`-mt-16`) or `relative` positioning with `z-*`. Verify at mobile widths, where overlaps most often break.

**Fails as.** Landing pages of stacked full-width bands with no interlock; a section boundary that reads as a hard seam.

### 6.5.1 Overlapping images

**Rule.** Give overlapping images an "invisible border" that matches the background color.

**Why.** Overlapping images clash where they meet: two photographs with no separation produce a visually confusing junction, since neither has a defined edge against the other. A border in the background color creates a consistent gap, so the layering reads clearly — the appearance of layers with none of the clashing.

**How.** Border, matched to the background color, on each overlapping image.

**Values.** None.

**Tailwind.** `ring-4 ring-white` (or the actual background color) on stacked avatars — the standard avatar-group pattern, and this rule is its origin. Must track the background: a `ring-white` avatar stack on a grey section is visibly wrong.

**Fails as.** Avatar stacks that blur into one another; overlapping image galleries with muddy junctions.

---

## Audit checklist for this lens

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

## Cross-references

- Semi-transparent white desaturating the layer beneath → `02-hierarchy.md` §2.3.a
- Why five levels rather than an open set → `01-starting-from-scratch.md` §1.5.1
- The ramp that §6.4.1 depends on → `05-color.md` §5.3
- Shadows as an alternative to borders → `08-finishing-touches.md` §8.5.1
- Inner shadows preventing upload background bleed → `07-images.md` §7.4.2
- Elevation in dark mode, where shadows stop working → `15-beyond-the-book.md`
