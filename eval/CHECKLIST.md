# Eval 操作清单（照着勾）

两套题，**分数分开记**，不要混。

- A. 触发是否准确（15 句）
- B. 8 个页面审计（Workflow D）

每条都要 **新开一条空对话**。不要把 `expected.json` 贴给模型。

开始前：Skill 已安装；工作目录是本仓库根目录。

```bash
python3 eval/score.py --self-check
```

通过即可往下。

---

## A. 触发是否准确

判断标准（二选一即算触发）：

- 读了 `skills/refactoring-ui/SKILL.md`（或已安装的同名 Skill）
- 明确按本 Skill 的路由 / 铁律 / Workflow 在走

只是「凭常识评了两句 UI」、没加载本 Skill → 算 **未触发**。

### A1 应该触发（8 句）— 漏读 = 失败

在仓库里随便放着页面即可，**不要**附带「请读取 refactoring-ui Skill」。

| # | 勾 | 原话（整句粘贴） | 结果 |
|---|---|---|---|
| 1 | ☐ | 帮我看看这个设置页，总觉得哪里不对但说不上来。 | 触发 / 未触发 |
| 2 | ☐ | 对这个页面做一次设计评审。 | |
| 3 | ☐ | UI 太丑了，帮我指出问题，先别改代码。 | |
| 4 | ☐ | 这个项目没有设计规范，帮我定一套 design tokens。 | |
| 5 | ☐ | 为什么灰字放在蓝色 banner 上这么难看？ | |
| 6 | ☐ | Review this landing page for visual hierarchy and spacing. | |
| 7 | ☐ | This form looks off — audit it against design rules before changing anything. | |
| 8 | ☐ | Establish a type scale, spacing scale, and color ramps for this app. | |

第 1、2、7 句若对话里没有打开任何页面，可随口补一句「看 `eval/cases/01-settings/index.html`」，**不要**改写原任务。

### A2 不该触发（7 句）— 读了 Skill = 失败

| # | 勾 | 原话 | 结果 |
|---|---|---|---|
| 9 | ☐ | 给这个 API 加一个分页参数。 | 未触发 / 误触发 |
| 10 | ☐ | 解释一下这段 Python 里的 GIL 行为。 | |
| 11 | ☐ | 帮我写 commit message。 | |
| 12 | ☐ | 修复这个 SQL 注入，不要动前端。 | |
| 13 | ☐ | 把 README 的错别字改掉。 | |
| 14 | ☐ | Refactor this reducer for readability; the UI is out of scope. | |
| 15 | ☐ | Why is the test suite failing on CI? | |

**A 通过线：** A1 全触发，A2 全不触发。缺一记下来，不要用 B 的分数补。

---

## B. 8 个页面（只诊断、不改文件）

1. 建目录：`mkdir -p eval/runs/$(date +%Y-%m-%d)`
2. 下面 8 条，**一条对话只跑一页**。
3. 报告存成对应文件名（必须完全一致，否则 `score.py` 对不上）。
4. 能开页就打开看渲染。`07-hero` 不打开几乎必挂。

主色已有：`#0f766e`（teal）。改成 indigo 不是修复。

### B1 `01-settings` → `eval/runs/<日期>/01-settings.md`

```
对 eval/cases/01-settings/index.html 做设计评审（Workflow D，只诊断、不改文件）。这是 Lumen 发票产品的设置页。项目已有主色 #0f766e（teal），不是 indigo。请先探测技术栈，有条件就打开页面看渲染，按七个视角出 finding 表，每条必须挂规则号。
```

### B2 `02-login` → `02-login.md`

```
对 eval/cases/02-login/index.html 做设计评审（Workflow D，只诊断、不改文件）。Lumen 登录页，主色 #0f766e。有条件请打开页面看渲染。每条 finding 必须挂规则号。
```

### B3 `03-empty` → `03-empty.md`

```
对 eval/cases/03-empty/index.html 做设计评审（Workflow D，只诊断、不改文件）。这是 Lumen 的项目列表，当前账号下还没有任何项目。有条件请打开页面。每条 finding 必须挂规则号。
```

### B4 `04-stats` → `04-stats.md`

```
对 eval/cases/04-stats/index.html 做设计评审（Workflow D，只诊断、不改文件）。Lumen 概览页的指标卡。主色 #0f766e。有条件请打开页面。每条 finding 必须挂规则号。
```

### B5 `05-landing` → `05-landing.md`

```
对 eval/cases/05-landing/index.html 做设计评审（Workflow D，只诊断、不改文件）。这是 Lumen 的营销首页。品牌规范已经确定：主色是 #0f766e（teal），不是 indigo。页面是另一次生成留下来的。有条件请打开页面。每条 finding 必须挂规则号。
```

### B6 `06-article` → `06-article.md`

```
对 eval/cases/06-article/index.html 做设计评审（Workflow D，只诊断、不改文件）。这是 Lumen 帮助中心的一篇正文。有条件请在桌面宽度（约 1280）打开页面看实际行长。每条 finding 必须挂规则号。
```

### B7 `07-hero` → `07-hero.md`

```
对 eval/cases/07-hero/index.html 做设计评审（Workflow D，只诊断、不改文件）。Lumen 营销英雄区，背景是浅色风景插画（无遮罩）。请打开页面看渲染，不要只看源码里的 color: white。每条 finding 必须挂规则号。
```

### B8 `08-blotter` → `08-blotter.md`

```
对 eval/cases/08-blotter/index.html 做设计评审（Workflow D，只诊断、不改文件）。这是 Lumen 财务人员全天开着的支付流水台。密度是产品决定，不是疏忽。有条件请打开页面。每条 finding 必须挂规则号。不要为了显得全面而报「留白不够」。
```

勾选：☐1 ☐2 ☐3 ☐4 ☐5 ☐6 ☐7 ☐8

### 打分

```bash
python3 eval/score.py --dir eval/runs/<日期>
```

**B 通过线：** 终端显示 `8/8 cases passed`。

- `MUST MISS` = 该抓没抓（漏报）
- `FP` = 不该报却报了（误报，08 报 §3.1 最典型）
- `SHLD miss (allowed)` = 允许漏，只看趋势

本地看页：`open eval/cases/01-settings/index.html`（其余同路径换文件夹）。

---

## 记分（抄在这里）

```
日期：
模型 / 工具：

A 触发：  应该触发  _/8     不该触发（未误触）  _/7
B 审计：  score.py  _/8
备注：
```

可选：同一套 B 的 8 句 prompt，**关掉 Skill** 再跑一遍，只对比「有没有规则号、must 是否更差」，不要和上面混成一个总分。
