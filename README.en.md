# Refactoring UI: a Claude Skill

A Web-UI design rulebook an AI coding agent can actually execute, plus a diagnostic layer on top. Extracted from [*Refactoring UI*](https://www.refactoringui.com) by Adam Wathan & Steve Schoger.

> ⚠️ **Unofficial and independent.** Not affiliated with, endorsed by, or reviewed by the book's authors.

> It is no substitute for the book itself, [read the original if it interests you](https://www.refactoringui.com) — it's genuinely good.

> See [ATTRIBUTION.md](ATTRIBUTION.md) for details.

**[中文文档 →](README.md)**

---

## Contents

- [The problem](#the-problem)
- [What this is](#what-this-is)
- [What it looks like](#what-it-looks-like)
- [Install](#install)
- [What else it does](#what-else-it-does)
- [A few things worth knowing upfront](#a-few-things-worth-knowing-upfront)
- [How it works](#how-it-works)
- [License](#license)

## The problem

AI writes competent HTML and CSS, and the interface still comes out slightly wrong. Nothing errors out, but something feels off.

Everything centered. One spacing value from top to bottom. The primary color always leaning indigo or purple. Every action rendered as a filled button. No empty state.

None of these look like much on their own. The trouble is that **generation is local, while design has to be judged globally.**

What's missing in between is a rulebook.

## What this is

Most AI design tooling generates: describe an interface, receive one.

This Skill does the opposite job. It's the constraint layer and the diagnostic layer — the rulebook and the reviewer, not the stylist.

Which makes it complementary to those generators rather than competing with them: **hand it the constraints before generation, hand it the output for a walkthrough afterward.**

Refactoring UI is a rules book, not an inspiration book. Nearly every page is *symptom → mechanism → specific fix → concrete number*, and its author also wrote Tailwind CSS, so almost nothing is lost between principle and code: the book's type scale, spacing scale and color ramps are Tailwind's defaults. This project turns the whole book into executable rules — **151 of them**, each one traceable.

## What it looks like

> *"Have a look at this settings page — something feels off but I can't tell what."*

It detects your stack, renders the page at desktop and mobile widths, then works through seven lenses in a fixed order: **hierarchy → spacing → typography → color → depth → images → finishing**.

The order is causal. Until hierarchy is sorted out, what counts as a spacing problem keeps shifting; and once spacing is fixed, the question "does this need a border" often disappears on its own.

Every finding it returns is severity-ranked and must cite a rule:

| Sev | Rule | Now | Proposed |
| --- | ---- | --- | -------- |
| P0 | §3.6 | Label spacing equals group spacing — each label sits as far from its own input as from the next group | `mb-1` inside, `mb-6` between |
| P1 | §2.8 | Three buttons all styled as the primary action | Keep one primary; outline and link for the rest |
| P1 | §6.2 | `shadow-lg` on static cards | Use `shadow-sm`. A shadow expresses elevation, not importance |

There's also a **Systemic** section that looks at the whole rather than the parts — for example, "this project has no spacing scale."

## Install

```
/plugin marketplace add edisonmbli/refactoring-ui-skill
/plugin install refactoring-ui
```

That's it. No central package registry, and nothing gets uploaded anywhere. What `marketplace add` does is clone the repo and read `.claude-plugin/marketplace.json`; `install` then loads the contents from the conventional directories. Updating is `git pull` wearing a different name: `/plugin marketplace update refactoring-ui`.

The scripts want **Python 3.9+** and have zero third-party dependencies. Without Python it still works — the palette algorithm comes with a hand-executable procedure.

<details>
<summary><b>Other ways to install: as a plain skill, and for non-Claude-Code tools</b></summary>

### Claude Code, as a plain skill

```bash
git clone https://github.com/edisonmbli/refactoring-ui-skill.git

cp -r refactoring-ui-skill/skills/refactoring-ui ~/.claude/skills/   # personal
cp -r refactoring-ui-skill/skills/refactoring-ui .claude/skills/     # project
```

### Other coding agents

The plugin mechanism belongs to Claude Code, but the Skill itself doesn't. It's a pile of Markdown, deliberately built as "an index plus references loaded on demand" — any agent that can read files can follow it. You just have to tell it once.

First put the Skill somewhere stable:

```bash
git clone https://github.com/edisonmbli/refactoring-ui-skill.git .refactoring-ui
```

Then copy a ready-made pointer file instead of hand-typing one — a description-only trigger is exactly the kind of instruction agents skip under load:

```bash
# Codex, Copilot, Windsurf, Cline/Roo, Aider, or as an AGENTS.md fallback for Cursor
cp .refactoring-ui/templates/AGENTS.md AGENTS.md          # or merge into your existing one

# Cursor specifically — glob-matched, so it attaches on the file type, not on Cursor
# guessing intent from a description
mkdir -p .cursor/rules && cp .refactoring-ui/templates/cursor/refactoring-ui.mdc .cursor/rules/
```

| Agent | Where it goes |
| ----- | ------------- |
| **OpenAI Codex** | `AGENTS.md` at the repo root |
| **Cursor** | `.cursor/rules/refactoring-ui.mdc` (glob-matched — see above), or `AGENTS.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Windsurf** | `.windsurf/rules/design.md` |
| **Cline / Roo** | `.clinerules/design.md` |
| **Aider** | `CONVENTIONS.md`, passed with `--read` at startup |
| **Anything else** | Whatever it reads at session start; failing that, pasting `templates/AGENTS.md`'s content into the chat also works |

`AGENTS.md` is becoming the cross-tool convention, so prefer it where available. These paths change often — if one doesn't take effect, check the tool's current docs.

What you lose outside Claude Code: the scripts need Python and permission to run commands, though there's a manual fallback; visual verification needs browser tooling, without which conclusions come from source alone and the Skill marks them `code-only`; parallel walkthroughs need subagents, while sequential is the default anyway. None of this is load-bearing — the rules, the diagnosis and the walkthrough discipline hold up in any agent that can read files.

</details>

## What else it does

**Build a design system**——*"This project has no design standards. Set some up."*

A short Q&A first: what the product is, what personality you want, what stack you're on. You can also just give it a reference site's URL and it will read that site's font stack and primary color. Then it delivers five things: a token JSON, a Tailwind theme matching your actual version, framework-neutral CSS, a human-readable `DESIGN.md`, and a `preview.html` you can send straight to a colleague.

Colors are computed, not picked out of the air. The book gives a complete palette algorithm and not one specific color value, so the script implements that algorithm: bisect down from a base color, raise saturation as lightness moves away from 50%, rotate hue toward brighter or darker hues within a 20–30° cap. Every text-color pairing is contrast-checked before delivery.

**Build something new**——following the book's order instead of jumping straight to pixels.

Feature before shell, grayscale before color, content ranked first. Values must come from an established scale; measure and rhythm get settled before color, depth and finishing. The empty state is designed alongside the feature, not bolted on afterward.

**Ask why**——*"Why does grey text look so bad on our blue banner?"*

It loads a single reference file and explains the mechanism: grey text works on white not because it's grey, but because contrast came down — the text moved toward the background color. On white, "going grey" and "reducing contrast" happen to be the same direction, which hides what's actually going on; on blue, the two part ways immediately. `§2.3`

## A few things worth knowing upfront

**Not using Tailwind is completely fine.** Tailwind runs through this whole document because the book's author later wrote it, making it the most economical notation available — not because anything depends on it. Hierarchy, measure, group spacing, contrast, elevation: none of them are Tailwind concepts.

The Skill checks what you're actually using before adapting: `@theme` for v4, config for v3; if you're on shadcn/MUI/Ant, tokens go into their own theme configuration; if you already have tokens, it translates into the naming you have; if you have nothing, you get framework-neutral CSS variables. **It won't install Tailwind for you, won't migrate your styling approach, and won't replace a design system you already have.**

**If you're also using another design-generation tool (a Design mode, `frontend-design`, that sort of thing), you need to ask for the walkthrough explicitly.** The reason: when you ask a design tool to do something and it succeeds, nothing anywhere raises a flag, so the walkthrough simply never happens — a generator doesn't come back and critique its own work. All it takes from you is one more sentence: *"now review that against the design rules."* Or, more economically, do it the other way around and hand it the design tokens **before** it starts.

These two things look like they're at odds, but they aren't. The `frontend-design` family pursues distinctiveness; this pursues consistency. Two different axes. A design system tells you which blue and which spacing step — it never told you to build another boring dropdown. (The book says as much itself, at `§8.6`.)

**Wherever something is deliberate, say so at the start.** A deliberately linear spacing scale, deliberately mixed radii, a brand color deliberately low in contrast — one sentence before you begin is enough. A project's own deliberate conventions outrank the book's rules, and the Skill will flag the conflict rather than score it as a defect. But if you don't say so, it has no way to know the choice was intentional, and a report whose first page is full of decisions you already made is one you'll stop reading after a couple of scrolls.

## How it works

Three layers, loaded progressively. `SKILL.md` (~220 lines) holds routing, 12 universal laws and 4 workflows, and stays in context; 14 reference files load on demand, one at a time; scripts and templates sit underneath.

Every rule takes the same six-part shape——**Rule · Why · How · Values · Tailwind · Fails as**——so the model can reason along the mechanism rather than reciting conclusions. "Fails as" is the diagnostic entry point: start from what looks wrong, work back to the rule.

Four commitments keep it from drifting:

- **Existing systems always win.** It does two things only: map principles onto the naming you already have, or suggest something where it's missing. Never overwrite, never migrate, never install unasked.
- **What it hands you are placeholders, not palettes.** Examples always say `bg-{primary}-600`, never `bg-indigo-600`: that syntax simply cannot be pasted into code, so colors have to be resolved from your own tokens. That one convention is why it won't quietly ship you a pile of indigo.
- **Invariants are marked.** Bolded numbers are the book's rules and don't vary by project; everything else is one valid value, not the required answer.
- **Extensions are labeled.** Dark mode, focus states, motion, z-index all came after this book. They're all included, but in a separate file where every entry states "the book doesn't cover this."

<details>
<summary><b>Project structure</b></summary>

```
.claude-plugin/          plugin + marketplace manifests
skills/refactoring-ui/
  SKILL.md               routing, 12 laws, 4 workflows
  references/
    00-coverage-matrix   all 151 rules tracked, the anti-omission device
    01-08                one per chapter of the book
    10-15                Tailwind mapping, tokens, component recipes,
                         audit rubric, antipatterns, beyond the book
  scripts/               generate_palette · check_contrast · emit_tokens
  assets/                token template, hand-fillable theme skeleton
  examples/              before → after cases, also eval fixtures
```

</details>

## License

Everything in this repository is [MIT](LICENSE). The book is a separate copyrighted work; this project only reimplements its principles independently and is not affiliated with its authors. Details in [ATTRIBUTION.md](ATTRIBUTION.md).

---

*Made by a PM with weak design instincts. What he wanted was simple: every time an AI touches a stylesheet, the book's judgment is in the room.*
