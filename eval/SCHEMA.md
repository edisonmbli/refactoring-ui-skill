# Gold-set schema

Each case is a folder:

```
eval/cases/<id>/
  index.html      # open in a browser; this is the surface under audit
  expected.json   # gold labels
```

## `expected.json`

| Field | Meaning |
|---|---|
| `id` | Stable case id, matches the folder name |
| `title` | Short name |
| `workflow` | Always `D` for this set (diagnose only) |
| `must` | **Required hits.** Missing any fails the case |
| `should` | Expected but **allowed miss**. Tracked, does not fail the case |
| `forbidden` | **False positives.** Citing these *as defects* fails the case |
| `pass_bar` | Human restatement of the must-set |

Each `must` / `should` item:

```json
{
  "rules": ["§2.8", "§2.8.a", "§2.8.1"],
  "severity": "P0",
  "severity_floor": "P1",
  "now": "what the fixture actually does",
  "notes": "any of the listed rule IDs counts as a hit"
}
```

- `rules` — OR-list. Citing **any one** counts.
- `severity` — gold severity. Scoring warns if the report is softer than `severity_floor`, but a hit still counts as long as the rule ID is present.
- Matching is on extracted rule tokens (`§2.8.1` ≠ `§2.8`). Put every acceptable citation in `rules`.

Each `forbidden` item:

```json
{
  "rules": ["§3.1", "§3.1.1"],
  "why": "density here is deliberate"
}
```

A forbidden rule ID appearing in a **finding table row** is a false positive. Mentioning the same rule in skip/“not a finding” prose does not count.

## Scoring

A case **passes** iff:

1. Every `must` item has a rule-ID hit
2. Zero `forbidden` hits

`should` recall is reported, not gated. Suite pass bar is documented in `README.md`.
