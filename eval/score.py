#!/usr/bin/env python3
"""Score an audit report against eval/cases/<id>/expected.json.

  python3 eval/score.py eval/cases/01-settings/report.md
  python3 eval/score.py --case 01-settings path/to/audit.md
  python3 eval/score.py --dir eval/runs
  python3 eval/score.py --self-check

Extracts § IDs from markdown finding table rows under P0/P1/P2 (or rows that themselves contain P0/P1/P2). Prose mentions of a rule do not count.
"""
from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "cases"
RULE_RE = re.compile(r"§\d+\.\d+(?:\.\d+|[a-z])?")
SEV_RE = re.compile(r"\bP[012]\b")


HEADING_SEV_RE = re.compile(r"^#{2,3}\s*P[012]\b")
TABLE_ROW_RE = re.compile(r"^\|")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|")


def extract_finding_rules(text: str) -> set[str]:
    """Collect § IDs from finding *table rows* only.

    Prose that says "§8.4 does not apply" must not count as a defect.
    A line counts when it is a markdown table row (not the `---` separator)
    AND either contains P0/P1/P2 itself or sits under a `### P0` / `### P1`
    / `### P2` heading. Other headings close the severity scope.
    """
    hits: set[str] = set()
    in_sev_section = False
    for line in text.splitlines():
        if line.startswith("#"):
            in_sev_section = bool(HEADING_SEV_RE.search(line))
            continue
        if not TABLE_ROW_RE.match(line) or TABLE_SEP_RE.match(line):
            continue
        if SEV_RE.search(line) or in_sev_section:
            hits.update(RULE_RE.findall(line))
    return hits


def load_expected(case_id: str) -> dict:
    path = CASES / case_id / "expected.json"
    if not path.exists():
        raise SystemExit(f"no expected.json for case {case_id}")
    return json.loads(path.read_text())


def infer_case_id(report: Path) -> str:
    name = report.stem
    if (CASES / name).is_dir():
        return name
    parent = report.parent.name
    if (CASES / parent).is_dir():
        return parent
    raise SystemExit(
        f"cannot infer case id from {report}. Use --case <id>."
    )


def score_case(expected: dict, report_text: str) -> dict:
    found = extract_finding_rules(report_text)
    must_results = []
    for item in expected.get("must", []):
        rules = item["rules"]
        hit = next((r for r in rules if r in found), None)
        must_results.append({**item, "hit": hit, "passed": hit is not None})

    should_results = []
    for item in expected.get("should", []):
        rules = item["rules"]
        hit = next((r for r in rules if r in found), None)
        should_results.append({**item, "hit": hit, "passed": hit is not None})

    fp = []
    for item in expected.get("forbidden", []):
        rules = item["rules"]
        hit = [r for r in rules if r in found]
        if hit:
            fp.append({**item, "hit": hit})

    must_pass = all(x["passed"] for x in must_results)
    passed = must_pass and not fp
    should_n = len(should_results)
    should_hits = sum(1 for x in should_results if x["passed"])
    return {
        "id": expected["id"],
        "passed": passed,
        "must": must_results,
        "should": should_results,
        "forbidden_hits": fp,
        "found_rules": sorted(found),
        "should_recall": None if not should_n else round(should_hits / should_n, 2),
    }


def print_case(result: dict) -> None:
    flag = "PASS" if result["passed"] else "FAIL"
    print(f"\n[{flag}] {result['id']}")
    print(f"  cited in finding rows: {', '.join(result['found_rules']) or '(none)'}")
    for item in result["must"]:
        mark = "hit " + item["hit"] if item["passed"] else "MISS"
        print(f"  MUST {mark:12} {item['rules'][0]:<10} {item['now']}")
    for item in result["should"]:
        mark = "hit " + item["hit"] if item["passed"] else "miss (allowed)"
        print(f"  SHLD {mark:16} {item['rules'][0]:<10} {item['now']}")
    for item in result["forbidden_hits"]:
        print(f"  FP   {item['hit']}  {item['why']}")
    if result["should_recall"] is not None:
        print(f"  should-recall {result['should_recall']}")


def list_cases() -> list[str]:
    return sorted(p.name for p in CASES.iterdir() if (p / "expected.json").exists())


def self_check() -> int:
    """Gold files parse; a synthetic report with every must-rule should pass."""
    failed = 0
    for cid in list_cases():
        exp = load_expected(cid)
        lines = []
        for i, item in enumerate(exp.get("must", []), 1):
            lines.append(f"| {i} | hierarchy | P0 | loc | {item['rules'][0]} | now | fix | S |")
        fake = "\n".join(lines) or "| 1 | hierarchy | P2 | loc | §9.9 | none | none | S |"
        result = score_case(exp, fake)
        if exp.get("must") and not result["passed"]:
            print(f"self-check FAIL {cid}: synthetic must-report did not pass")
            failed += 1
        else:
            print(f"self-check ok   {cid}")
    return 1 if failed else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("report", nargs="?", type=Path)
    p.add_argument("--case")
    p.add_argument("--dir", type=Path, help="score every *.md whose stem is a case id")
    p.add_argument("--json", action="store_true")
    p.add_argument("--self-check", action="store_true")
    a = p.parse_args()

    if a.self_check:
        return self_check()

    results = []
    if a.dir:
        for md in sorted(a.dir.glob("*.md")):
            if md.stem not in list_cases():
                continue
            exp = load_expected(md.stem)
            results.append(score_case(exp, md.read_text()))
        if not results:
            raise SystemExit(f"no matching reports in {a.dir}")
    elif a.report:
        cid = a.case or infer_case_id(a.report)
        results.append(score_case(load_expected(cid), a.report.read_text()))
    else:
        p.print_help()
        return 2

    if a.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print_case(r)
        n = sum(1 for r in results if r["passed"])
        print(f"\n{n}/{len(results)} cases passed")

    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
