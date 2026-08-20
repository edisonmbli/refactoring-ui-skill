# Example 2 — Form group

One finding that matters far more than the others, and a good illustration of why
`§3.6` is P0 rather than P1.

## Before

```html
<form class="space-y-4">
  <div>
    <label class="block mb-4 text-{neutral}-700">Email address</label>
    <input class="w-full px-3 py-2 border border-{neutral}-300 rounded shadow-lg">
  </div>
  <div>
    <label class="block mb-4 text-{neutral}-700">Password</label>
    <input class="w-full px-3 py-2 border border-{neutral}-300 rounded shadow-lg">
  </div>
  <button class="w-full py-2 bg-{primary}-600 text-white rounded">Sign in</button>
  <button class="w-full py-2 bg-{neutral}-600 text-white rounded">Cancel</button>
</form>
```

## Findings

| # | Sev | Rule | Now | Proposed |
|---|---|---|---|---|
| 1 | **P0** | `§3.6` | `mb-4` inside a group, `space-y-4` between groups — **identical** | Inner must be visibly smaller: `mb-1` inside, `mb-6` between |
| 2 | P1 | `§6.1.3` | Inputs carry an outer `shadow-lg` — they read as raised | Inputs are inset: `shadow-inner` |
| 3 | P1 | `§2.8` | Two full-width solid buttons — two primary actions | One primary; Cancel is tertiary |
| 4 | P2 | `§3.4.2` | Form is full-width | `max-w-md` — an input gains nothing from 900px |

Finding 1 is the whole example. With equal inner and outer spacing, each label sits
exactly as close to its own input as to the previous one, so grouping is genuinely
undetermined by the visual — the reader resolves it from content. In a login form
that is a password typed into a visible email field. **A spacing value is a
security-adjacent decision here**, which is why the rule is P0.

Finding 3 has a second-order effect: with Cancel as a solid button, a user
scanning for the primary action has to read both.

## After

```html
<form class="max-w-md">
  <div class="mb-6">
    <label class="block mb-1 text-sm font-medium text-{neutral}-700">Email address</label>
    <input type="email"
           class="w-full px-3 py-2 rounded border border-{neutral}-300 shadow-inner">
  </div>
  <div class="mb-6">
    <label class="block mb-1 text-sm font-medium text-{neutral}-700">Password</label>
    <input type="password"
           class="w-full px-3 py-2 rounded border border-{neutral}-300 shadow-inner">
  </div>
  <button class="w-full py-2 rounded bg-{primary}-600 text-white font-medium">Sign in</button>
  <button class="w-full py-2 mt-2 text-{neutral}-600 hover:underline">Cancel</button>
</form>
```

**Not changed:** the labels stay. `§2.5` is about displaying data, not about form
inputs — accessible labels are untouched by it, and removing them would be the
overcorrection listed in `14-antipatterns.md` Part 3.
