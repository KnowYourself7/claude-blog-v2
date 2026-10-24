# 开发文档：按瑜东 A·08 卡片修正信息增量清单

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已实现，待合并 |
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
| `briefs/[slug]-competitor-gaps.md` | Gap List 和 Format Advantage：排名页面现在给了什么、缺什么 |
| `briefs/[slug]-evidence-plan.md` | 采用的材料：每条增量的证据和归属 |
| `briefs/[slug]-task-brief.md` | 只读 Does not sell or claim 一行：哪些增量不能写 |

任务单是唯一留下的卡片外输入。留下的原因：「不能说的话」目前只有 Step 7 在查。Step 3 读任务单只为筛掉业务范围外的词。去掉后，整个 blog-brief 不再检查客户不让说的话。它对应第 01 课的业务边界（p.107，例子是「不能冒称生产胶水配方」），不是新编的规则。

不再读 Our Difference。它原来只用来写 Main Gain。

### 4.2 处理步骤

1. 读 Gap List 和 Format Advantage，按下面三类规划增量。每一类可以有零条，也可以有几条。

   | 类别 | 意思（p.121） | 课程里的例子 |
   |---|---|---|
   | 因素怎么相互影响 | 排名页面只列了影响因素，这篇说明因素怎么一起起作用 | 课程没给具体例子 |
   | 带条件的比较 | 排名页面只给通用定义，这篇给一张写明条件的比较表 | 7-Symptom Fault Finder：症状 → 可能原因 → 动作 → 部件 |
   | 读者能照做的检查步骤 | 排名页面只给宽泛建议，这篇给一套能照做的步骤 | 60-Second Triage：观察 → 排查 → 核对 → 部件；铝件询价准备清单 |

   Ebestron 第 4 条 Pot-Life Clock 区分几个和操作时间有关的概念，课程没说它属于哪一类。本方案把它算作带条件的比较：几个概念并排，写明各自的条件。

2. 每条增量写一行：类别、来自哪些差距、排名页面现在给了什么、这篇多给什么。一条差距可以进几条增量。「这篇多给什么」用一两句写这样东西的结构和作用，例如表格有哪几列、步骤按什么顺序，不复述证据计划里的结论和数字。
3. 写证据要求：用到证据计划里哪几份采用的材料，每份是谁的数据（归属），每个数字是实测、推算还是示例。归属指做出数据的人或公司；数据是别的网站转载的，两个都写。增量整条或其中一部分没有采用的材料支持，就给那一部分写 none 和收窄后的说法。
   - 实测：有人测出来或数出来的数，例如实验、调查、产品规格里的数。
   - 推算：从别的数或模型算出来的数。
   - 示例：为了说明而编的数。
4. 不是每条差距都要变成一行。写不出读者能用的东西的差距，例如 G10，不写行。没变成增量的「没回答」「没给判断」差距也不会丢：它们挂在需求面上，Step 8 要求每个保留的需求面至少有一个 H2。
5. 第一方证据照旧：只写用户给的方法、证据和结果，没有就写 none supplied。

规则沿用现在的五条，都有出处：多写、多抓、换说法不算增量（p.53）；给框架起名字不等于证明有效（p.122）；外部实验不写成客户的（p.121）；缺证据就缩小结论，不保留说法再加免责（卡片红线）；不写任务单禁止的增量（p.107）。

按新规则，亚麻衬衫那 11 行大致会合成 4 行左右。这是我的推测，要真实跑确认：

| 类别 | 增量 | 合并的差距 |
|---|---|---|
| 带条件的比较 | 一张表：单品、面料克重、要加的层、合适的室内温度 | G1、G2、G3、G5、G6、格式优势 |
| 因素怎么相互影响 | 亚麻本身为什么不保暖，暖和来自外层，风会抵消静止空气的条件 | G4、G8 |
| 读者能照做的检查步骤 | 看商品页的克重和混纺比例，对照单品范围 | G9 |
| 因素怎么相互影响 | 颜色、阳光、风怎么一起影响冷暖 | G7 |

### 4.3 输出

`briefs/[slug]-information-gain.md`：

| 段或列 | 写什么 | 进不进简报 |
|---|---|---|
| Gains 表 ID | I1、I2 这样的编号 | 进：大纲每个 H2 写它兑现哪几个 ID |
| Kind | factor interaction、conditional comparison、check steps 三选一 | 不进 |
| From gap | 差距编号，或 format、DISCOURSE.md | 不进 |
| The ranking pages give | 排名页面现在给了什么 | 不进 |
| This post adds | 一两句：这样东西的结构和作用，读者能多理解、多判断或多完成什么；不写证据计划的结论和数字 | 不原样抄。Step 8 在对应 H2 的 Cover 行用自己的话写这样东西 |
| Evidence requirement | 证据计划里的材料编号、归属、每个数字的类型；没有支持的部分写 none 加收窄说法 | 只进两样：收窄后的说法、推算或示例的标记。Step 8 写进对应 H2 的 Cover 行 |
| First-Party Evidence 段 | 用户给的方法、证据和结果，或 none supplied | 不进。Step 8 读它，判断能不能写第一手经验 |
| Main Gain 段 | 删掉：卡片里没有，内容和差距清单的 Our Difference 重复 | 原来进，以后不进 |
| Facet 列 | 删掉：差距清单里每条差距已经写了需求面，按 From gap 能查到 | 原来不进 |

### 4.4 下游怎么变

- Step 8 生成简报，原规则让大纲抄 This post adds 和 Evidence 两列。改成三条规则：
  1. 把每条增量放进兑现它的 H2，在这些 H2 的 Gains 行写 ID。
  2. Cover 行用自己的话写这一节为这条增量做什么，不抄增量清单的格子。
  3. 证据要求里有 none，就把收窄后的说法写进 Cover；有推算或示例的数字，也在 Cover 里说明。
- Step 8 的检查：原来要求每条增量都出现在增量段，改成每个增量 ID 至少出现在一个 H2 的 Gains 行。Step 8 的输入说明加上 First-Party Evidence。
- 简报模板：Information Gain Opportunities 段只留增量文件路径一行；大纲每个 H2 在 Facets 行下面加一行 `Gains: [I1, I3, or -]`。
- SKILL.md：DISCOURSE.md 那句把主题当作「more gains」，和「每条增量属于三类之一」冲突。改成「more sources of gains」：主题可以引出增量，但也要归进三类。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-7-information-gain.md` | 重写 Goal、Steps、Check；Inputs 删掉 Our Difference |
| `skills/blog-brief/templates/information-gain.md` | 删 Main Gain 段和 Facet 列；加 Kind 列；Evidence 改成 Evidence requirement，一份材料一行，用 `<br>` 分行 |
| `skills/blog-brief/references/step-8-generate-brief.md` | 改一条输入说明、一条检查；一条规则换成三条 |
| `skills/blog-brief/templates/brief-template.md` | Information Gain Opportunities 段只留路径；H2 加 Gains 行 |
| `skills/blog-brief/SKILL.md` | DISCOURSE.md 那句改一个词组 |
| `docs/plans/2026-10-23-blog-brief-a08-information-gain.md` | 状态改成「已合并（#14），Step 7 的表格由修正文档取代」 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 只改简报：增量段只留路径，Step 7 不动 | 增量清单本身仍是一条差距一行、抄数字，和证据计划重复；不符合卡片动作 1 和动作 2 |
| 保留「每条差距一行」，只把 Evidence 改成证据要求 | 行数还跟着差距数走；G10 这种写不出读者收益的差距还会被硬写成一行 |
| 按卡片去掉任务单输入 | Does not sell or claim 这一行只有 Step 7 在读，去掉后 blog-brief 不再检查客户不让说的话 |
| 加「名称」列，像 7-Symptom Fault Finder | 卡片的动作和产物都没要求起名，还警示起名不等于证明有效；大纲引用增量用 ID 就够了 |
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

真实跑发现、留给后面分支的问题：

- Cover 行的「Narrower claim」里仍有写给写手的话，例如「No source gives a check for weave density」，有一句还写成「a guide ..., not a measured rule」，接近免责句。留给路线图第 7 个分支重做大纲时处理。
- Step 8 没有任务单输入，内链、CTA、作者、分发计划只能编。留给路线图第 7 个分支。
- 证据计划不记录数字是实测、推算还是示例，Step 7 要自己判断。例如 ASHRAE 舒适区，子代理凭自己的知识标成推算。
- 差距清单的 Our Difference 现在没有步骤读。以后再定是删掉还是给 Step 8 写引言用。

## 7. 提交拆分

1. `docs(blog-brief): add design for the A·08 gain list fix`，同时更新原开发文档的状态
2. `fix(blog-brief): plan information gains by kind and stop copying them into the brief`
