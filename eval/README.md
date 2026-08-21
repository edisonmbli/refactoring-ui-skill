# Gold set — 怎么跑 evaluation

**动手请先跟 [CHECKLIST.md](CHECKLIST.md)**（人工逐步勾选），或 **Slim B 自动回归跟 [AGENT_RUN.md](AGENT_RUN.md)**。打分与汇总页：

```bash
python3 eval/summarize.py eval/runs/<run-id>
open eval/runs/<run-id>/index.html
```

8 个可在浏览器打开的真实界面，用来验证 `refactoring-ui` Skill 的 **Workflow D（只诊断）**。内容全不全看覆盖矩阵；能不能用看这套题。

## 套件里有什么

| id | 界面 | 这题在考什么 |
|---|---|---|
| `01-settings` | 账号设置 | 三个实心按钮（含破坏性主按钮）、彩底灰字、表单成组间距 |
| `02-login` | 登录 | **P0 成组间距**（标签离输入框 = 离下一组）、双主按钮、输入框外阴影 |
| `03-empty` | 空项目列表 | 禁用的筛选/表头该删不该灰掉；缺 CTA；不是「搜不到」 |
| `04-stats` | 指标卡 | 标签比数字还大；静态卡用了弹层级阴影 |
| `05-landing` | 营销首页 | 已有 teal 品牌却用了 indigo→粉渐变；四个实心 CTA |
| `06-article` | 帮助正文 | 行长远超 45–75；长文居中 |
| `07-hero` | 浅色风景英雄区 | 白字压浅图、无遮罩。**必须看渲染** |
| `08-blotter` | 支付流水台 | **克制题**：密度是故意的。报「留白不够 / §3.1」算误报 |

产品设定统一为 **Lumen**（发票工具），已有主色 `#0f766e`。把主色改成 indigo 不是修复，是误报。

每个 case：

```
eval/cases/<id>/index.html     # 打开这个看界面
eval/cases/<id>/expected.json  # must / should / forbidden
```

字段含义见 [SCHEMA.md](SCHEMA.md)。

- **must** — 漏一条，本题 FAIL  
- **should** — 允许漏报，只记 recall，不否决  
- **forbidden** — 当作缺陷写进 finding 表，本题 FAIL  

## 通过线（建议）

一次完整 run：

1. **8/8 must 全中**，且 **08 没有密度误报** → 套件 PASS  
2. should-recall 作趋势，不设门槛（第一次跑出个基数即可）  
3. 触发词另测，见下方「触发 eval」——和审计质量分开记

不要用「平均感觉还行」代替这条线。

## 跑法 A — 人工（Cursor / Claude Code）

**必须新开会话。** 写 Skill 的那条对话里带着作者上下文，会掩盖指令漏洞。

1. 确认 Skill 已安装（Claude：`/plugin install refactoring-ui`；Cursor：按仓库 README 把 Skill 挂进会读到的规则里）。
2. 每个 case **单独开一条空对话**，只贴 `expected.json` 里的 `prompt` 字段（不要把 `expected.json` 本身贴给模型）。
3. 要求它走 Workflow D：探测栈 → 能开页就开 → 七镜 → finding 表，每条挂 `§` 号。
4. 把完整报告存成：

```
eval/runs/<run-id>/01-settings.md
eval/runs/<run-id>/02-login.md
...
eval/runs/<run-id>/08-blotter.md
```

文件名必须等于 case id，评分脚本靠这个对齐。

5. 打分：

```bash
python3 eval/score.py --self-check          # 先确认黄金集自身可解析
python3 eval/score.py --dir eval/runs/<run-id>
```

单题：

```bash
python3 eval/score.py --case 01-settings eval/runs/<run-id>/01-settings.md
```

`score.py` 只扫描 **同时出现 P0/P1/P2 和 § 规则号** 的行（finding 表）。在「刻意约定 / 不是缺陷」段落里提到某条规则，只要那一行没有严重度标记，不会记成误报。

退出码：全过为 `0`，有 FAIL 为 `1`。

## 跑法 B — 对照基线（有没有 Skill）

同一条 prompt 跑两遍，**两条都要新会话**：

| 条件 | 做法 |
|---|---|
| Skill 开启 | 正常安装 |
| Skill 关闭 | Claude Code：按官方文档关掉该 skill 的可见性；Cursor：本轮不要挂这条 skill / 不要指向 SKILL.md |

对比时看三件硬的，不要看文笔：

- finding 是否挂得出规则号  
- must 命中是否更高  
- 08 会不会把密度当缺陷  

## 跑法 C — skill-creator（可选）

Anthropic 的 `skill-creator` 默认读 **Skill 目录下的** `evals/evals.json`。本仓库黄金集在仓库根的 `eval/`，避免和 plugin 约定抢位置。

若要用插件自动跑：

```bash
mkdir -p skills/refactoring-ui/evals
cp eval/evals.json skills/refactoring-ui/evals/evals.json
```

然后在 Claude Code 里装 `skill-creator@claude-plugins-official`，按它的 eval 流程跑。`evals.json` 里的 `files` 是相对**仓库根**的路径；复制过去之后若插件以 skill 目录为根，需要把 `files` 改成 `../../../eval/cases/...` 或改成把 HTML 拷进 `evals/files/`。

审计质量仍以 `score.py` + `expected.json` 为准。skill-creator 的 `expectations` 是自然语言断言，适合做冒烟，不替代 must/forbidden。

## 触发 eval（和审计分开）

`eval/triggers.json` 里是该触发 / 不该触发的用户原话。

做法：每条一句，新会话，看模型是否去读 `SKILL.md`（或是否自称在用 refactoring-ui）。

- `should_trigger` 漏读 → 触发失败  
- `should_not_trigger` 却读了 → 过度触发  

不要和 8 道审计题混成一个分数。

## 本地预览界面

```bash
# macOS
open eval/cases/01-settings/index.html
```

或起一个静态服务再截桌面 1280 / 手机 375：

```bash
python3 -m http.server 8765 --directory eval/cases
# http://127.0.0.1:8765/01-settings/index.html
```

`07-hero` 不打开页面几乎必挂：源码里是 `color: #fff`，对比问题只在浅色背景上才成立。

## 改黄金集时

- 先改 HTML，再改 `expected.json`，最后 `python3 eval/score.py --self-check`  
- must 宁少勿滥：只放「这题不抓就说明 Skill 没起作用」的条目  
- 不要把 should 提成 must 来「显得严格」——漏报预算就是 should 的意义
