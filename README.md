# Refactoring UI — a Claude Skill

**A design rulebook and diagnostic layer for web UI**, distilled from
[*Refactoring UI*](https://www.refactoringui.com) by Adam Wathan & Steve Schoger
into something an AI coding agent can actually apply.

> ⚠️ **Unofficial and independent.** Not affiliated with, endorsed by, or reviewed
> by the book's authors, and not a substitute for reading it —
> [buy it](https://www.refactoringui.com), it's excellent.
> See [ATTRIBUTION.md](ATTRIBUTION.md).

**[中文文档 →](README.zh-CN.md)**

---

## The problem

AI coding agents write competent HTML and CSS, and produce interfaces that look
*off*. Not broken — off.

Everything centered. One spacing value everywhere. Indigo primary on a brand that
isn't indigo. A blue-to-pink gradient. Every action a filled button. No empty
state.

Each of those is a locally defensible decision. **Generation is local; design is
global.** That gap is what a rulebook closes.

## What this is

Most AI design tooling **generates**: describe an interface, receive one. This does
the opposite job — it's the **constraint and diagnosis** layer. The rulebook and
the reviewer, not the stylist.

So it composes with the generators instead of competing with them: hand a design
tool the constraints *before* it runs, audit its output *after*, or run the build
workflow on its own when there's no generator in play.

Why this book in particular: it's a rules book, not an inspiration book. Nearly
every page is *symptom → mechanism → specific fix → concrete number*. And its
author went on to write Tailwind CSS, so the path from principle to code is
unusually short — the book's type scale, spacing scale and color ramps **are**
Tailwind's defaults.

This encodes all of it: **151 rules**, every one traceable, none dropped.

## What it looks like

> *"Have a look at this settings page — something feels off but I can't tell what."*

It detects your stack, renders the page at desktop and mobile widths, then sweeps
seven lenses in a fixed order: **hierarchy → spacing → typography → color → depth →
images → finishing**. The order is causal — hierarchy problems change what counts
as a spacing problem, and spacing fixes routinely dissolve the "should this have a
border" question entirely.

What comes back is severity-ranked, and **every finding cites a rule**:

| Sev | Rule | Now | Proposed |
|---|---|---|---|
| P0 | §3.6 | Label spacing equals group spacing — the label is equidistant from its own input and the next one | `mb-1` inside, `mb-6` between |
| P1 | §2.8 | Three primary-styled buttons | One primary; outline and link for the rest |
| P1 | §6.2 | `shadow-lg` on static cards | `shadow-sm` — elevation is z-position, not importance |

Then a **Systemic** section, which is where it earns its keep: twelve "off-scale
spacing" findings are *one* finding — there is no spacing scale.

No rule ID, no finding. If it can't name the rule, it's an opinion, and opinions
get dropped.

## Install

```
/plugin marketplace add edisonmbli/refactoring-ui-skill
/plugin install refactoring-ui
```

That's it — no registry, nothing uploaded. `marketplace add` clones this repo and
reads `.claude-plugin/marketplace.json`; `install` loads what it finds under the
conventional directories. Updating is `git pull` wearing a different name:
`/plugin marketplace update refactoring-ui`.

Scripts want **Python 3.9+** and no packages. Without Python everything still
works — the palette algorithm is documented as a hand-executable procedure.

<details>
<summary><b>Other ways to install — plain skill, and non-Claude-Code agents</b></summary>

### Claude Code, as a plain skill

```bash
git clone https://github.com/edisonmbli/refactoring-ui-skill.git

cp -r refactoring-ui-skill/skills/refactoring-ui ~/.claude/skills/   # personal
cp -r refactoring-ui-skill/skills/refactoring-ui .claude/skills/     # project
```

### Any other coding agent

The plugin mechanism is Claude Code's. **The skill is not** — it's plain Markdown,
built as *an index plus references loaded on demand*, which any file-reading agent
can follow. It just has to be told once.

Put the skill somewhere stable:

```bash
git clone https://github.com/edisonmbli/refactoring-ui-skill.git .refactoring-ui
```

Then add this to whichever instruction file your agent already reads:

```markdown
## Design work

When the task involves building, changing, or reviewing any user interface,
read `.refactoring-ui/skills/refactoring-ui/SKILL.md` FIRST and follow its
routing table. It names which file under `references/` to load for the task
at hand — load them on demand, one at a time. Do not read the whole
references/ directory; the progressive loading is the design.
```

| Agent | File |
|---|---|
| **OpenAI Codex** | `AGENTS.md` at the repo root |
| **Cursor** | `.cursor/rules/design.mdc` (add `description:` frontmatter), or `AGENTS.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Windsurf** | `.windsurf/rules/design.md` |
| **Cline / Roo** | `.clinerules/design.md` |
| **Aider** | `CONVENTIONS.md`, passed with `--read` |
| **Anything else** | Whatever it reads at session start — or paste the snippet into the chat |

`AGENTS.md` is becoming the cross-tool convention and is the best single bet.
These paths change; check your tool's docs if one doesn't take.

**What degrades outside Claude Code:** the scripts need Python and shell access
(there's a hand-executable fallback); visual verification needs browser tooling
(without it, findings are marked `code-only`); parallel audits need subagents (the
sequential sweep is the default anyway). None of it is load-bearing — the rules,
the diagnosis and the audit discipline work in any agent that can read files.

</details>

## What else it does

**Establish a design system** — *"This project has no design standards. Set some
up."* A short interview (product, personality, stack, optionally a reference site
whose fonts and colors it reads directly), then five artifacts: tokens JSON, a
Tailwind theme for *your* version, framework-neutral CSS, a human-readable
`DESIGN.md` in your language, and a shareable `preview.html`.

Colors are **computed, not invented.** The book gives a complete palette algorithm
and zero specific values, so the script implements the algorithm — bisection from a
base shade, saturation raised as lightness leaves 50%, hue rotated toward brighter
or darker hues within a 20–30° cap. Every text pair is contrast-checked before it
ships.

**Build something new** — follows the book's order instead of jumping to pixels:
feature before shell, grayscale before color, ranked content, values off the scale,
measure and rhythm, *then* color, depth and polish. The empty state gets designed
**with** the feature, not after.

**Explain why** — *"Why does grey text look wrong on our blue banner?"* Loads one
reference and gives you the mechanism: what makes grey-on-white work isn't
greyness, it's *reduced contrast* — the text moved closer to the background. On
white those are the same direction, which hides the real mechanism. On blue they
aren't. `§2.3`

## Notes for your setup

**You don't need Tailwind.** It's throughout because the book's author wrote it, so
it's the shortest notation available — not because anything requires it. Hierarchy,
measure, group spacing, contrast, elevation: none of that is a Tailwind concept.
The skill detects what you actually have and adapts — v4 `@theme`, v3 config,
tokens injected into shadcn/MUI/Ant's own contract, translation into your existing
vocabulary, or framework-neutral CSS variables if you have nothing. **It will never
install Tailwind, migrate your styling, or replace a design system you already
have.**

**If you also use a design mode, ask for the review separately.** This is the one
non-obvious thing. When you ask a design tool to build something and it succeeds,
nothing signals a problem, so **no review happens** — a generator doesn't come back
and critique its own work. Closing that gap takes one sentence from you: *"now
review that against the design rules."* Cheaper still is going the other direction:
hand it your tokens *before* it builds.

These aren't in tension, though it can look that way. Skills like `frontend-design`
push toward *distinctive*; this pushes toward *systematic*. Different axes. A
system tells you which blue and which spacing step — it never told you to build
another boring dropdown. (The book makes that point itself, at `§8.6`.)

**Say up front where you deviate on purpose.** Intentionally linear spacing scale,
intentionally mixed radius, intentionally low-contrast brand color — mention it.
Deliberate project conventions outrank the book's rules and get noted rather than
scored as defects, but the skill can't know a choice was deliberate until you tell
it, and an audit whose first page is full of decisions you already made is one
you'll stop reading.

## How it works

Three layers, loaded progressively. `SKILL.md` (~220 lines) holds routing, twelve
universal laws and four workflows, and stays in context. The 14 references load one
at a time, only when the task needs them. Scripts and templates sit underneath.

Every rule carries the same six parts — **Rule · Why · How · Values · Tailwind ·
Fails as** — so the skill reasons about *mechanism* rather than reciting
conclusions. "Fails as" is the diagnostic entry point: start from what looks wrong,
arrive at the rule.

Four things keep it honest:

- **Existing systems always win.** It maps onto what you have, or proposes what's
  missing. It never overwrites, migrates, or installs.
- **Placeholders, not palettes.** Examples say `bg-{primary}-600`, never
  `bg-indigo-600` — syntactically impossible to paste, so colors must resolve from
  *your* tokens. That single convention is why it won't quietly ship you indigo.
- **Invariants are marked.** Bold numbers are the book's rules and don't vary.
  Everything else is one valid instance, not the required answer.
- **Extensions are labeled.** Dark mode, focus states, motion and z-index post-date
  the book. They're included, in a file that says so on every entry.

<details>
<summary><b>Project structure</b></summary>

```
.claude-plugin/          plugin + marketplace manifests
skills/refactoring-ui/
  SKILL.md               routing, twelve laws, four workflows
  references/
    00-coverage-matrix   all 151 rules, tracked — the anti-omission device
    01-08                one per book chapter
    10-15                Tailwind mapping, tokens, recipes, audit rubric,
                         antipatterns, extensions beyond the book
  scripts/               generate_palette · check_contrast · emit_tokens
  assets/                token template, hand-fillable theme skeleton
  examples/              worked before → after cases, also eval fixtures
```

</details>

## Contributing

Issues and PRs welcome. Two rules specific to this repo:

1. **Never add content copied from the book** — no prose, no figures. Restate in
   your own words. See [ATTRIBUTION.md](ATTRIBUTION.md).
2. **Keep the coverage matrix true.** Any change to a reference updates its row in
   `00-coverage-matrix.md`. That file is why nothing gets quietly dropped.

## License

[MIT](LICENSE) for everything here. The book is a separate copyrighted work; this
project reimplements its principles independently and isn't affiliated with its
authors — [ATTRIBUTION.md](ATTRIBUTION.md) has the details.

---

*Built because a PM with weak design instincts wanted the book's judgment available
every time an agent touched a stylesheet.*
