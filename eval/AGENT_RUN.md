# Slim B — 父代理执行说明

在 Cursor 里对新的 Skill 改动做审计回归。子代理用 **Grok 4.6 Medium**。不要用 Fast，也不要更高推理档。

## 一键（报告已经在时）

```bash
# 打分 + 写出汇总页
python3 eval/summarize.py eval/runs/<run-id>
open eval/runs/<run-id>/index.html   # macOS
```

没有报告时，先走下面「派发 8 路」，再跑这一句。

`eval/run.sh <run-id>` 是上面的包装。

## 派发 8 路（要 Cursor 父代理来做）

对每个 `eval/cases/<id>/` 起一个**新的**子代理，互不共享对话。Prompt = 本文件「硬约束」+ 该 case `expected.json` 的 `prompt` 字段。

硬约束：

```
最多读 3 个文件：
  skills/refactoring-ui/SKILL.md
  skills/refactoring-ui/references/13-audit-rubric.md
  eval/cases/<id>/index.html
禁止读 expected.json / CHECKLIST / eval README / PLAN / 其它章节。
禁止开浏览器、起服务、截图。Verified: code-only。
禁止再派子代理。只诊断，不改 fixture。
把完整报告写到 eval/runs/<run-id>/<id>.md 后立刻停。
```

跑完：

```bash
python3 eval/summarize.py eval/runs/<run-id>
```

通过线：汇总页顶栏 **8/8 PASS**。`should` 只作趋势。触发词（A 组）不在这套脚本里。

## 本次目录约定

`eval/runs/auto-2026-08-21/`
