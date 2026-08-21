#!/usr/bin/env python3
"""Score every case in a run folder and write a single HTML dashboard.

  python3 eval/summarize.py eval/runs/auto-2026-08-21
  python3 eval/summarize.py eval/runs/auto-2026-08-21 --json
"""
from __future__ import annotations

import argparse, html, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import score as S  # noqa: E402

KIND_LABEL = {"must": "must", "should": "should", "forbidden": "forbidden"}

FONTS = """
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600&display=swap" rel="stylesheet" />
"""

# Canvas/surfaces from Linear homepage tokens. Action/pass/fail from
# generate_palette.py --base #5e6ad2 | #27a644 | #eb5757.
# Text #f7f8f8 / #d0d6e0 / #8a8f98 from Linear. Hairline solid #23252a
# (Linear rgba(255,255,255,.08) equivalent). Lighter surface = closer.
CSS = """
:root {
  --action-400: #7b9be3; --action-500: #5e6ad2;
  --pass-400: #47cd7e; --pass-500: #27a644;
  --fail-400: #f89174; --fail-500: #eb5757;
  --miss-400: #ffca38;
  --page: #08090a;
  --surface: #0f1011;
  --raised: #191a1b;
  --hover: #141516;
  --hair: #23252a;
  --text: #f7f8f8;
  --secondary: #d0d6e0;
  --muted: #8a8f98;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 64px;
  --fs-12: 12px; --fs-14: 14px; --fs-16: 16px;
  --fs-20: 20px; --fs-24: 24px; --fs-36: 36px;
  --lh-tight: 1.05; --lh-snug: 1.25; --lh-body: 1.5;
  --weight-body: 400; --weight-strong: 600;
  --radius: 12px;
  --radius-btn: 6px;
  --focus: 0 0 0 2px var(--page), 0 0 0 4px var(--action-500);
  --font: Inter, "SF Pro Display", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --chrome: inset 0 1px 0 #2c2e32, 0 0 0 1px var(--hair);
}
*, *::before, *::after { box-sizing: border-box; }
html { color-scheme: dark; }
body {
  margin: 0;
  font-family: var(--font);
  font-size: var(--fs-16);
  font-weight: var(--weight-body);
  color: var(--text);
  background: var(--page);
  line-height: var(--lh-body);
}
a { color: var(--muted); text-decoration: none; }
a:hover { color: var(--text); }
a.report { color: var(--action-400); }
a.report:hover { color: var(--text); }
a:focus-visible, summary:focus-visible, .btn-primary:focus-visible {
  outline: none;
  box-shadow: var(--focus);
}
.skip { position: absolute; left: -999px; }
.skip:focus { left: var(--space-4); top: var(--space-4); z-index: 2; background: var(--surface); padding: var(--space-2) var(--space-3); }
.topnav {
  height: 56px;
  border-bottom: 1px solid var(--hair);
}
.topnav .inner, .canvas {
  max-width: 1360px;
  margin: 0 auto;
  padding: 0 var(--space-5);
}
.topnav .inner {
  height: 56px;
  display: flex;
  align-items: center;
  gap: var(--space-5);
}
.brand {
  color: var(--text);
  font-weight: var(--weight-strong);
  letter-spacing: -0.02em;
}
.nav-muted { color: var(--muted); font-size: var(--fs-12); }
.nav-spacer { flex: 1; }
.canvas { padding: var(--space-7) var(--space-5) var(--space-8); }
.command {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: baseline;
  column-gap: var(--space-6);
  row-gap: var(--space-2);
  margin: 0 0 var(--space-7);
}
.command h1 {
  margin: 0;
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  font-size: var(--fs-36);
  font-weight: var(--weight-strong);
  line-height: var(--lh-tight);
  letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.lede {
  margin: 0;
  color: var(--secondary);
  font-size: var(--fs-14);
  line-height: var(--lh-snug);
  text-wrap: pretty;
  text-wrap: balance;
}
.notes {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2) var(--space-5);
  color: var(--muted);
  font-size: var(--fs-12);
  font-variant-numeric: tabular-nums;
  grid-column: 1 / -1;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  border-radius: var(--radius-btn);
  background: var(--action-500);
  color: #fff;
  font-size: var(--fs-12);
  font-weight: var(--weight-strong);
}
.btn-primary:hover { color: #fff; filter: brightness(1.08); }
.stage {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-4);
  align-items: start;
}
.tile {
  background: var(--surface);
  border-radius: var(--radius);
  padding: var(--space-5);
  box-shadow: var(--chrome);
  display: flex;
  flex-direction: column;
  min-height: 100%;
}
.tile:hover { background: var(--hover); }
.tile-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-3);
}
.kicker {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin: 0;
  font-family: var(--font-mono);
  font-size: var(--fs-12);
  color: var(--muted);
}
.status {
  font-size: var(--fs-12);
  font-weight: var(--weight-strong);
  letter-spacing: 0.04em;
  flex: none;
}
.status.pass { color: var(--pass-400); }
.status.fail { color: var(--fail-400); }
.status.missing { color: var(--miss-400); }
.tile h2 {
  margin: var(--space-3) 0 0;
  font-size: var(--fs-20);
  font-weight: var(--weight-strong);
  letter-spacing: -0.025em;
  line-height: var(--lh-snug);
  text-wrap: balance;
}
.tile h2 a { color: var(--text); }
.tally {
  margin: var(--space-3) 0 0;
  font-family: var(--font-mono);
  font-size: var(--fs-12);
  color: var(--muted);
  font-variant-numeric: tabular-nums;
}
.tile-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  margin-top: auto;
  padding-top: var(--space-4);
}
.tile-actions .links { display: flex; gap: var(--space-4); margin: 0; font-size: var(--fs-12); }
.judge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--fs-12);
  color: var(--muted);
  flex: none;
}
.judge:hover { color: var(--text); }
.judge svg { display: block; flex: none; }
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex: none;
  background: var(--muted);
}
.dot.pass { background: var(--pass-500); }
.dot.fail { background: var(--fail-500); }
.dot.missing { background: var(--miss-400); }
.overlay {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 40;
  align-items: center;
  justify-content: center;
  padding: var(--space-5);
}
.overlay:target { display: flex; }
.overlay-scrim {
  position: absolute;
  inset: 0;
  background: color-mix(in srgb, var(--page) 45%, transparent);
  backdrop-filter: blur(8px);
}
.overlay-panel {
  position: relative;
  z-index: 1;
  width: min(40rem, 100%);
  max-height: 85vh;
  overflow: auto;
  background: var(--raised);
  border-radius: var(--radius);
  box-shadow: inset 0 1px 0 #2c2e32, 0 var(--space-5) var(--space-7) hsla(0,0%,0%,.55);
  padding: var(--space-6);
}
.overlay-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--space-4);
  margin: 0 0 var(--space-5);
}
.overlay-head h2 {
  margin: 0;
  font-size: var(--fs-16);
  font-weight: var(--weight-strong);
}
.overlay-head .status { margin-left: auto; }
.overlay h3 {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  margin: var(--space-6) 0 var(--space-3);
  font-size: var(--fs-12);
  font-weight: var(--weight-strong);
  color: var(--muted);
}
.overlay h3:first-of-type { margin-top: 0; }
.overlay h3 span {
  font-family: var(--font-mono);
  color: var(--secondary);
  font-variant-numeric: tabular-nums;
}
.table-wrap { overflow-x: auto; margin: 0 0 var(--space-3); }
table.grid {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  font-size: var(--fs-12);
}
table.grid col.c-mark { width: 4.5rem; }
table.grid col.c-rule { width: 7.5rem; }
table.grid col.c-hit { width: 6.5rem; }
table.grid th, table.grid td {
  text-align: left;
  padding: var(--space-3) var(--space-3) var(--space-3) 0;
  border-bottom: 1px solid var(--hair);
  vertical-align: top;
}
table.grid th { color: var(--muted); font-weight: var(--weight-strong); }
table.grid td:first-child, table.grid th:first-child { white-space: nowrap; }
.mark { font-family: var(--font-mono); font-weight: var(--weight-strong); }
.mark.ok { color: var(--pass-400); }
.mark.bad { color: var(--fail-400); }
.mono { font-family: var(--font-mono); font-size: var(--fs-12); }
.muted { color: var(--muted); font-size: var(--fs-12); }
.who {
  margin: 0 0 var(--space-3);
  display: flex;
  align-items: baseline;
  gap: var(--space-2);
  font-family: var(--font-mono);
  font-size: var(--fs-12);
  color: var(--muted);
}
.who .status { font-family: var(--font); }
.report-hero { margin: 0 0 var(--space-8); }
.report-hero h1 {
  margin: 0 0 var(--space-4);
  max-width: 22em;
  font-size: var(--fs-36);
  font-weight: var(--weight-strong);
  letter-spacing: -0.03em;
  line-height: var(--lh-snug);
  text-wrap: balance;
}
.report-hero .meta { font-size: var(--fs-12); }
.report-body { max-width: none; }
.report-body > h2 {
  margin: var(--space-8) 0 var(--space-4);
  font-size: var(--fs-20);
  font-weight: var(--weight-strong);
  letter-spacing: -0.02em;
}
.report-body > h2:first-child { margin-top: 0; }
.report-body > h3 {
  margin: var(--space-7) 0 var(--space-4);
  font-size: var(--fs-12);
  font-weight: var(--weight-strong);
  letter-spacing: 0.06em;
  color: var(--muted);
}
.report-body > h2 + h3 { margin-top: var(--space-5); }
.report-body > p {
  margin: 0 0 var(--space-5);
  max-width: 40em;
  color: var(--secondary);
  font-size: var(--fs-16);
  line-height: 1.65;
  text-wrap: pretty;
}
.report-body li {
  margin: 0 0 var(--space-3);
  color: var(--secondary);
  line-height: 1.65;
  text-wrap: pretty;
}
.report-body > ul, .report-body > ol {
  margin: 0 0 var(--space-7);
  max-width: 40em;
  padding: var(--space-6) var(--space-6) var(--space-6) var(--space-8);
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--chrome);
}
.report-body hr {
  border: 0;
  border-top: 1px solid var(--hair);
  margin: var(--space-8) 0;
}
.report-body .table-wrap {
  margin: 0 0 var(--space-4);
  padding: var(--space-6);
  background: var(--surface);
  border-radius: var(--radius);
  box-shadow: var(--chrome);
  overflow-x: auto;
}
table.audit {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
  font-size: var(--fs-14);
}
table.audit col.c-num { width: 2.5rem; }
table.audit col.c-lens { width: 6.5rem; }
table.audit col.c-loc { width: 11rem; }
table.audit col.c-rule { width: 5rem; }
table.audit col.c-eff { width: 3.5rem; }
table.audit th {
  text-align: left;
  padding: 0 var(--space-4) var(--space-3) 0;
  border-bottom: 1px solid var(--hair);
  color: var(--muted);
  font-size: var(--fs-12);
  font-weight: var(--weight-strong);
  letter-spacing: 0.05em;
}
table.audit td {
  text-align: left;
  padding: var(--space-4) var(--space-4) var(--space-4) 0;
  border-bottom: 1px solid var(--hair);
  vertical-align: top;
  color: var(--secondary);
  line-height: var(--lh-body);
  text-wrap: pretty;
}
table.audit td:nth-child(1),
table.audit td:nth-child(7) {
  font-family: var(--font-mono);
  font-size: var(--fs-12);
  color: var(--muted);
}
table.audit td:nth-child(3) {
  font-family: var(--font-mono);
  font-size: var(--fs-12);
  word-break: break-word;
}
.report-body code {
  font-family: var(--font-mono);
  font-size: 0.92em;
  background: var(--raised);
  padding: 0 0.25em;
  border-radius: var(--radius-btn);
}
@media (max-width: 1100px) {
  .stage { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .command { grid-template-columns: 1fr; }
  .command h1 { white-space: normal; }
}
@media (max-width: 640px) {
  .stage { grid-template-columns: 1fr; }
  .command h1 { font-size: var(--fs-24); }
  .report-hero h1 { font-size: var(--fs-24); }
  .overlay { padding: 0; align-items: stretch; }
  .overlay-panel {
    width: 100%;
    max-height: none;
    height: 100%;
    border-radius: 0;
  }
  table.audit col.c-loc { width: 7rem; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; }
  .overlay-scrim { backdrop-filter: none; }
}
"""

def collect(run_dir: Path) -> dict:
    cases = S.list_cases()
    rows = []
    for cid in cases:
        exp = S.load_expected(cid)
        report_path = run_dir / f"{cid}.md"
        if not report_path.exists():
            rows.append({
                "id": cid,
                "title": exp.get("title", cid),
                "status": "missing",
                "passed": False,
                "must": [{"passed": False, **item, "hit": None} for item in exp.get("must", [])],
                "should": [{"passed": False, **item, "hit": None} for item in exp.get("should", [])],
                "forbidden_hits": [],
                "found_rules": [],
                "should_recall": None,
                "report": None,
                "report_text": "",
            })
            continue
        text = report_path.read_text(encoding="utf-8")
        result = S.score_case(exp, text)
        result["title"] = exp.get("title", cid)
        result["status"] = "pass" if result["passed"] else "fail"
        result["report"] = str(report_path)
        result["report_text"] = text
        rows.append(result)

    n = len(rows)
    n_pass = sum(1 for r in rows if r["status"] == "pass")
    n_fail = sum(1 for r in rows if r["status"] == "fail")
    n_miss = sum(1 for r in rows if r["status"] == "missing")
    should_hits = sum(sum(1 for i in r["should"] if i["passed"]) for r in rows)
    should_total = sum(len(r["should"]) for r in rows)
    return {
        "run": run_dir.name,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "pass": n_pass,
        "fail": n_fail,
        "missing": n_miss,
        "total": n,
        "should_hits": should_hits,
        "should_total": should_total,
        "cases": rows,
    }


def _esc(s) -> str:
    return html.escape("" if s is None else str(s))


def _inline_md(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r'<code>\1</code>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def md_to_html(src: str) -> str:
    """Small GFM subset: headings, tables, lists, hr, bold, inline code."""
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    sep = re.compile(r"^\|[\s:|-]+\|$")
    bullet = re.compile(r"^[-*] ")
    numbered = re.compile(r"^\d+\. ")

    while i < n:
        line = lines[i]
        if line.startswith("|") and i + 1 < n and sep.match(lines[i + 1].strip()):
            rows = []
            while i < n and lines[i].startswith("|"):
                row = lines[i]
                if sep.match(row.strip()):
                    i += 1
                    continue
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
                i += 1
            if rows:
                head, *body = rows
                keys = {c.strip().lower() for c in head}
                thead = "<tr>" + "".join(f"<th>{_inline_md(c)}</th>" for c in head) + "</tr>"
                tbody = "".join(
                    "<tr>" + "".join(f"<td>{_inline_md(c)}</td>" for c in r) + "</tr>"
                    for r in body
                )
                if {"lens", "now", "proposed"} <= keys:
                    cols = (
                        '<colgroup><col class="c-num" /><col class="c-lens" /><col class="c-loc" />'
                        '<col class="c-rule" /><col class="c-now" /><col class="c-prop" /><col class="c-eff" /></colgroup>'
                    )
                    klass = "audit"
                else:
                    cols = COLGROUP
                    klass = "grid"
                out.append(f'<div class="table-wrap"><table class="{klass}">{cols}<thead>{thead}</thead><tbody>{tbody}</tbody></table></div>')
            continue
        if line.startswith("### "):
            out.append(f"<h3>{_inline_md(line[4:])}</h3>"); i += 1; continue
        if line.startswith("## "):
            out.append(f"<h2>{_inline_md(line[3:])}</h2>"); i += 1; continue
        if line.startswith("# "):
            out.append(f"<h1>{_inline_md(line[2:])}</h1>"); i += 1; continue
        if line.strip() in ("---", "***", "___"):
            out.append("<hr />"); i += 1; continue
        if bullet.match(line):
            items = []
            while i < n and bullet.match(lines[i]):
                items.append(f"<li>{_inline_md(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if numbered.match(line):
            items = []
            while i < n and numbered.match(lines[i]):
                items.append(f"<li>{_inline_md(numbered.sub('', lines[i], count=1))}</li>"); i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        if not line.strip():
            i += 1
            continue
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("|") and not bullet.match(lines[i]) and not numbered.match(lines[i]) and lines[i].strip() not in ("---", "***"):
            buf.append(lines[i]); i += 1
        out.append("<p>" + "<br />".join(_inline_md(x.rstrip()) for x in buf) + "</p>")
    return "\n".join(out)


COLGROUP = (
    '<colgroup><col class="c-mark" /><col class="c-rule" />'
    '<col class="c-now" /><col class="c-hit" /></colgroup>'
)

JUDGE_ICON = (
    '<svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true">'
    '<path fill="none" stroke="currentColor" stroke-width="1.25" '
    'd="M4 2.5H2.75A.75.75 0 0 0 2 3.25v6c0 .41.34.75.75.75h6c.41 0 .75-.34.75-.75V8M7 2h3v3M10 2 6.5 5.5"/>'
    "</svg>"
)


def _item_rows(items, kind: str) -> str:
    if not items:
        return f'<p class="muted">本用例没有 {KIND_LABEL[kind]} 项。</p>'
    bits = []
    for it in items:
        ok = it.get("passed")
        hit = it.get("hit")
        if kind == "forbidden":
            flagged = bool(it.get("hit"))
            mark = "触发" if flagged else "未触发"
            tone = "bad" if flagged else "ok"
        else:
            mark = "满足" if ok else "未满足"
            tone = "ok" if ok else "bad"
        rules = ", ".join(it.get("rules") or it.get("hit") or [])
        now = it.get("now") or it.get("why") or ""
        bits.append(
            f'<tr class="{tone}"><td><span class="mark {tone}">{_esc(mark)}</span></td>'
            f'<td class="mono">{_esc(rules)}</td>'
            f'<td>{_esc(now)}</td>'
            f'<td class="mono">{_esc(hit or "")}</td></tr>'
        )
    return (
        '<div class="table-wrap"><table class="grid">'
        f"{COLGROUP}<thead><tr>"
        "<th>判定</th><th>规则</th><th>预期</th><th>匹配</th>"
        f"</tr></thead><tbody>{''.join(bits)}</tbody></table></div>"
    )


def _nav(extra: str) -> str:
    return (
        '<nav class="topnav" aria-label="主导航"><div class="inner">'
        '<a class="brand" href="index.html">Slim B</a>'
        '<span class="nav-muted">Workflow D</span>'
        '<span class="nav-spacer"></span>'
        f"{extra}"
        "</div></nav>"
    )


def render_report(case: dict, run_id: str) -> str:
    body = md_to_html(case.get("report_text") or "")
    st = case["status"]
    st_label = {"pass": "PASS", "fail": "FAIL", "missing": "无报告"}.get(st, st)
    fixture = f"../../cases/{case['id']}/index.html"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_esc(case["id"])} · 报告</title>
  {FONTS}
  <style>{CSS}</style>
</head>
<body>
  <a class="skip" href="#report">跳到正文</a>
  {_nav(f'<a class="btn-primary" href="index.html">返回汇总</a>')}
  <main class="canvas" id="report">
    <header class="report-hero">
      <p class="who"><span class="dot {st}"></span> <span class="status {st}">{_esc(st_label)}</span> · {_esc(case["id"])} · {_esc(run_id)}</p>
      <h1>{_esc(case.get("title") or case["id"])}</h1>
      <p class="meta"><a href="{_esc(fixture)}">原页面</a></p>
    </header>
    <div class="report-body">{body}</div>
  </main>
</body>
</html>
"""


def render(data: dict, run_dir: Path) -> str:
    tiles = []
    overlays = []
    first_bad = next((r["id"] for r in data["cases"] if r["status"] != "pass"), None)
    for r in data["cases"]:
        st = r["status"]
        body_must = _item_rows(r["must"], "must")
        body_should = _item_rows(r["should"], "should")
        fps = [{"rules": x.get("hit", []), "why": x.get("why", ""), "hit": ", ".join(x.get("hit") or []), "passed": False} for x in r.get("forbidden_hits") or []]
        if not fps and r["status"] != "missing":
            fp_html = '<p class="muted">未触发 forbidden。</p>'
        elif r["status"] == "missing":
            fp_html = '<p class="muted">无报告，无法判定。</p>'
        else:
            fp_html = _item_rows(fps, "forbidden") if fps else '<p class="muted">无报告，无法判定。</p>'
        fixture = f"../../cases/{r['id']}/index.html"
        report_rel = f"{r['id']}.html" if r.get("report") else ""
        must_hit = sum(1 for i in r["must"] if i.get("passed"))
        must_n = len(r["must"])
        sh = r.get("should_recall")
        if not r.get("should"):
            tally = f"must {must_hit}/{must_n}"
            should_n = ""
        else:
            sh_s = "—" if sh is None else f"{int(sh * 100)}%"
            tally = f"must {must_hit}/{must_n} · should {sh_s}"
            should_n = sh_s
        report_link = f'<a class="report" href="{_esc(report_rel)}">报告</a>' if report_rel else ""
        title_href = report_rel or f"#{r['id']}"
        st_label = {"pass": "PASS", "fail": "FAIL", "missing": "无报告"}.get(st, st)
        oid = f"judge-{r['id']}"
        should_block = (
            f"<h3>should <span>{_esc(should_n)}</span></h3>{body_should}"
            if r.get("should") else
            f"<h3>should</h3>{body_should}"
        )
        tiles.append(f"""
<article class="tile" id="{_esc(r['id'])}">
  <div class="tile-top">
    <p class="kicker"><span class="dot {st}"></span> {_esc(r['id'])}</p>
    <span class="status {st}">{_esc(st_label)}</span>
  </div>
  <h2><a href="{_esc(title_href)}">{_esc(r.get('title', r['id']))}</a></h2>
  <p class="tally">{_esc(tally)}</p>
  <div class="tile-actions">
    <p class="links">
      <a href="{_esc(fixture)}">原页面</a>{report_link}
    </p>
    <a class="judge" href="#{_esc(oid)}">判定明细{JUDGE_ICON}</a>
  </div>
</article>
""")
        overlays.append(f"""
<div class="overlay" id="{_esc(oid)}" role="dialog" aria-modal="true" aria-labelledby="h-{_esc(oid)}">
  <a class="overlay-scrim" href="#board" aria-label="关闭"></a>
  <div class="overlay-panel">
    <div class="overlay-head">
      <h2 id="h-{_esc(oid)}">{_esc(r['id'])}</h2>
      <span class="status {st}">{_esc(st_label)}</span>
      <a href="#board">关闭</a>
    </div>
    <h3>must <span>{must_hit}/{must_n}</span></h3>
    {body_must}
    {should_block}
    <h3>forbidden</h3>
    {fp_html}
  </div>
</div>
""")
    should_s = (
        f"{data['should_hits']}/{data['should_total']}"
        if data["should_total"] else "—"
    )
    verdict = "未全部通过" if (data["fail"] or data["missing"]) else "全部通过"
    score_dot = "fail" if data["fail"] else ("missing" if data["missing"] else "pass")
    nav_right = f'<span class="nav-muted">{_esc(data["run"])}</span>'
    if first_bad:
        nav_right += f'<a class="btn-primary" href="#{_esc(first_bad)}">未通过用例</a>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Slim B · {_esc(data['run'])}</title>
  {FONTS}
  <style>{CSS}</style>
</head>
<body>
  <a class="skip" href="#board">跳到用例</a>
  {_nav(nav_right)}
  <main class="canvas">
    <header class="command">
      <h1 id="score"><span class="dot {score_dot}"></span> {data['pass']}/{data['total']} {_esc(verdict)}</h1>
      <p class="lede">must 全部满足、且未触发 forbidden，才算 PASS。should 只看趋势，不决定是否通过。</p>
      <ul class="notes">
        <li>{data['fail']} FAIL</li>
        <li>{data['missing']} 无报告</li>
        <li>{_esc(should_s)} should</li>
      </ul>
    </header>
    <section class="stage" id="board" aria-label="用例舞台">{''.join(tiles)}</section>
  </main>
  {''.join(overlays)}
  <script>
  document.addEventListener("keydown", function (e) {{
    if (e.key === "Escape" && location.hash.indexOf("#judge-") === 0) location.hash = "#board";
  }});
  </script>
</body>
</html>
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run_dir", type=Path)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    run_dir = a.run_dir.resolve()
    if not run_dir.is_dir():
        raise SystemExit(f"not a directory: {run_dir}")
    data = collect(run_dir)
    out_html = run_dir / "index.html"
    out_html.write_text(render(data, run_dir), encoding="utf-8")
    for r in data["cases"]:
        if r.get("report_text"):
            (run_dir / f"{r['id']}.html").write_text(render_report(r, data["run"]), encoding="utf-8")
    slim = {
        "run": data["run"],
        "generated": data["generated"],
        "pass": data["pass"],
        "fail": data["fail"],
        "missing": data["missing"],
        "total": data["total"],
        "should_hits": data["should_hits"],
        "should_total": data["should_total"],
        "cases": [
            {
                "id": r["id"],
                "status": r["status"],
                "passed": r["passed"],
                "must_hit": sum(1 for i in r["must"] if i.get("passed")),
                "must_n": len(r["must"]),
                "should_recall": r.get("should_recall"),
                "forbidden": [x.get("hit") for x in r.get("forbidden_hits") or []],
            }
            for r in data["cases"]
        ],
    }
    (run_dir / "summary.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False), encoding="utf-8")
    if a.json:
        print(json.dumps(slim, indent=2, ensure_ascii=False))
    print(f"{data['pass']}/{data['total']} PASS  {data['fail']} FAIL  {data['missing']} missing")
    print(out_html)
    return 0 if data["fail"] == 0 and data["missing"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
