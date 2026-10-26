# 开发文档：状态文件记录每步进度，最后过 A→B 阶段门

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 2026-10-25 用户确认方案。第一个分支已合并（#19）；第二个分支已合并（#21），细化方案见 `docs/plans/2026-10-25-blog-brief-gate-a-to-b.md` |
| 分支 | 两个分支，先后做：`feat/blog-brief-run-state`（状态文件），`feat/blog-brief-gate-a-to-b`（阶段门）。都等 `feat/blog-brief-workflow-checklist` 合并后从 `main` 开，因为两个都要读它加的可勾选清单 |
| 依据 | 第 05 课 A→B 阶段门（p.127）；第 01 课任务状态文件 `_blog_workflow_state.json`（p.108）；第 00 课「每一步都有明确输入、产物和验收」（p.106）和质量门要说清「哪一步有问题、为什么、怎么修」（p.29）；Anthropic 官方 Prompting best practices「State management best practices」和 Skill authoring best practices「Create verifiable intermediate outputs」，原话见第 3.3 节 |
| 路线图 | `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节第 2 行（原名 run-folder）和第 8 行 |
| 来源 | `docs/reviews/2026-10-25-blog-brief-vs-yudong-phase-a.md` 的建议第 1 条 |

## 1. 目标

跑 blog-brief 时，每一步做到哪、停下时问了用户什么、用户怎么选的，都记在一个状态文件里；中途断了，新会话从第一个没做完的步骤接着跑。全部步骤做完后，脚本过一次 A→B 阶段门，告诉用户能不能交给 `/blog write`，不能的话是哪一步出了问题。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| A·04 竞争机会、A·09 语义基准 | 各自单独开分支。阶段门对这两项写 `not built`，不算失败 |
| 预算上限和余额检查（p.109） | 随 A·02「先复用，再补研究」的分支一起定。阶段门只报告 Step 4 和 Step 6 已经写在文件里的积分数 |
| 每次接口调用记一条日志（原型的 `api_calls`） | 不做。Step 4 的 Data Scope 和 Step 6 的 Search Plan 已经记了次数和积分 |
| 每篇简报一个文件夹 `briefs/<slug>/`（路线图第 2 行原来的做法） | 不做。要改 9 个步骤文件、模板和测试里的所有路径；续跑只需要状态文件，不需要换文件夹。路线图第 2 行改名为 run-state |
| 逐步停下等用户确认的 step 模式、连续跑的 auto 模式（原型有） | 不做。课程说全程已授权时「检查通过后继续执行」（p.127），现在的 skill 本来就只在标了 Can stop 的地方停 |
| 让 `/blog write` 读阶段门结果，没过就不写 | 路线图第 9 个分支 `feat/blog-write-use-brief` |
| 阶段门检查「收窄说法是否真的更窄」「核心答案是否回答了问题」这类要判断的事 | 不做。这些由 Step 8 的 Check 管，脚本判断不了 |

## 3. 原因

### 3.1 现在的问题

1. 进度只在对话里。SKILL.md 让 Claude 把清单抄进回复、做完一步勾一步。会话断了或上下文被压缩，新会话只能看 `briefs/` 里有哪些文件来猜。但文件在不等于这一步的 Check 过了：写到一半断掉的文件也在。
2. Step 5 的结果只在对话里。`step-5-template-recommendation.md` 写的是「Output: no file」，选的模板和理由靠对话带到 Step 9。断在 Step 5 和 Step 9 之间，选择就丢了。Step 9 也一样：它把填好的简报交给 Step 10 保存，中间不落盘。
3. 停下时用户怎么选，有的步骤没处记。Step 2 有 User choice 一格；Step 3 第 11 条「保留面少于 3 个就停下问用户」，用户选了「照写」之后，没有文件记这个选择。
4. 重跑一步后，下游文件是旧的，没人提醒。真实例子：Coofandy「can you wear linen in winter」测试新写法时，Step 6 重跑了 1 次，Step 7 重跑了 7 次（其中 1 次跟着 Step 6），Step 8 重跑了 2 次。每次都是手工新建一个文件夹（`rerun-2026-10-24-gain-list-5/`、`rerun-2026-10-24-outline-2/` 等），只放这次改过的文件。现在要知道 `outline-2` 的大纲用的是哪一版证据计划，只能翻测试笔记。
5. 没有阶段结束时的总检查。Step 9 的 Check 只看简报和大纲是否一致。方向、结构、证据三样是否都清楚（p.127），没有一处一起看，也没有一条记录写着「这次简报过了没有」。

还没有发生过的：真实测试里还没遇到过会话中途断掉。第 1 条到第 3 条是按流程长度推出来的风险，不是已经看到的故障。

### 3.2 阶段门能挑出什么错

2026-10-25 用 Coofandy 第 2 次大纲真实跑（`rerun-2026-10-24-outline-2/`）手工模拟了一遍跨文件检查：

| 检查 | 结果 |
|---|---|
| 第二版引用的材料号都是 `adopted` | 13 份全是 |
| 每个保留面都进了第二版 | 9 个全进了，没有多出来的面 |
| 每个增量都进了第二版 | 6 个全进了 |

也就是说，步骤自己的 Check 已经把这些挡住了，正常跑一遍时阶段门挑不出新错。它的用处在三个地方：

1. 重跑和手改之后。重跑 Step 6 删掉一份材料，或者用户手改了大纲，步骤 Check 不会回头查下游；阶段门会。
2. 步骤 Check 是 Claude 自己判断自己。阶段门的机械检查交给脚本，结果不受 Claude 自评影响。
3. 留一条记录，并把还没解决的事一次摆给用户：Still Open、证据不够的问题、缺失的支撑页、没做的 A·04 和 A·09。

所以阶段门做小：只做脚本能查的跨文件检查，加一张待办清单。判断类的检查留在各步骤里。

### 3.3 依据

课程：

- A→B 门三项：方向清楚（关键词与搜索意图；读者任务和页面职责；竞争机会与风险处置）、结构清楚（需求面与第二版大纲；章节、常见问题、内链；计算器候选的取舍）、证据清楚（研究计划与来源线索；待验证声明和信息增量；语义基线、状态与预算）（p.127）。
- 产物落盘：「这些文件让任务中断后能恢复，也让下一阶段知道哪些判断已经作出、哪些仍待验证。」（p.127）
- 「全程已授权时，阶段检查通过后继续执行；检查不等于每阶段都要人工确认。」（p.127）
- 阶段门由脚本检查，课程说「不必逐条讲解内部脚本命令」（p.127），没有展示脚本。
- 质量门要能回答「哪一步有问题、为什么、怎么修」（p.29）。

Anthropic 官方文档：

- Prompting best practices，State management best practices：任务状态这类结构化信息用 JSON，让 Claude 清楚格式要求（"use JSON or other structured formats to make schema requirements explicit"）。新会话从本地文件恢复状态，例子是先读 `progress.txt` 和 `tests.json`。https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Skill authoring best practices，Create verifiable intermediate outputs：中间产物用脚本校验，「Scripts provide objective verification」，出错信息要指明具体问题。Feedback loops：校验、修、再校验。https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- 本项目 CLAUDE.md：脚本要有 docstring、命令行接口和 JSON 输出。

## 4. 方案

一个新脚本 `skills/blog-brief/scripts/brief_state.py`，标准库实现。第一个分支做 `init` 和 `set` 两个子命令，第二个分支加 `gate`。

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| `SKILL.md` 的 Brief Progress 清单 | 脚本从这里读每一步的编号、名字和产出文件。清单是唯一的步骤登记处，脚本里不再抄一份 |
| `briefs/[slug]-state.json` | 状态文件本身 |
| 各步骤的产出文件（第二个分支） | 阶段门检查的对象，见 4.3 |

### 4.2 第一个分支：状态文件

状态文件 `briefs/[slug]-state.json`：

```json
{
  "schema_version": 1,
  "slug": "can-you-wear-linen-in-winter",
  "focus_keyword": "can you wear linen in winter",
  "created": "2026-10-25",
  "steps": {
    "1": {"status": "done", "outputs": ["briefs/can-you-wear-linen-in-winter-task-brief.md"], "note": "", "updated": "2026-10-25T09:12:00Z"},
    "5": {"status": "done", "outputs": [], "note": "Template: how-to-guide. Reason: four of five ranking pages are step guides.", "updated": "..."}
  }
}
```

`status` 只有四种：`pending`（没开始）、`in_progress`（在做）、`done`（Check 全过）、`stopped`（停下问用户，`note` 写问题）。

处理步骤：

1. Step 1 写第一个文件之前，先跑 `init --slug [slug] --focus "[keyword]"`（`--out` 默认 `briefs`，从项目根目录跑）。续跑时用状态文件里的 slug 和焦点词再跑一次 `init`；焦点词对不上，脚本报错。
   - 没有状态文件：新建，每步 `pending`。
   - 有状态文件，就是续跑：`done` 的步骤逐个核对产出文件还在，缺了就改回 `pending`；`in_progress` 改回 `pending`，整步重做，因为它的半成品不可信；没有产出文件、`note` 也空的 `done` 步骤（Step 9）改回 `pending`。然后从第一个不是 `done` 的步骤起，后面的步骤全部改回 `pending`。
   - 输出 JSON：下一步是第几步、每步状态、`stopped` 步骤的问题。
2. 开始一步前跑 `set --step N --status in_progress`。前面有哪一步不是 `done`，脚本报错，保证按顺序做。如果后面已经有不是 `pending` 的步骤（这是重跑），脚本把它们全部改回 `pending`，并在输出的 `reset` 里列出来。这就是 3.1 第 4 条要的「重跑后下游作废」。
3. 这一步的 Check 全过后跑 `set --step N --status done`。这一步必须先是 `in_progress`。脚本核对清单里写的产出文件都在，不在就报错（JSON `{"error": ...}`，退出码 1），写明缺哪个文件；`competitor-[n].md` 要至少有一个带数字的文件。没有产出文件的步骤用 `--note` 记结果：Step 5 写模板名和理由。简报存到别处时，用 `--file` 给出实际路径。
4. 停下问用户时跑 `set --step N --status stopped --note "[问题]"`，没有 `--note` 脚本报错。用户回答后跑 `set --step N --status in_progress --note "[用户的选择]"`。

状态文件先写到临时文件再改名，写到一半断掉也不会留下半个文件。

下游怎么变：

- SKILL.md 在清单下面加一段 State File，4 条对应上面 4 条，最后一句：脚本报错就先修，`set` 没接受 `done` 不进下一步。
- 清单 Step 5 一行只留「Output: no file.」；Step 5 步骤文件的 Outputs 改成写进状态文件 Step 5 的 note。
- Step 9 的 Inputs：「The template and the reason from Step 5」改成读状态文件里 Step 5 的 note。

### 4.3 第二个分支：A→B 阶段门

清单加 Step 11「A→B Gate」，步骤文件 `references/step-11-a-to-b-gate.md`。放在最后，不插在 Step 9 前面，这样前面 10 步都不用改编号。

处理步骤：

1. 跑 `gate --slug [slug]`。脚本逐项检查，每项给 `pass`、`fail`、`warn` 或 `not built`，`fail` 的项写明要重做的步骤。结果写进状态文件的 `gate` 段，同时输出 JSON。
2. 有 `fail`：对要重做的最早那一步跑 `set --status in_progress`（下游自动作废），从那一步重做，再跑 `gate`。连续第二次 `fail`，停下，把 `fail` 项摆给用户。连续两次就停是本项目的规则，课程没写，为了不让 Claude 在一个错上来回重做。
3. 没有 `fail`：把 `warn` 和待办清单摆给用户，说明简报可以交给 `/blog write`。原 Step 10 最后一句「Confirm the brief is ready for `/blog write`」挪到这里。

检查项：

| 门（p.127） | 检查 | 不过时 | 重做 |
|---|---|---|---|
| 落盘 | 清单里 Step 1 到 Step 10 的产出文件都在，状态都是 `done` | fail | 第一个缺的步骤 |
| 方向 | search-intent 的 Decision 是 `continue`，或 User choice 是 `write anyway` | fail | Step 2 |
| 方向 | 任务单的 Page this post supports 不是 `missing` | warn | - |
| 方向 | 竞争机会 | not built | - |
| 结构 | 每个保留面都在第二版某个 H2 的 Facets 行；Facets 行没有保留面以外的 ID | fail | Step 8 |
| 结构 | 增量文件的每个 ID 都在第二版某个 Gains 行 | fail | Step 8 |
| 结构 | 第一版的 Calculator 行已填写 | fail | Step 8 |
| 结构 | 简报的 Content Outline 和第二版一致 | fail | Step 9 |
| 证据 | 第二版每个 Evidence 行引用的材料号，在证据计划里都是 `adopted` | fail | Step 8 |
| 证据 | 第二版每个 H2 有材料号，或者 Narrower claim 不是 `-` | fail | Step 8 |
| 证据 | 证据计划里 Weak 为 `yes` 的问题 | 有就 warn，列出来 | - |
| 证据 | 第二版的 Still Open | 不是 `none` 就 warn，列出来 | - |
| 证据 | 语义基线 | not built | - |
| 证据 | 积分：Step 4 Data Scope 的 Fetch 行和 Step 6 Search Plan 的 Actual credits | 只报告数字 | - |

输出：状态文件加一段

```json
"gate": {"result": "warn", "checked": "2026-10-25T10:02:00Z", "attempt": 1,
         "items": [{"gate": "evidence", "check": "Still Open", "result": "warn", "detail": "1 claim: no comfort range for the cold band", "redo": null}]}
```

`result` 取最重的一项：有 `fail` 就是 `fail`，否则有 `warn` 就是 `warn`，否则 `pass`。`not built` 不影响结果。

下游怎么变：

- SKILL.md 清单加 Step 11 一行，标 Can stop。Step 10 去掉最后一句。
- `tests/test_blog_brief_workflow.py` 的步骤数从 10 改成 11。
- CLAUDE.md 的 blog-brief 目录说明：步骤文件 10 个，scripts 下多一个脚本。

### 4.4 改动文件

第一个分支：

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/scripts/brief_state.py` | 新建：`init`、`set` |
| `tests/test_brief_state.py` | 新建，13 项：清单解析、新建、焦点词不符、按顺序、done 前须 in_progress、缺文件报错、记录产出、带数字的文件、stopped 须有问题、重跑作废下游、续跑从缺文件那步重做、无文件步骤靠 note 保留、`--file` |
| `skills/blog-brief/SKILL.md` | 清单下加 State File 段；Step 5 一行只留 Output: no file. |
| `skills/blog-brief/references/step-5-template-recommendation.md` | Outputs 改成写进状态文件 Step 5 的 note |
| `skills/blog-brief/references/step-9-generate-brief.md` | Inputs 改读状态文件里 Step 5 的 note |
| `CLAUDE.md` | blog-brief 的 scripts 说明加 `brief_state.py` |
| `docs/plans/2026-10-22-blog-brief-step-files.md` | 路线图第 2 行改成 run-state，写明不换文件夹 |
| `docs/reviews/2026-10-25-blog-brief-vs-yudong-phase-a.md` | 新增：本文件第 1 行「来源」引用的对照评估 |
| 本文件 | 第 6 节填实际结果 |

第二个分支：

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/scripts/brief_state.py` | 加 `gate` |
| blog-brief 的 `references/step-11-a-to-b-gate.md` | 新建。路径不写全，否则第一个分支提交本文件时 `consistency_check.py` 会报文件不存在 |
| `tests/test_brief_state.py` | 加阶段门测试：全过、每类 fail、warn、连续两次 fail |
| `skills/blog-brief/SKILL.md` | 清单加 Step 11，Step 10 去掉最后一句 |
| `tests/test_blog_brief_workflow.py` | 步骤数改成 11 |
| `CLAUDE.md` | 步骤文件数改成 10 |

测试用的简报文件自己编，不用 Coofandy 的真实产物，因为那是客户资料。

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 不要状态文件，看 `briefs/` 里有哪些文件判断进度 | 文件在不等于 Check 过了；Step 5、Step 9 没有文件；停下时用户的选择没处记 |
| 状态文件由 Claude 直接编辑 JSON，不写脚本 | 每步两次手改，容易写坏格式；续跑和「重跑后下游作废」的规则要写成一大段文字让 Claude 照做。这类每次结果都该一样的操作，官方建议交给脚本 |
| 状态文件写成 Markdown 表 | 官方建议任务状态用 JSON，格式要求更明确；脚本读写也更稳 |
| Step 5 单独写一个文件 | 多一个模板和一个文件，只为存两句话。状态文件的 note 够用，而且 Step 9 同样问题也一并解决 |
| 阶段门插在 Step 9 之前 | 简报只是照抄第二版，门放在前面能少生成一次简报。但 Step 9、Step 10 要改编号，所有提到它们的文件、测试和旧开发文档都要跟着改（A·10 分支就因此改了 3 份旧文档） |
| 阶段门由 Claude 按清单逐项判断，不写脚本 | 和各步骤的 Check 重复，又是 Claude 自己判断自己。课程的阶段门由脚本检查（p.127） |
| 两件事一个分支做完 | 本项目一个分支只做一个功能。状态文件不依赖阶段门，可以先合并先用 |

## 6. 验证

### 6.1 第一个分支（状态文件）

| 验证项 | 结果 |
|---|---|
| 先看到失败 | 先写 13 项测试，脚本还不存在时收集就报错；写完脚本后 13 项全过 |
| 仓库检查 | pytest 1560 项通过、6 项跳过；`validate_skills.py` 通过；`consistency_check.py` 先报 2 个 errors：对照评估文档引用了两份还没提交的文件，改成只写名字后为空；`lint_prose.py` 先报 8 处，全是对照评估文档里页码范围的 en-dash，改成连字符后为 0 |
| 整篇重读 | 删了一处重复：Step 5 的结果写进 note，原来在清单行、Step 5 文件、State File 段说了三遍，清单行改回只写 Output: no file.。脚本里一行同时判断找到和缺失的代码拆成 if/else |
| 模拟续跑（子代理，Haiku，只读 SKILL.md） | 现场：Step 1 到 4 已完成，Step 5 做到一半。子代理跑 `init` 得到 reset [5]、next_step 5，接着把 Step 5 记成 done 并写 note，再开始 Step 6，全部按说明走。它提的疑问：没写去哪找状态文件（它用 `ls` 找到的），已在 State File 第 1 条补「find its state file in `briefs/`」；没提 `--out`，默认值就是 `briefs`，不补；另外几条是模拟限制它不读步骤文件，或本分支之前就有的 `orchestration-details.md` 那句，不在本次范围 |
| 真实跑 | 没有做。要在 claude-seo-playground 开会话、付费调接口。下次真实跑 blog-brief 时顺带做：做完 Step 6 后结束会话，开新会话说「继续」，看是否从 Step 7 开始、Step 5 的模板还在；再重跑 Step 6，看 Step 7 到 Step 10 是否改回 `pending` |
| 对照瑜东（提交前评估） | 五项里四项符合，一项部分符合，见 6.2 |
| 对照上游原版（提交前评估） | 上游没有可以续跑的东西；增益未经真实跑验证，见 6.3 |

### 6.2 对照瑜东第 00、01、05 课

| 课程要求 | 现在 | 结论 |
|---|---|---|
| 任务状态文件，记录任务做到哪一步（p.108 `_blog_workflow_state.json`） | `briefs/[slug]-state.json`，每步一个状态 | 符合。文件名不同：课件说表名是教学用名 |
| 落盘文件「让任务中断后能恢复」（p.127） | `init` 续跑：缺文件或做到一半的步骤重做，从第一个没完成的步骤接着做 | 符合。只有模拟跑，没有真实中断过 |
| 让下一阶段知道「哪些判断已经作出、哪些仍待验证」（p.127） | 状态和 note 记下已做的判断和用户的选择；「仍待验证」要等阶段门汇总 | 部分符合，第二个分支补 |
| 全程已授权时检查通过就继续，不每步等人确认（p.107、p.127） | 脚本不加任何停点，只在步骤文件写了 Can stop 的地方停 | 符合 |
| 每步有输入、产物和验收（p.106） | 产出文件不在，`set` 不接受 `done` | 符合 |

课程里没有、我们自己加的：必须按顺序做；重跑一步后下游改回 `pending`；`stopped` 状态和 note；先写临时文件再改名。来源是 3.1 的问题和 Anthropic 状态管理建议；做法参照了原型的结构（只参照结构，不作内容依据）。

### 6.3 对照上游原版

上游 `3544423` 的 blog-brief 是一个 SKILL.md，整个流程只在最后存一个 brief 文件，没有进度记录，也没有可以续跑的中间文件。

| | 内容 |
|---|---|
| 增益 | 断了能接着做，不用从头再付一遍接口费用；重跑一步时下游自动作废，不会拿旧文件往下走；Step 5 的模板不再只存在对话里 |
| 代价 | 每步多两次脚本调用，10 步共 20 次左右，每次输出约 20 行 JSON；SKILL.md 多 24 行 |
| 证据 | 只有单元测试和一次模拟续跑。真实跑中的增益未验证 |

### 6.4 第二个分支（阶段门）：打算怎么验

| 验证项 | 打算怎么验 |
|---|---|
| 仓库检查 | 同 6.1 |
| 脚本单元测试 | 阶段门的每个 `fail` 至少一个用例，用例里故意弄坏一处，看它是否指对要重做的步骤 |
| 整篇重读 | 每个改过的文件从头读，每句问谁需要、删了坏什么、别处是否已写 |
| 真实跑：阶段门 | 对 Coofandy 第 2 次大纲真实跑跑 `gate`，预期没有 `fail`（手工模拟已对上）。再复制一份，把大纲里一个材料号改成 `rejected` 的那份，预期 `fail` 并指向 Step 8 |
| 对照瑜东、对照上游（提交前评估） | 同 6.2、6.3 的做法 |

## 7. 提交拆分

第一个分支 `feat/blog-brief-run-state`：

```
feat(blog-brief): record step progress in a state file so a run can resume
```

本文件、路线图改动和 CLAUDE.md 的说明随这个提交一起。

第二个分支 `feat/blog-brief-gate-a-to-b`：

```
feat(blog-brief): add the A-to-B gate as Step 11
```
