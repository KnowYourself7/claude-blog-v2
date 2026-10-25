# 开发文档：按瑜东 A·08 卡片修正信息增量清单

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已合并（#16） |
| 分支 | fix/blog-brief-a08-gain-list |
| 依据 | 瑜东 A·08 步骤卡片（p.121-122）；第 04 课「步骤 08：规划信息增量」；第 05 课 A·10 自审和第二版（p.125） |
| 修正对象 | PR #14 合并的 Step 7，原开发文档 `docs/plans/2026-10-23-blog-brief-a08-information-gain.md` |

## 1. 目标

信息增量清单只列几样读者能用的东西，并写清每样需要什么证据；简报不再把清单抄一遍，只标出每样东西放在哪一节。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 删简报里其他重复的数字。Key stat、Statistics to Include、Evidence-Backed Section Plan、Visual Element Plan 仍会重复证据计划里的数字 | 路线图第 7 个分支 feat/blog-brief-a10-outline，重做大纲时一起处理 |
| 改大纲 Cover 行的其他写法。这次只加两条：写这一节为增量做什么，写收窄后的说法 | 同上 |
| 终稿回看增量有没有兑现。卡片写了要回看，但它发生在终稿阶段（第 07 课原稿验收） | 以后再定，可能放进路线图第 9 个分支 |
| 改 Step 4 差距清单、Step 6 证据计划 | 不需要改：它们的产物照旧当 Step 7 的输入 |
| 给增量条数设上限。Ebestron 有 4 条，但课程没给规则 | 不设 |
| 任务单补「可公开的一手资料」一栏（瑜东 p.107 有，我们的任务单没有） | 以后改 Step 1 时再定。这次第一方证据照旧按用户在对话里给的写 |
| 修 `skills/blog-brief/templates/competitor-gaps.md` 注释里的旧路径（写成 step-5，应为 step-4） | 单独一个小修正 |

## 3. 原因

### 3.1 现在的问题

例子是 Coofandy「can you wear linen in winter」的证据计划重跑。产物在 `rerun-2026-10-23-evidence-plan/` 文件夹。

1. 增量清单有 11 行：差距 G1 到 G10 各一行，格式优势一行。每行的 This post adds 抄了证据计划里的数字。例如 I1 写了「about 0.65 clo ... 70-77°F (21-25°C)」，这些数字证据计划的 Finding 列已经有了。
2. I10 写的是「the post makes no sustainability claim」。这是一条禁令，不是读者多得到的东西。a07 开发文档已经把它记成遗留问题：G10 写不出读者收益，和「每条差距一行」冲突。
3. 简报第 50 到 61 行把 11 行原样又抄一遍。原因是 Step 8 有一条检查：每条增量都要出现在 Information Gain Opportunities 段。
4. 结果同一个数字在一份简报里出现很多次。空气透气率 91.34 出现了 6 次：增量段、大纲 Chart 行、Key stat 行、统计表、证据段落计划、配图计划。

### 3.2 问题从哪一步进来

问题出在 Step 7 的设计，不是模型没照做。「每条差距写一行」和「Main Gain」都是 PR #14 加的，A·08 卡片里没有。

卡片和现在的 Step 7 逐项对照：

| 卡片项 | 卡片原文（p.121-122） | 现在的 Step 7 |
|---|---|---|
| 输入 | 差距清单、证据计划 | 另加了任务单 |
| 动作 1 | 规划新增：因素之间如何相互影响、带条件的比较表、读者可执行的检查步骤 | 没有这三类，改成一条差距写一行 |
| 动作 2 | 写明证据要求：数据与案例的归属；区分实测、推算、示例 | Evidence 列抄来源和数字，不写归属，不分实测、推算、示例 |
| 产物 | 信息增量清单（终稿阶段要回看是否兑现） | 有，另加了 Main Gain 一句 |
| 红线 | 专有数据追溯到客户资料；外部实验不写成「我们的实验」；缺证据就缩小结论 | 有 |
| 案例 | Ebestron 4 条：故障速查表、症状到部件索引、60 秒排查顺序、时间概念卡 | 11 条，每条是一组事实 |

Ebestron 的 4 条，每条都是一样东西：一张表、一个排查顺序、一张概念卡。增量单写的是它的结构和作用，例如「症状 → 可能原因 → 动作 → 部件」，不写数字。

简报这边，第 05 课说大纲第二版要「确定表格、案例、内链的位置」，还说「不把大纲做成长篇提示词」（p.125）。所以简报要做的是标出每样增量放在哪一节，不是把增量全文再写一遍。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| `templates/information-gain.md` | 要填的表 |
| `briefs/[slug]-competitor-gaps.md` | Our Difference：主增量从它来；Gap List 和 Format Advantage：还缺什么 |
| `briefs/[slug]-evidence-plan.md` | 采用的材料：每条增量的证据和归属 |
| `briefs/[slug]-task-brief.md` | 只读 Does not sell or claim 一行：哪些增量不能写 |

任务单是唯一留下的卡片外输入。留下的原因：「不能说的话」目前只有 Step 7 在查。Step 3 读任务单只为筛掉业务范围外的词。去掉后，整个 blog-brief 不再检查客户不让说的话。它对应第 01 课的业务边界（p.107，例子是「不能冒称生产胶水配方」），不是新编的规则。

Our Difference 要读。Ebestron 的本篇差异是「把跨部件的诊断组织成表」（p.118），增量单第一条 7-Symptom Fault Finder 正是这张表（p.122）。增量就是把本篇差异变成读者能用的东西。

### 4.2 处理步骤

1. 读 Our Difference，先规划把它落地的那一条或几条增量。
2. 读 Gap List 和 Format Advantage。读者能因此多理解、多判断或多完成什么，才再加一条增量。p.121「三列思路」的三行是例子，不是分类：说明因素怎么相互影响、带条件的比较表、读者能照做的检查步骤。Ebestron 的时间概念卡就不属于这三样。
3. 每条增量写一行。中间三列照 Ebestron 增量单（p.122）：增量是什么东西（速查表、索引、排查顺序、概念卡）、名称、作用。作用用一行写结构，最后落到读者能理解、判断或完成什么，例如「症状 → 可能原因 → 动作 → 要检查的部件」，不复述证据计划里的结论和数字。前面加一列「排名页面现在给了什么」，一行就够，对应卡片标题的「已有内容给了什么」。
4. 最后一列是证据要求，这是卡片动作 2 要求的。用一两句写：证据计划里的哪几份材料，数据是谁的（归属），数字是实测、推算还是示例。每行都写清归属，不写「来源同 I2」。缺证据的部分再写收窄后的说法。
   - 实测：有人测出来或数出来的数，例如实验、调查、产品规格里的数。
   - 推算：从别的数或模型算出来的数。
   - 示例：为了说明而编的数。
5. 有 `DISCOURSE.md` 时，它的主题也是增量的来源。这一条原来只写在 SKILL.md 里，Step 7 没提。
6. 第一方证据照旧：只写用户给的方法、证据和结果，没有就写 none supplied。Ebestron 增量单最后一行也是这一项。

规则沿用现在的五条，都有出处：多写、多抓、换说法不算增量（p.53）；给框架起名字不等于证明有效（p.122）；外部实验不写成客户的（p.121）；缺证据就缩小结论，不保留说法再加免责（卡片红线）；不写任务单禁止的增量（p.107）。

### 4.3 输出

`briefs/[slug]-information-gain.md`：

| 段或列 | 写什么 | 进不进简报 |
|---|---|---|
| ID | I1、I2 这样的编号 | 进：大纲每个 H2 写它兑现哪几个 ID |
| The ranking pages give | 一行：排名页面现在给了读者什么 | 不进 |
| Gain | 增量是什么东西：速查表、索引、排查顺序、概念卡等 | 不原样抄。Step 8 在对应 H2 的 Cover 行用自己的话写 |
| Name | 短名称，例如 7-Symptom Fault Finder | 同上 |
| Use | 一行结构，例如「症状 → 可能原因 → 动作 → 部件」 | 同上 |
| Evidence requirement | 一两句：材料编号、归属、实测或推算或示例；缺证据时写收窄说法 | 只进两样：收窄后的说法、推算或示例的标记。Step 8 写进对应 H2 的 Cover 行 |
| First-Party Evidence 段 | 用户给的方法、证据和结果，或 none supplied | 不进。Step 8 读它，判断能不能写第一手经验 |

删掉的：Main Gain 段（卡片里没有，内容就是 Our Difference）；Facet 列；以及本分支第一版加的 Kind、From gap 两列（课程的增量单里没有）。

### 4.4 下游怎么变

- Step 8 生成简报，原规则让大纲抄 This post adds 和 Evidence 两列。改成三条规则：
  1. 把每条增量放进兑现它的 H2，在这些 H2 的 Gains 行写 ID。
  2. Cover 行用自己的话写这一节为这条增量做什么，不抄增量清单的格子。
  3. 证据要求里有收窄后的说法，就写进 Cover。有推算或示例的数字，也在 Cover 里说明。
- Step 8 的检查：原来要求每条增量都出现在增量段，改成每个增量 ID 至少出现在一个 H2 的 Gains 行。Step 8 的输入说明加上 First-Party Evidence。
- 简报模板：Information Gain Opportunities 段只留增量文件路径一行；大纲每个 H2 在 Facets 行下面加一行 `Gains: [I1, I3, or -]`。
- SKILL.md：DISCOURSE.md 那句把主题直接当作增量，改成「more sources of gains」：主题可以引出增量，但也要照增量单的格式写。删掉「From gap 那一格写 DISCOURSE.md」那句，因为没有这一列了。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-7-information-gain.md` | 重写 Goal、Steps、Check |
| `skills/blog-brief/templates/information-gain.md` | 删 Main Gain 段；表格换成 ID、The ranking pages give、Gain、Name、Use、Evidence requirement 六列 |
| `skills/blog-brief/references/step-9-generate-brief.md` | 改一条输入说明、一条检查；一条规则换成三条 |
| `skills/blog-brief/templates/brief-template.md` | Information Gain Opportunities 段只留路径；H2 加 Gains 行 |
| `skills/blog-brief/SKILL.md` | DISCOURSE.md 那句改一个词组，删一句 |
| `docs/plans/2026-10-23-blog-brief-a08-information-gain.md` | 状态改成「已合并（#14），Step 7 的表格由修正文档取代」 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 只改简报：增量段只留路径，Step 7 不动 | 增量清单本身仍是一条差距一行、抄数字，和证据计划重复；不符合卡片动作 1 和动作 2 |
| 保留「每条差距一行」，只把 Evidence 改成证据要求 | 行数还跟着差距数走；G10 这种写不出读者收益的差距还会被硬写成一行 |
| 按卡片去掉任务单输入 | Does not sell or claim 这一行只有 Step 7 在读，去掉后 blog-brief 不再检查客户不让说的话 |
| 本分支第一版：每条增量必须属于三类之一，表格六列（Kind、From gap、The ranking pages give、This post adds、Evidence requirement 加 ID），证据要求逐份列出来源 | 用户对照讲解追问后放弃。三类是 p.121 的例子，不是分类；Ebestron 增量单只有增量、名称、作用三列；逐份列来源又把证据计划抄了一遍，真实跑里 I1 一格就有 6 行 |
| 简报增量段每条留一句短话 | 大纲 Cover 行已经写了每样东西怎么写，这一段只会重复；短话还要和清单保持一致，改一处漏一处 |

## 6. 验证

| 验证 | 结果 |
|---|---|
| 仓库检查 | pytest 1518 通过，6 跳过；`validate_skills.py` 通过（要用项目 `.venv` 跑，系统 Python 没有 yaml）；`consistency_check.py` 的 errors 为空；`lint_prose.py` 在跟踪文件里没有违规 |
| 整篇重读 | 删掉一处无意中调换的输入和规则顺序，没有改含义 |
| 新旧对照（子代理） | 找出 4 处要修，都已修：步骤里漏了 `format`；收窄说法和推算、示例的标记不进简报，写手只读简报，红线到写作时失效；Cover 行没要求写增量内容，写手只看到 I1；DISCOURSE.md 那句和「每条属于三类之一」冲突 |
| 模拟跑（子代理，2k dispensing problems 的模拟输入） | 5 行增量。和这次改动有关、已修的：部分有证据的增量怎么写；厂商规格填哪种类型；一条差距能不能进两条增量 |
| 真实跑第 1 次（改前的文件，输出在 `rerun-2026-10-23-gain-list/`） | 4 行增量，G10 没有行。但温度那一节写成「把室内范围当户外参考，不当规则」，正是红线禁止的「保留说法加免责」。原因是部分有证据时没有地方写收窄说法 |
| 真实跑第 2 次（修后的文件，输出在 `rerun-2026-10-23-gain-list-2/`） | 五项核对全部通过：4 行都有类别；This post adds 只写结构和用途，没有证据计划的数字；每份材料写了归属和类型，缺证据的部分写了 none 和收窄说法；简报增量段只有路径；I1 到 I4 都在 H2 的 Gains 行。温度那一节改成按「要加哪一层」分档，室内舒适区只作锚点。91.34 在简报里从 6 次降到 2 次 |
| 用户对照讲解复查（第一版提交之后） | 发现第一版还不符合：三类写成了封闭分类；表格六列，证据一格最多 6 行；删了名称列；不读 Our Difference。按 4.2 和 4.3 改成增量单的样子 |
| 真实跑第 3 次（新表格，输出在 `rerun-2026-10-24-gain-list-3/`） | 3 行，形状对了：增量、名称、一行作用、两句证据要求。但子代理把「Plan one more gain only if」读成最多再加一条，颜色对比被丢掉。已改成「Plan more gains from them」 |
| 真实跑第 4 次（改措辞后，输出在 `rerun-2026-10-24-gain-list-4/`） | 5 行：单品对温度的表、克重检查清单、面料特性卡、什么时候别穿的清单、颜色卡。I1 和 I2 落地 Our Difference。G10 没有写成增量。I1 到 I5 都在 H2 的 Gains 行，简报增量段只有路径。两个步骤文件的 Check 全部通过 |
| 两版对照（子代理，只按讲解评判） | 新版更符合瑜东：读本篇差异，表格和增量单一致。找出 4 处退步，都已修：作用没落到读者能判断什么；证据要求可以写「来源同 I2」；删了「已有内容给了什么」；Step 7 没提 DISCOURSE.md |
| 真实跑第 5 次（修 4 处后，输出在 `rerun-2026-10-24-gain-list-5/`） | 6 行：单品对温度的表、克重检查清单、面料概念卡、加层阶梯、颜色规则、什么时候别穿。每行的作用都以「他决定、检查或明白什么」结尾，每行都写了归属，没有「同 I2」。I1 到 I6 都在 H2 的 Gains 行。简报 `TL;DR` 里不再有「只能在室内 70-77°F 单穿」那句。两个步骤文件的 Check 全部通过 |

真实跑发现、留给后面分支的问题：

- Cover 行的「Narrower claim」里仍有写给写手的话，例如「No source gives a check for weave density」，有一句还写成「a guide ..., not a measured rule」，接近免责句。留给路线图第 7 个分支重做大纲时处理。
- Step 8 没有任务单输入，内链、CTA、作者、分发计划只能编。留给路线图第 7 个分支。
- 证据计划不记录数字是实测、推算还是示例，Step 7 要自己判断。例如 ASHRAE 舒适区，子代理凭自己的知识标成推算。
- 模拟跑只对第一版做过。

## 7. 提交拆分

1. `docs(blog-brief): add design for the A·08 gain list fix`，同时更新原开发文档的状态
2. `fix(blog-brief): plan information gains by kind and stop copying them into the brief`
