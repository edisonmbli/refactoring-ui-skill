# Example 3 — Empty state

The case where the correct fix is mostly **deletion**, which makes it a useful
counterweight to the assumption that an audit produces additions.

## Before

```html
<div>
  <div class="flex gap-2 border-b border-{neutral}-200 pb-2 mb-4">
    <button class="opacity-50" disabled>All</button>
    <button class="opacity-50" disabled>Active</button>
    <button class="opacity-50" disabled>Archived</button>
    <input class="ml-auto" placeholder="Search projects…" disabled>
  </div>
  <table class="w-full">
    <thead><tr class="text-left text-{neutral}-500">
      <th>Name</th><th>Owner</th><th>Updated</th>
    </tr></thead>
    <tbody></tbody>
  </table>
  <p class="text-center text-{neutral}-400 mt-8">No results found.</p>
</div>
```

## Findings

| # | Sev | Rule | Now | Proposed |
|---|---|---|---|---|
| 1 | **P0** | `§8.4` | Filters, search and table headers are rendered but disabled | **Hide them entirely.** They do nothing until content exists |
| 2 | P0 | `§8.4` | "No results found." is the whole state | Illustration, a clear line, and an emphasized CTA |
| 3 | P1 | `§8.4` | No call to action at all — the user cannot proceed | The CTA is this screen's primary action |
| 4 | P1 | `§2.2.a` | `text-{neutral}-400` on the only message on screen | This is primary content here, not tertiary |
| 5 | P1 | `§4.8.2` | Table headers are not the problem; the disabled toolbar is | (rolled into 1) |

Finding 1 is the one people miss. A disabled filter bar is **worse** than no filter
bar: it adds visual noise, states the emptiness a second time, and presents a row
of controls that cannot be used. "No results found" also mis-describes the
situation — there are no results because nothing has been created yet, which is a
different message with a different next step.

The empty state is the only state **every** user is guaranteed to see. That is why
this sits at P0 despite living in the Finishing Touches chapter.

## After

```html
<div class="text-center py-12">
  <div class="w-16 h-16 mx-auto rounded-full bg-{primary}-100 grid place-items-center">
    <FolderIcon class="w-8 h-8 text-{primary}-600" aria-hidden="true" />
  </div>
  <p class="mt-4 text-lg font-semibold text-{neutral}-900">No projects yet</p>
  <p class="mt-1 text-{neutral}-600">Create your first project to get started.</p>
  <button class="mt-6 px-4 py-2 rounded-md bg-{primary}-600 text-white font-medium">
    New project
  </button>
</div>
```

**What changed and why:**

- Toolbar and table removed from the DOM, not disabled. `§8.4`
- Icon kept at its intended size inside a larger shape — **not scaled to 64px**. `§7.3.1`
- `mt-1` binds the two lines, `mt-4` and `mt-6` separate the blocks. `§3.6`
- Centering is correct here: short, independent blocks. `§4.7.1`
- The message is primary content and takes a primary text color. `§2.2.a`

## Eval expectations

A correct audit of the "before" surfaces at minimum: the disabled-control finding
(`§8.4`), the missing CTA (`§8.4`), and the tertiary color on primary content
(`§2.2.a`). An audit that only proposes "add an illustration" has missed the point.
