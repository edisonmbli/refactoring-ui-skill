# Coverage Matrix

Authoritative checklist mapping every rule in *Refactoring UI* to its home in this skill.
**No reference file is considered done until every row assigned to it is marked `done`.**

- **50** top-level rules, **101** sub-points → **151** total items.
  (The book's table of contents exposes 92 sub-points; 9 more are only stated in body prose — the `n.n.a` rows — and are tracked here so they can't be lost.)
- `HV` = the item carries hard numeric values that must survive verbatim (no rounding, no "simplifying").
- `TW` = the item has a direct Tailwind expression that belongs in `10-tailwind-mapping.md`.
- Status: `done` · `todo` · `omitted` (omissions require a stated reason in the ref file).

| Legend | |
|---|---|
| `§n.n` | top-level rule |
| `§n.n.n` | sub-point |

---

## Ch 1 — Starting from Scratch → `01-starting-from-scratch.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 1.1 | Start with a feature, not a layout | Design a real piece of functionality first; the shell (nav, container, logo) cannot be decided before features exist | | |done |
| 1.2 | Detail comes later | Defer typefaces, shadows, icons in early exploration; low fidelity on purpose (Sharpie test) | | |done |
| 1.2.1 | Hold the color | Design in grayscale first so spacing, contrast and size carry the hierarchy | | ✓ |done |
| 1.2.2 | Don't over-invest | Sketches are disposable; abandon them once the decision is made | | |done |
| 1.3 | Don't design too much | Don't design every feature and edge case up front | | |done |
| 1.3.1 | Work in cycles | Design simple → build real → iterate on the working thing → return to design | | |done |
| 1.3.2 | Be a pessimist | Never imply functionality you aren't ready to build; design the smallest shippable version | | |done |
| 1.4 | Choose a personality | Personality is set by concrete factors, not vibes | | |done |
| 1.4.1 | Font choice | Serif = elegant/classic; rounded sans = playful; neutral sans = plain/neutral | | ✓ |done |
| 1.4.2 | Color | Blue = safe/familiar; gold = expensive/sophisticated; pink = fun/not serious | | ✓ |done |
| 1.4.3 | Border radius | Small = neutral; large = playful; none = serious/formal. Must be consistent — never mix | | ✓ |done |
| 1.4.4 | Language | Word choice drives personality as much as any visual property | | |done |
| 1.4.5 | Deciding what you actually want | Look at sites your target audience already uses; don't copy direct competitors | | |done |
| 1.5 | Limit your choices | Unconstrained choice is paralysis; near-identical options can't be decided between | | |done |
| 1.5.1 | Define systems in advance | Pick 8–10 shades and a restrictive type scale ahead of time, not per-decision | ✓ | ✓ |done |
| 1.5.2 | Designing by process of elimination | Guess the middle, test the neighbours on each side, re-center if an outer wins | | |done |
| 1.5.3 | Systematize everything | Systems needed for: font size, font weight, line height, color, margin, padding, width, height, box shadow, border radius, border width, opacity | ✓ | ✓ |done |

## Ch 2 — Hierarchy is Everything → `02-hierarchy.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 2.1 | Not all elements are equal | Visual hierarchy is the highest-leverage tool for making something feel designed; it is independent of color scheme, font and layout | | | done |
| 2.2 | Size isn't everything | Over-relying on font size gives oversized primary and undersized secondary content; use weight and color instead | ✓ | ✓ | done |
| 2.2.a | (three text colors) | Dark = primary, grey = secondary, lighter grey = tertiary | ✓ | ✓ | done |
| 2.2.b | (two font weights) | 400/500 normal, 600/700 emphasis; never below 400 for UI text | ✓ | ✓ | done |
| 2.3 | Don't use grey text on colored backgrounds | The real mechanism is reduced contrast, not greyness; hand-pick a same-hue color with adjusted S/L | | ✓ | done |
| 2.3.a | (why not opacity) | White-at-lower-opacity looks washed out/disabled and lets patterned backgrounds bleed through the text | | ✓ | done |
| 2.4 | Emphasize by de-emphasizing | When the primary element won't stand out, soften its competitors instead of amplifying it | | ✓ | done |
| 2.4.a | (applies at section scale) | A competing sidebar can be fixed by removing its background, not by restyling the content | | ✓ | done |
| 2.5 | Labels are a last resort | Naive `label: value` gives every datum equal emphasis and blocks hierarchy | | | done |
| 2.5.1 | You might not need a label at all | Format (email, phone, price) or context often identifies the data by itself | | | done |
| 2.5.2 | Combine labels and values | "12 left in stock" over "In stock: 12"; "3 bedrooms" over "Bedrooms: 3" | | | done |
| 2.5.3 | Labels are secondary | When a label is genuinely needed, de-emphasize it: smaller, lower contrast, lighter weight, or a combination | | ✓ | done |
| 2.5.4 | When to emphasize a label | Invert only when the user scans *for the label* (spec tables); keep the value close behind, not buried | | ✓ | done |
| 2.6 | Separate visual hierarchy from document hierarchy | Choose elements semantically, style them for hierarchy; section titles often behave as labels and can be small or visually hidden | | ✓ | done |
| 2.7 | Balance weight and contrast | Emphasis tracks surface area — bold text covers more pixels in the same space | | | done |
| 2.7.1 | Using contrast to compensate for weight | Icons are heavy and can't change weight; lower their contrast to rebalance against adjacent text | | ✓ | done |
| 2.7.2 | Using weight to compensate for contrast | When a 1px border is too subtle but a darker color is too harsh, thicken the border instead | | ✓ | done |
| 2.8 | Semantics are secondary | Actions sit in a pyramid: one primary, a couple of secondary, a few tertiary | | ✓ | done |
| 2.8.a | (the three treatments) | Primary = solid high-contrast fill; secondary = outline or low-contrast fill; tertiary = styled as a link | | ✓ | done |
| 2.8.1 | Destructive actions | Severity ≠ prominence; demote destructive actions, then apply the loud treatment inside the confirmation step where it *is* primary | | ✓ | done |

## Ch 3 — Layout and Spacing → `03-layout-spacing.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 3.1 | Start with too much white space | Extra breathing room is the cheapest cleanup available | | ✓ |done |
| 3.1.1 | White space should be removed, not added | Adding until "not actively bad" undershoots; start excessive and subtract | | |done |
| 3.1.2 | Dense UIs have their place | Density must be a deliberate decision (dashboards), not the default | | |done |
| 3.2 | Establish a spacing and sizing system | Never nitpick 120px vs 125px; choose from a fixed set | | ✓ |done |
| 3.2.1 | A linear scale won't work | "Multiples of 4px" doesn't help; **no two adjacent values closer than ~25%** | ✓ | ✓ |done |
| 3.2.2 | Defining the system | Base 16px (divides well, browser default); packed at the low end, progressively wider apart. Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 640, 768 | ✓ | ✓ |done |
| 3.2.3 | Using the system | Pick from the scale; if not enough, the next value up is usually right | | ✓ |done |
| 3.3 | You don't have to fill the whole screen | Available canvas is not an obligation; 600px content stays 600px | ✓ | ✓ |done |
| 3.3.1 | Shrink the canvas | Design the mobile layout first on a ~400px canvas, then adapt upward | ✓ | ✓ |done |
| 3.3.2 | Thinking in columns | Split into columns rather than widening past the optimal width | | ✓ |done |
| 3.3.3 | Don't force it | Equally, don't cram into a small area if the content needs room | | |done |
| 3.4 | Grids are overrated | A grid is just constrained percentage widths; outsourcing every layout decision to it backfires | ✓ | ✓ |done |
| 3.4.1 | Not all elements should be fluid | Sidebars want a fixed width optimized for contents; the main area flexes and runs its own internal grid | ✓ | ✓ |done |
| 3.4.2 | Don't shrink an element until you need to | Give a max-width and shrink only below it — otherwise a card can be wider at medium than at large screens | ✓ | ✓ |done |
| 3.5 | Relative sizing doesn't scale | em-encoded relationships don't hold across screen sizes; **large elements must shrink faster than small ones** | ✓ | ✓ |done |
| 3.5.1 | Relationships within elements | Button padding shouldn't be em-derived; large buttons want disproportionately generous padding, small ones tighter | ✓ | ✓ |done |
| 3.6 | Avoid ambiguous spacing | Space *around* a group must exceed space *within* it — vertically and horizontally | | ✓ |done |
| 3.6.a | (the four manifestations) | Form label/input groups; headings above sections; bulleted lists vs line-height; horizontal component groups | | ✓ |done |

## Ch 4 — Designing Text → `04-typography.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 4.1 | Establish a type scale | Unsystematic sizes cause inconsistency and slow the workflow | | ✓ |done |
| 4.1.1 | Choosing a scale | A linear scale fails here too; small jumps matter at the bottom, not at the top | | |done |
| 4.1.1a | Modular scales | Ratios: 4:5 major third, 2:3 perfect fifth, 1:1.618 golden; applied compounding from a 16px base | ✓ | |done |
| 4.1.1b | You end up with fractional values | 31.25 / 39.063 / 48.828px; subpixel rounding differs per browser — round manually if used | ✓ | |done |
| 4.1.1c | You usually need more sizes | Rounded 3:4 gives 12/16/21/28 — you'll want sizes between 12–16 and 16–21; tightening the ratio just reverse-engineers a scale you already knew | ✓ | |done |
| 4.1.1d | Hand-crafted scales | Recommended scale: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72 | ✓ | ✓ |done |
| 4.1.2 | Avoid em units | em compounds in nested elements (1.25em → .875em = 17.5px, off-scale); use px or rem | ✓ | ✓ |done |
| 4.2 | Use good fonts | Judging typefaces takes years; use shortcuts in the meantime | | |done |
| 4.2.1 | Play it safe | Neutral sans-serif; system font stack: `-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue` | ✓ | ✓ |done |
| 4.2.2 | Ignore typefaces with less than five weights | Filter font directories to 10+ styles (weights × italics) — removes ~85% of Google Fonts, leaving <50 sans-serifs | ✓ | |done |
| 4.2.3 | Optimize for legibility | Headline faces = tight letter-spacing + short x-height; text faces = wider spacing + tall x-height. Avoid condensed/short-x-height for UI body text | | |done |
| 4.2.4 | Trust the wisdom of the crowd | Sort by popularity; especially useful for non-neutral choices like a serif with personality | | |done |
| 4.2.5 | Steal from people who care | Inspect typefaces on sites you admire | | |done |
| 4.2.6 | Developing your intuition | Taste accrues from deliberate attention | | |done |
| 4.3 | Keep your line length in check | **45–75 characters per line**; on the web use em: **20–35em**. Beyond 75 is risky territory | ✓ | ✓ |done |
| 4.3.1 | Dealing with wider content | Constrain paragraph width even when the surrounding content area must be wider for images/components | | ✓ |done |
| 4.4 | Baseline, not center | Align mixed font sizes on one line by baseline, not vertical center; the mismatch is most visible when the text is close together | | ✓ |done |
| 4.5 | Line-height is proportional | The 1.5 rule of thumb is not universal | ✓ | ✓ |done |
| 4.5.1 | Accounting for line length | Line-height and paragraph width are **proportional**: narrow ≈1.5, wide up to 2 | ✓ | ✓ |done |
| 4.5.2 | Accounting for font size | Line-height and font size are **inversely** proportional; large headlines can sit at 1 | ✓ | ✓ |done |
| 4.6 | Not every link needs a color | Paragraph-link treatment is overbearing in link-dense UI; use heavier weight or darker color, or reveal underline/color on hover only for ancillary links | | ✓ |done |
| 4.7 | Align with readability in mind | Align to the language direction — left for English | | ✓ |done |
| 4.7.1 | Don't center long form text | Centering works for headlines and short blocks; past 2–3 lines, left-align. Prefer rewriting shorter over breaking the alignment | ✓ | ✓ |done |
| 4.7.2 | Right-align numbers | Aligned decimal positions make columns comparable at a glance | | ✓ |done |
| 4.7.3 | Hyphenate justified text | Justification without hyphenation creates word gaps; enable both together | | ✓ |done |
| 4.8 | Use letter-spacing effectively | Default: trust the type designer and leave it alone | | ✓ |done |
| 4.8.1 | Tightening headlines | Tighten a text-optimized family (e.g. Open Sans) when used for headlines; never loosen a headline face to make it work small | | ✓ |done |
| 4.8.2 | Improving all-caps legibility | Lowercase has x-height/ascender/descender variety; all-caps has none, so increase letter-spacing | | ✓ |done |

## Ch 5 — Working with Color → `05-color.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 5.1 | Ditch hex for HSL | Hex/RGB make visually-related colors look unrelated in code | | ✓ |done |
| 5.1.a | (the three components) | Hue = position on the wheel, in degrees: 0° red, 120° green, 240° blue. Saturation: 0% grey → 100% vivid; at 0% hue is irrelevant. Lightness: 0% black, 100% white, 50% pure hue | ✓ | |done |
| 5.1.1 | HSL vs. HSB | HSB 0% brightness is always black, but 100% brightness is only white at 0% saturation; HSB 100/100 = HSL 100% saturation at **50%** lightness. Design tools favor HSB, browsers only take HSL | ✓ | |done |
| 5.2 | You need more colors than you think | Five-hex palette generators can't build a real interface | | |done |
| 5.2.1 | Greys | Almost everything in a UI is grey; **8–10 shades**; start from a very dark grey, not true black | ✓ | ✓ |done |
| 5.2.2 | Primary color(s) | One, maybe two; **5–10 shades**; ultra-light for tinted backgrounds, dark for text | ✓ | ✓ |done |
| 5.2.3 | Accent colors | Attention colors (yellow/pink/teal) plus semantic states (red destructive, yellow warning, green positive); more if colors must categorize data. **Up to ~10 colors × 5–10 shades** for a complex UI | ✓ | ✓ |done |
| 5.3 | Define your shades up front | Never generate shades on the fly with `lighten()`/`darken()` — that's how you get 35 near-identical blues | | ✓ |done |
| 5.3.1 | Choose the base color first | Pick the middle shade; rule of thumb — one that works as a button background. No "start at 50% lightness" rule exists | | |done |
| 5.3.2 | Finding the edges | Darkest is usually text, lightest is usually a tinted background; an alert component exercises both. Match the base hue, then tune S/L | | |done |
| 5.3.3 | Filling in the gaps | ≥5 shades, ~10 preferred. Nine divides well: darkest **900**, base **500**, lightest **100** → fill **700/300** as midpoints → then **800/600/400/200** | ✓ | ✓ |done |
| 5.3.4 | What about greys? | Same procedure, base matters less. Darkest = darkest text; lightest = a subtle off-white background | | ✓ |done |
| 5.3.5 | It's not a science | Trust your eyes over the math and tweak; but resist *adding new shades* or the system is meaningless | | |done |
| 5.4 | Don't let lightness kill your saturation | Near 0%/100% lightness, saturation weakens; **increase saturation as lightness moves away from 50%** or shades look washed out | ✓ | ✓ |done |
| 5.4.1 | Use perceived brightness to your advantage | Perceived brightness = `√(0.299r² + 0.587g² + 0.114b²) / 255`. Three local minima (red, green, blue) and three maxima (yellow, cyan, magenta) — not linear around the wheel | ✓ | |done |
| 5.4.2 | Changing brightness by rotating hue | Lighten → rotate toward the nearest of **60°/180°/300°**; darken → toward **0°/120°/240°**. Preserves intensity where changing lightness washes it out. **Never rotate more than 20–30°** | ✓ | ✓ |done |
| 5.5 | Greys don't have to be grey | True grey is 0% saturation; most "greys" in good UI are noticeably saturated | | ✓ |done |
| 5.5.1 | Color temperature | Saturate with blue for cool, yellow/orange for warm; raise saturation at both ends of the ramp or the extremes wash out | | ✓ |done |
| 5.6 | Accessible doesn't have to mean ugly | WCAG: **4.5:1** for normal text (under ~18px), **3:1** for large text | ✓ | ✓ |done |
| 5.6.1 | Flipping the contrast | White-on-color needs surprisingly dark backgrounds, which then dominate the page; invert to dark-colored text on a light-colored background | | ✓ |done |
| 5.6.2 | Rotating the hue | For colored text on a colored background, raise contrast by rotating toward a brighter hue (cyan/magenta/yellow) instead of approaching white | | ✓ |done |
| 5.7 | Don't rely on color alone | Red-green colorblind users can't read color-only signals; add a supporting signal such as directional icons. For multi-series graphs, differentiate by **contrast** rather than distinct hues. Color supports, never carries | | ✓ |done |

## Ch 6 — Creating Depth → `06-depth.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 6.1 | Emulate a light source | Depth is one rule, not a bag of effects | | |done |
| 6.1.1 | Light comes from above | Raised: top edge lighter (angled toward sky), bottom edge darker. Inset: shadow at top (lip blocks light), bottom edge lighter | | ✓ |done |
| 6.1.2 | Raised elements | Both flat edges can't be visible at once; people look slightly downward, so reveal the top edge and hide the bottom. Lighter top border or inset shadow with slight vertical offset — **hand-pick the lighter color, don't overlay semi-transparent white** (it desaturates). Then a small dark shadow below with a slight vertical offset and **a blur of only a couple of pixels** — sharp edges | ✓ | ✓ |done |
| 6.1.3 | Inset elements | Bottom lip visible and facing the sky → lighter bottom border or inset shadow with negative vertical offset; plus a small dark inset shadow with positive vertical offset at the top. Applies to inputs and checkboxes | | ✓ |done |
| 6.1.4 | Don't get carried away | Borrow real-world cues; don't chase photo-realism — it makes interfaces busy and unclear | | |done |
| 6.2 | Use shadows to convey elevation | Shadows position elements on a z-axis; tight blur = slightly raised, large blur = close to the user. Closer attracts more focus | | ✓ |done |
| 6.2.a | (the three canonical uses) | Small = buttons (noticed, not dominant); medium = dropdowns; large = modals | | ✓ |done |
| 6.2.1 | Establishing an elevation system | **Five shadows is plenty.** Define smallest and largest, fill in roughly linearly: `0 1px 3px`, `0 4px 6px`, `0 5px 15px`, `0 10px 24px`, `0 15px 35px`, all `hsla(0,0%,0%,.2)` | ✓ | ✓ |done |
| 6.2.2 | Combining shadows with interaction | Raise a dragged list item on click; press a button in by shrinking or removing its shadow. Choose by intended z-position, not by how the shadow looks | | ✓ |done |
| 6.3 | Shadows can have two parts | Two shadows do two distinct jobs, not random experimentation | | ✓ |done |
| 6.3.a | (the two jobs) | #1 larger and softer — considerable vertical offset, large blur — the cast shadow from a direct light source. #2 tighter and darker — less offset, smaller blur — the ambient-occlusion band directly under the object | | ✓ |done |
| 6.3.1 | Accounting for elevation | The tight ambient shadow fades as an object rises: distinct at the lowest elevation, almost or completely invisible at the highest | | ✓ |done |
| 6.4 | Even flat designs can have depth | Flat = no shadows/gradients, but effective flat design still conveys depth | | |done |
| 6.4.1 | Creating depth with color | Lighter than the background reads as raised; darker reads as inset. Applies to non-flat designs too | | ✓ |done |
| 6.4.2 | Using solid shadows | Short, vertically offset, **zero blur** — lifts a card or button while keeping the flat aesthetic | | ✓ |done |
| 6.5 | Overlap elements to create layers | Offset a card across a background transition, or make an element taller than its parent so it overlaps both sides; works for small controls (carousel arrows) too | | ✓ |done |
| 6.5.1 | Overlapping images | Give overlapping images an "invisible border" matching the background color so they never clash | | ✓ |done |

## Ch 7 — Working with Images → `07-images.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 7.1 | Use good photos | Bad photos ruin an otherwise good design. Hire a professional for specific needs, or use quality stock (e.g. Unsplash). Never design with placeholders intending to swap in phone photos later | | |done |
| 7.2 | Text needs consistent contrast | The problem is the image, not the text color | | ✓ |done |
| 7.2.1 | The problem with background images | Photos are dynamic — light text dies in light areas, dark text dies in dark areas. Reduce the image's dynamics | | |done |
| 7.2.2 | Add an overlay | Semi-transparent overlay: black tones down light areas for light text; white brightens dark areas for dark text | | ✓ |done |
| 7.2.3 | Lower the image contrast | More control than an overlay (which affects the whole image); adjust brightness afterward to compensate | | ✓ |done |
| 7.2.4 | Colorize the image | Three steps: lower contrast → desaturate → solid fill in **multiply** blend mode. Also aligns photography with brand colors | | ✓ |done |
| 7.2.5 | Add a text shadow | Preserves image dynamics; **large blur radius, no offset** — a glow, not a shadow. Combine with a smaller contrast reduction | | ✓ |done |
| 7.3 | Everything has an intended size | Upscaling bitmaps is obviously bad — but that's not the only scaling failure | | |done |
| 7.3.1 | Don't scale up icons | Vector doesn't degrade, but 16–24px icons at 3–4× look chunky and detail-poor. Fix: enclose the icon at its intended size inside a larger shape with a background color | ✓ | ✓ |done |
| 7.3.2 | Don't scale down screenshots | Shrinking 70% crams detail into nothing (16px text → 4px). Fix: screenshot at a smaller viewport (tablet), take a partial screenshot, or draw a simplified UI with text replaced by lines | ✓ | |done |
| 7.3.3 | Don't scale down icons, either | Large-drawn icons turn to mush when shrunk — favicons worst of all. Redraw a simplified version at the target size | ✓ | |done |
| 7.4 | Beware user-uploaded content | You lose control of contrast, color and crop | | |done |
| 7.4.1 | Control the shape and size | Intrinsic aspect ratios wreck layouts; center inside fixed containers and crop the overflow — `background-size: cover` | | ✓ |done |
| 7.4.2 | Prevent background bleed | When an upload's background matches yours, the image loses its shape. Use a subtle **inner** box shadow, or a semi-transparent inner border — not a solid border, which clashes with image colors | | ✓ |done |

## Ch 8 — Finishing Touches → `08-finishing-touches.md`

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 8.1 | Supercharge the defaults | Liven up what's already on the page instead of adding elements: icons as list bullets (checkmarks/arrows generically, topical icons where they fit), promoted quote marks in testimonials, custom link styling (weight/color, or a thick overlapping underline), custom checkboxes and radios in a brand color | | ✓ |done |
| 8.2 | Add color with accent borders | A colored rectangle needs no graphic-design talent: across the top of a card, on active nav items, along the side of an alert, as a short underline beneath a headline, across the top of the whole layout | | ✓ |done |
| 8.3 | Decorate your backgrounds | Break up monotony without redesigning | | ✓ |done |
| 8.3.1 | Change the background color | Emphasize a panel or distinguish page sections; for energy use a slight gradient with **two hues no more than ~30° apart** | ✓ | ✓ |done |
| 8.3.2 | Use a repeating pattern | Subtle repeatable patterns (e.g. Hero Patterns); can repeat along a single edge instead of the full background. **Keep pattern/background contrast low** | | ✓ |done |
| 8.3.3 | Add a simple shape or illustration | Geometric shapes, small chunks of a pattern, or something like a simplified world map; keep contrast low | | ✓ |done |
| 8.4 | Don't overlook empty states | The empty state is the user's *first* interaction with a feature, and must be designed with it — not after. Add an image/illustration, emphasize the CTA, and **hide supporting UI (tabs, filters) that does nothing until content exists** | | ✓ |done |
| 8.5 | Use fewer borders | Borders work but stack up into clutter; reach for an alternative first | | ✓ |done |
| 8.5.1 | Use a box shadow | Outlines like a border but more subtle; works best when the element differs in color from the background | | ✓ |done |
| 8.5.2 | Use two different background colors | Usually sufficient on its own; if you already have both a color difference and a border, drop the border | | ✓ |done |
| 8.5.3 | Add extra spacing | Separation by distance — no new UI introduced at all | | ✓ |done |
| 8.6 | Think outside the box | Preconceptions about component appearance are not constraints: dropdowns can have sections, multiple columns, supporting text and colorful icons; table columns can be merged for hierarchy and can hold images and color; radio groups can become selectable cards | | ✓ |done |

## Ch 9 — Leveling Up → folded into `SKILL.md` (Continuous Improvement)

| ID | Book section | Core assertion | HV | TW | Status |
|---|---|---|---|---|---|
| 9.1 | Leveling up | Two durable practices for continued growth | | | done |
| 9.1.1 | Look for decisions you wouldn't have made | On any design you like, ask what the designer did that you'd never have thought to do (inverted datepicker background, a button inside a text input, two font colors in one headline) | | | done |
| 9.1.2 | Rebuild your favorite interfaces | Recreate designs from scratch **without opening devtools** — the discrepancies teach the details (tighter heading line-height, letter-spaced uppercase, layered shadows) | | | done |

---

## Synthesized references (not book chapters)

These carry no coverage obligation of their own; they aggregate the rows marked `TW` or extend beyond the book.

| Ref | Draws from | Purpose |
|---|---|---|
| `10-tailwind-mapping.md` | every `TW` row above | One Tailwind expression per rule; v3 and v4 |
| `11-design-tokens.md` | 1.5.x, 3.2.x, 4.1.x, 5.1–5.6, 6.2.1, 1.4.3 | Interview script + generation algorithm + output contract |
| `12-component-recipes.md` | 2.8, 6.1.2, 6.1.3, 6.2, 8.1, 8.4, 8.6, 3.6 | Buttons, cards, form groups, tables, dropdowns, modals, alerts, empty states |
| `13-audit-rubric.md` | all chapters | Severity model, finding schema, seven-lens sweep order |
| `14-antipatterns.md` | all chapters | Symptom → diagnosis → rule ID, incl. the AI-generated-UI failure set |
| `15-beyond-the-book.md` | — | Explicitly marked extensions: dark mode, focus states, target sizes, motion, breakpoints, z-index, semantic token naming |

## Deliberate omissions

| ID | Reason |
|---|---|
| — | none yet |
