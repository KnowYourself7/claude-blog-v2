# 开发文档：blog-brief 加 Step 11，A→B 阶段门

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 已实施，等合并 |
| 分支 | feat/blog-brief-gate-a-to-b，从 `main` 的 10ea95d 开 |
| 依据 | 第 05 课 A→B 阶段门三项检查、产物落盘、检查不等于人工确认（p.127）；第 00 课每一步有输入、产物和验收（p.106），质量门要说清「哪一步有问题、为什么、怎么修」（p.29）；Anthropic 官方 Skill authoring best practices「Create verifiable intermediate outputs」：中间产物用脚本校验，出错信息指明具体问题，https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| 上一份文档 | `docs/plans/2026-10-25-blog-brief-run-state-and-gate.md`：状态文件和阶段门的总方案，2026-10-25 用户确认。本文件是其中第二个分支的细化，背景和原因只摘要，详见那份文档第 3 节 |
| 路线图 | `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节第 8 行 |

## 1. 目标

跑完 blog-brief 的 10 步后，脚本做一次 A→B 阶段门（阶段门：一个阶段结束时的集中检查，过了才进下一阶段），告诉用户简报能不能交给 `/blog write`；不能的话，写明哪一项没过、要从哪一步重做；能的话，把还没解决的事列成一张清单。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| A·04 竞争机会、A·09 语义基线的检查 | 这两步还没做。阶段门对它们写 `not built`，不算失败。各自单独开分支 |
| 判断类检查：收窄说法是否真的更窄、核心答案是否回答了问题、内链是否合适 | 不做。由 Step 8 的 Check 管，脚本判断不了 |
| 预算上限和余额检查（p.109） | 随 A·02「先复用，再补研究」的分支一起定。阶段门只报告 Step 4 和 Step 6 文件里已经写下的积分数 |
| 让 `/blog write` 读阶段门结果，没过就不写 | 路线图第 9 个分支 `feat/blog-write-use-brief` |
| 把阶段门插在 Step 9 之前 | 不做，见第 5 节 |
| 用真实客户产物当测试数据 | 不做。单元测试的简报文件自己编；Coofandy 产物只在 scratchpad 里跑一次，不进仓库 |

## 3. 原因

现在 blog-brief 做完 Step 10 就结束。Step 10 最后一句让 Claude 告诉用户简报可以交给 `/blog write`（`skills/blog-brief/SKILL.md` 第 102 行）。这句话没有任何检查撑着：

1. 方向、结构、证据三样是否都清楚（p.127），没有一处一起看。每步的 Check 只看自己的产物。
2. 重跑或手改之后，没人回头查下游。真实例子：Coofandy「can you wear linen in winter」测试里，Step 7 重跑 7 次、Step 8 重跑 2 次。状态文件（#19）会把下游改回 `pending`，但用户直接手改大纲时，状态文件不知道。大纲里引用的材料号如果在证据计划里已经改成 `rejected`，现在没有任何一步会发现。
3. 步骤的 Check 是 Claude 自己判断自己。可以机械核对的跨文件关系（面、增量、材料号是否对得上），交给脚本更可靠。课程的阶段门也是脚本检查（p.127）。
4. 没有一条记录写着「这次简报过了没有」，也没有一处把待办事项（Still Open、证据薄弱的问题、缺失的支撑页）一次摆给用户。

上一份文档 3.2 节用 Coofandy 第 2 次大纲真实跑手工模拟过：正常跑一遍时，阶段门挑不出新错（13 个材料号全是 `adopted`，9 个面、6 个增量全进了第二版）。所以阶段门做小：只做脚本能查的跨文件检查，加一张待办清单。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| `briefs/[slug]-state.json` | Step 1 到 Step 10 的状态和产出文件路径。阶段门从这里找每个文件，不自己拼路径，所以 `--file` 存到别处的简报也能找到 |
| `[slug]-task-brief.md` | Page this post supports |
| `[slug]-search-intent.md` | Decision 和 User choice |
| `[slug]-demand-facets.md` | Kept Facets 表的 ID |
| `[slug]-competitor-gaps.md` | Data Scope 的 Fetch 行里的积分 |
| `[slug]-evidence-plan.md` | Questions 表的 Weak 列；Sources 表的 # 和 Status；Search Plan 的 Total 行 Actual credits |
| `[slug]-information-gain.md` | Gains 表的 ID |
| `[slug]-outline.md` | 第一版的 Calculator 行；第二版每个 H2 的 Facets、Evidence、Gains 行，FAQ 的 Evidence，Still Open |
| `[slug]-brief.md` | Content Outline 一节 |

### 4.2 处理步骤

`brief_state.py` 加子命令 `gate`。SKILL.md 清单加一行 Step 11，步骤文件 `references/step-11-a-to-b-gate.md`。

1. Claude 跑 `set --step 11 --status in_progress`。状态文件已经保证 Step 1 到 Step 10 全是 `done`。
2. Claude 跑 `gate --slug [slug]`。Step 11 不是 `in_progress`，脚本报错。
3. 脚本逐项检查（检查项见 4.3），每项给 `pass`、`fail`、`warn` 或 `not built`。`fail` 项写明要重做的步骤。
4. 脚本按结果改 Step 11 的状态：
   - 没有 `fail`：Step 11 改成 `done`，note 写「Gate: pass」或「Gate: warn」。
   - 有 `fail`，而上一次阶段门不是 `fail`：Step 11 保持 `in_progress`。输出 `redo_from`，即所有 `fail` 项里最早要重做的步骤。
   - 有 `fail`，上一次也是 `fail`：Step 11 改成 `stopped`，note 列出 `fail` 项。连续两次就停是本项目的规则，课程没写，为了不让 Claude 在同一个错上来回重做。
5. Claude 按结果做：
   - `done`：把 `warn` 项和待办清单摆给用户，说明简报可以交给 `/blog write`。原 Step 10 最后一句挪到这里。
   - `in_progress` 加 `redo_from`：先把 `fail` 项和要重做的步骤告诉用户，再对那一步跑 `set --status in_progress`（下游自动改回 `pending`，Step 11 也是），从那一步重做，回到 Step 11 再跑 `gate`。
   - `stopped`：把 `fail` 项摆给用户，等回答。用户要接受现状，Claude 跑 `set --step 11 --status in_progress`，再跑 `set --step 11 --status done --note "[用户的回答]"`；用户要改，就按用户说的步骤重做。

   手动把 Step 11 设成 `done` 有两个条件，由脚本把关：状态文件里要有比 Step 1 到 Step 10 最后一次改动更新的阶段门结果，并且带 `--note` 写用户的回答。这样不跑 `gate` 就绕不过去。接受之后 `gate` 段记 `accepted`，下一次 `fail` 重新从 1 数。

为什么让脚本改 Step 11 的状态：要不要停、连续几次，每次结果都该一样，交给脚本，Claude 少记一条规则。

### 4.3 检查项

| 门（p.127） | 检查 | 不过时 | 重做 |
|---|---|---|---|
| 落盘 | Step 1 到 Step 10 记录的产出文件都还在 | fail | 第一个缺文件的步骤 |
| 方向 | 搜索意图的 Decision 是 `continue`，或 User choice 是 `write anyway` | fail | Step 2 |
| 方向 | 任务单的 Page this post supports 不是 `missing` | warn | - |
| 方向 | 竞争机会 | not built | - |
| 结构 | 每个保留面都在第二版某个 H2 的 Facets 行；Facets 行没有保留面以外的 ID | fail | Step 8 |
| 结构 | 增量文件的每个 ID 都在第二版某个 Gains 行；Gains 行没有增量文件以外的 ID | fail | Step 8 |
| 结构 | 第一版的 Calculator 行已填写，不是空的或方括号 | fail | Step 8 |
| 结构 | 简报的 Content Outline 和第二版一致（去掉 Title 行、空行、行尾空格后比较） | fail | Step 9 |
| 证据 | 第二版 H2 和 FAQ 的 Evidence 引用的材料号，在证据计划 Sources 表里都是 `adopted` | fail | Step 8 |
| 证据 | 第二版每个 H2 有材料号，或者 Narrower claim 不是 `-` | fail | Step 8 |
| 证据 | 证据计划里 Weak 为 `yes` 的问题 | 有就 warn，列出 ID 和问题 | - |
| 证据 | 第二版的 Still Open | 不是 `none` 就 warn，列出内容 | - |
| 证据 | 语义基线 | not built | - |

补充规则：

- FAQ 的 Evidence 也查材料号。这是比上一份文档多的一处。课程的结构清楚一项写了「常见问题」（p.127），FAQ 的答案同样会进正文。
- 文件里找不到要解析的段落或表时，该项 `fail`，重做产出这个文件的步骤。例子：大纲没有 Outline V2 一节。
- 材料号只取 Evidence 里每个逗号项开头的数字，括号里的字不算。例子：`1, 3 (estimated, 2019)` 只取 1 和 3。表格里转义的竖线 `\|` 不拆格。
- 几处写法放宽：Weak 列不分大小写；支撑页以 `missing` 开头就算缺；Still Open 写 `- none` 也算没有。Still Open 还留着方括号时 `fail`，重做 Step 8。
- Introduction 的 Hook 和各 H2 的 Components 里的材料号不查。那里是自由文字，数字不一定是材料号（例子：「12 rows」），脚本分不清。这两处仍由 Step 8 的 Check 管。

### 4.4 输出

状态文件加一段 `gate`，同时打印同样的 JSON：

```json
"gate": {
  "result": "warn",
  "checked": "2026-10-25T10:02:00Z",
  "attempt": 1,
  "redo_from": null,
  "credits": {"step_4": 5, "step_6": 43},
  "items": [
    {"gate": "evidence", "check": "Still Open", "result": "warn",
     "detail": "H2 1: the cold-band cells rest on no adopted comfort range", "redo": null}
  ]
}
```

- `result`：有 `fail` 就是 `fail`，否则有 `warn` 就是 `warn`，否则 `pass`。`not built` 不影响结果。
- `attempt`：连续 `fail` 的次数。上一次不是 `fail` 时从 1 开始；这次没有 `fail` 时是 0。
- `credits`：文件里找不到数字就写 `null`，不写 0。
- 重跑前面的步骤时，`set` 只把 Step 11 改回 `pending`，`gate` 段留着，下一次 `gate` 靠它数连续次数。用户接受后，`gate` 段多一个 `accepted: true`。`gate` 段只在 Step 11 是 `done` 时代表当前简报。

### 4.5 下游怎么变

- SKILL.md 清单加 Step 11 一行，标 Can stop；Step 10 去掉最后一句。
- 以后 `feat/blog-write-use-brief` 可以读 `gate.result` 和 Step 11 的状态，决定能不能写。这次不改 `/blog write`。

### 4.6 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/scripts/brief_state.py` | 加 `gate` 子命令和各项检查；docstring 加说明 |
| `skills/blog-brief/references/step-11-a-to-b-gate.md` | 新建，六段格式 |
| `skills/blog-brief/SKILL.md` | 清单加 Step 11；Step 10 去掉最后一句；State File 第 3 条加一句：Step 11 照它的步骤文件做 |
| `tests/test_brief_state.py` | 步骤数改成 11；加阶段门测试 |
| `tests/test_blog_brief_workflow.py` | 步骤数改成 11 |
| `CLAUDE.md` | blog-brief 步骤文件数改成 10，脚本说明加阶段门 |
| `docs/plans/2026-10-25-blog-brief-run-state-and-gate.md` | 状态行写明第二个分支见本文件 |
| 本文件 | 第 6 节填实际结果 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 阶段门插在 Step 9 之前 | 能少生成一次简报，但 Step 9、Step 10 要改编号，所有提到它们的文件、测试和旧开发文档都要跟着改。上一份文档已定放在最后 |
| 阶段门由 Claude 按清单逐项判断，不写脚本 | 和各步骤的 Check 重复，又是 Claude 自己判断自己。课程的阶段门由脚本检查（p.127） |
| `gate` 只写结果，Step 11 的状态由 Claude 用 `set` 改 | 上一份文档的写法。要在步骤文件里多写「连续两次 fail 就停」的规则让 Claude 照做；脚本已经知道上一次结果，自己改更稳 |
| 阶段门结果单独存一个 `[slug]-gate.md` 文件 | 多一个模板和一个文件。结果是给脚本和下游读的，放进状态文件就够；摆给用户的部分由 Claude 从 JSON 转述 |
| 检查 Content Outline 时逐字比较，不去空行 | Step 9 抄写时多一个空行就会误报，空行不影响写作 |

## 6. 验证

### 6.1 结果

| 验证项 | 结果 |
|---|---|
| 先看到失败 | 先写 19 项阶段门测试，`gate` 还不存在时全部失败；写完脚本后有 1 项仍失败，原因是测试本身只改了大纲的 Still Open、没改简报，阶段门正确地报了 Content Outline 不一致。补上简报后全过 |
| 脚本单元测试 | `tests/test_brief_state.py` 共 39 项（参数化用例逐个算），比 `main` 的 13 项多 26 项。第一次提交时是 30 项，之前写成「33 项，新加 19 项」，是数错了，审查时发现。内容：Step 11 不是 `in_progress` 时报错；全过；`warn` 三项；11 种 `fail` 各指对重做的步骤；连续两次 `fail` 停下；重做后 Step 11 改回 `pending`、`gate` 段保留、下一次能过；用户接受停下的阶段门。审查后加 9 项：转义竖线、3 种 Evidence 写法、宽松写法、Still Open 没填、没有阶段门结果不能设 `done`、手动 `done` 要 `--note`、接受后重新计数 |
| 仓库检查 | 见 6.4 |
| 整篇重读 | 脚本：赋值给变量的 lambda 改成函数，嵌套三元表达式拆成 if/elif，Content Outline 不一致时改为直接列出两边不同的那一行（原来报「第几行」，数的是去掉空行后的行号，用户对不上文件），删掉 `cmd_gate` 里没用的 `load_steps()`。步骤文件：没删句子 |
| 模拟跑（子代理，Haiku，只读 SKILL.md 和 Step 11 步骤文件） | 三个场景（第一次 `fail`、第二次 `fail` 后用户说照写、`warn`）命令全部走对。提了 9 处疑问，补了 4 处：SKILL.md 写「gate 设状态」和步骤文件第 5 条手动 `set done` 冲突，改成「Step 11 照它的步骤文件做」；第一次 `fail` 时先告诉用户；重做「一直做到这一步」；加一条规则：`warn` 不挡简报，由用户决定。没补的 5 处：重做是否要问积分（各步骤自己管）、`fail` 还在时用户照写怎么办（就是用户的决定，note 记下）、`set done` 会不会被接受（会，Step 11 没有产出文件）、stopped 的 note 谁写（脚本写，Claude 只需转述）、重做时 Step 11 的状态（脚本自动改回 `pending`） |
| 真实产物跑 | Coofandy「can you wear linen in winter」：Step 1 到 4 用主目录的文件，证据计划用 `rerun-2026-10-23-evidence-plan`，增量用 `rerun-2026-10-24-gain-list-5`，大纲和简报用 `rerun-2026-10-24-outline-2`，拼在 scratchpad 里，不进仓库。结果 `warn`：9 个面、6 个增量、13 个材料号全对上，和上一份文档的手工模拟一致；两条 `warn` 是支撑页 `missing` 和 Still Open 一条；Step 4 积分 5，Step 6 积分 `null`（那版证据计划还没有 Actual credits 列）。然后把大纲里一处 Evidence 加上材料 2（证据计划里是 `reference`）：第一次 `fail`，`redo_from` 8，同时报 Content Outline 不一致（重做 Step 9），第二次 `fail` 后 Step 11 变成 `stopped` |
| 对照瑜东审查（子代理，独立，只给课程和代码） | 课程 p.127 的要求都落实了或在 6.2 写明。挑出 2 处必须改、5 处建议改、1 组可不改，全部核实属实。改了：转义竖线 `\|` 被拆格，标题带竖线的已采用材料被误报（必须改）；开发文档测试数写错（必须改）；Evidence 行里年份、小写 narrower claim 后面的数字被当成材料号；接受停下的阶段门后连续次数不清零，下一次第一次 `fail` 就停；不跑 `gate` 也能手动把 Step 11 设成 `done`；Weak 大写、`missing (…)`、`- none`、Still Open 留方括号几种写法；Check 里「gate 在最后一次改动之后跑过」Claude 没法核对，改成「每次改动后再跑一次」。没改：Hook 和 Components 的材料号不查，理由见 4.3；6.2 那一行改成部分符合。真实产物复跑：接受后重做 Step 8，新一轮 `attempt` 从 0 开始，结果 `warn` |
| 对照瑜东（提交前评估） | 见 6.2 |
| 对照上游原版（提交前评估） | 见 6.3 |

### 6.2 对照瑜东第 05 课 A→B 阶段门（p.127）

| 课程要求 | 现在 | 结论 |
|---|---|---|
| 方向清楚：关键词与搜索意图 | SERP 判定必须是 `continue` 或用户选了照写 | 符合 |
| 方向清楚：读者任务和页面职责 | 支撑页 `missing` 时 `warn`；读者任务由 Step 2 的 Check 管 | 部分符合：读者任务写得好不好要判断，脚本不查 |
| 方向清楚：竞争机会与风险处置 | `not built` | 不符合，A·04 还没做，按路线图暂缓 |
| 结构清楚：需求面与第二版大纲 | 保留面和第二版 Facets 行双向核对 | 符合 |
| 结构清楚：章节、常见问题、内链 | 章节有材料号或收窄说法；FAQ 的材料号也查；简报和第二版一致。内链只由 Step 8 的 Check 管 | 部分符合：内链要判断，脚本不查 |
| 结构清楚：计算器候选的取舍 | 第一版 Calculator 行必须填写 | 符合 |
| 证据清楚：研究计划与来源线索 | H2 和 FAQ 引用的材料号都是 `adopted`；薄弱问题 `warn` | 部分符合：Hook 和 Components 里的材料号是自由文字，脚本不查，由 Step 8 的 Check 管 |
| 证据清楚：待验证声明和信息增量 | Still Open `warn`；每个增量进第二版 | 符合 |
| 证据清楚：语义基线、状态与预算 | 语义基线 `not built`；状态来自状态文件；积分只报告 | 部分符合：A·09 没做，预算上限随 A·02 再定 |
| 产物落盘 | Step 1 到 Step 10 记录的产出文件都要在 | 符合 |
| 检查不等于每阶段都要人工确认 | 没有 `fail` 就直接 `done`，只把 `warn` 告诉用户，不停下 | 符合 |
| 阶段门由脚本检查 | `brief_state.py gate` | 符合。课程没展示脚本，检查项是我们按三项检查自己定的 |

课程里没有、我们自己加的：连续两次 `fail` 就停（为了不在同一个错上来回重做）；`fail` 时写明从哪一步重做（依据第 00 课 p.29「哪一步有问题、为什么、怎么修」）。

### 6.3 对照上游原版

上游 `3544423` 的 blog-brief 最后一句是「Confirm the brief is ready for `/blog write`」（原版 SKILL.md 第 290 行），之前没有任何跨文件检查，也没有中间文件可查。

| | 内容 |
|---|---|
| 增益 | 简报交出前，面、增量、材料号、简报和大纲是否对得上，由脚本核对，不靠 Claude 自评；重跑或手改后，引用了没采用的材料会被拦下并指明从 Step 8 重做；待办（支撑页缺失、Still Open、薄弱问题、没做的 A·04 和 A·09）一次摆给用户 |
| 代价 | 多一步：两次脚本调用，输出约 80 行 JSON；SKILL.md 多 1 行，步骤文件 60 行，脚本多约 300 行 |
| 证据 | 单元测试、一次模拟跑、一次真实产物跑（含一次故意弄坏）。正常跑时它挑不出新错，增益主要在重跑和手改之后；真实会话里从 Step 1 跑到 Step 11 还没做过 |

### 6.4 仓库检查

| 检查 | 结果 |
|---|---|
| `pytest tests/` | 1580 通过、6 跳过（4 分 15 秒）。之后改了步骤文件措辞和脚本写法，复跑 `test_brief_state.py`、`test_blog_brief_workflow.py`、`test_editorial_contracts.py` 全过 |
| `validate_skills.py --root .` | 通过 |
| `consistency_check.py --root .` | errors 为空。工作区里还没提交的 blog-write 开发文档会报 6 个 errors，那份文件不在这个分支里 |
| `lint_prose.py` | 本分支的文件 0 处。报出的 43 处都在 `.gitignore` 忽略的课程笔记文件夹里 |

## 7. 提交拆分

```
docs(blog-brief): add design for the A-to-B gate as Step 11
feat(blog-brief): add the A-to-B gate as Step 11
fix(blog-brief): fix gate parsing and acceptance found in review
```

第一个提交只有本文件和上一份文档的状态行。第二个提交是代码、步骤文件、测试和本文件第 6 节的结果。第三个提交是审查后的修改。
