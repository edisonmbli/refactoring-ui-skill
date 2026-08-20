# Example 1 — Stat card

A single component, six findings. Good demonstration that most problems are
structural rather than stylistic.

## Before

```html
<div class="border border-{neutral}-300 rounded-lg p-4 shadow-lg text-center">
  <div class="text-2xl font-bold text-{neutral}-900">Monthly Revenue</div>
  <div class="text-sm text-{neutral}-400 mt-2">$48,200</div>
  <div class="text-sm text-green-500 mt-2">↑ 12.5%</div>
</div>
```

## Findings

| # | Sev | Rule | Now | Proposed |
|---|---|---|---|---|
| 1 | P0 | `§2.5.3` | Label is 24px bold; the value is 14px muted | Invert. The data is what matters, the label is supporting content |
| 2 | P1 | `§2.2` | Hierarchy carried by size alone | Use weight and color; keep sizes reasonable |
| 3 | P1 | `§8.5` | Border **and** shadow **and** a rounded panel — three separations, one job | Keep one. On a tinted page, the background difference alone is enough |
| 4 | P1 | `§6.2` | `shadow-lg` is modal-level elevation on a static card | `shadow-sm`. Elevation expresses z-position, not importance |
| 5 | P1 | `§3.6` | Uniform `mt-2` throughout — no grouping | Label and value are one unit; the trend is separate |
| 6 | P0 | `§5.7` | Trend direction is an arrow glyph plus color, but the color is doing the work | Keep an actual icon; make sure the sign reads without color |

Note finding 1 is P0, not cosmetic: a reader scanning a dashboard for numbers
finds words instead. The card fails at its only job.

## After

```html
<div class="bg-white rounded-lg p-6 shadow-sm">
  <div class="text-sm text-{neutral}-600">Monthly revenue</div>
  <div class="mt-1 text-3xl font-semibold text-{neutral}-900">$48,200</div>
  <div class="mt-3 flex items-baseline gap-1 text-sm text-{accent}-700">
    <TrendUpIcon class="w-4 h-4" aria-hidden="true" />12.5%
  </div>
</div>
```

**What changed and why:**

- Label demoted by size, contrast and weight together; value promoted. `§2.5.3`
- `mt-1` binds label to value, `mt-3` separates the trend — outer exceeds inner. `§3.6`
- One separation mechanism: background difference against a tinted page. `§8.5.2`
- `shadow-sm`, matching an actual card's elevation. `§6.2.a`
- `items-baseline`, since the row mixes sizes. `§4.4`
- Icon at `w-4` beside 14px text, one step softer in color. `§2.7.1`
- Text left-aligned; centering a multi-line block was never justified. `§4.7`
- `{accent}-700` rather than `-500`, so it clears 4.5:1 on white. `§5.6`

**Not changed:** the rounded corners. Radius is a personality decision (`§1.4.3`)
and the only requirement is consistency with the rest of the system.
