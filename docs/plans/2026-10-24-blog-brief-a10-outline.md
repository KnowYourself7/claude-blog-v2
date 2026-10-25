# 开发文档：大纲先写第一版，自审后出第二版

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-24 |
| 状态 | 待合并 |
| 分支 | feat/blog-brief-a10-outline |
| 依据 | 第 05 课「步骤 10：大纲第一版到第二版」（p.125-126）；A→B 阶段门「结构清楚」一行（p.127）；第 07 课计算器和内链的规则（p.132-133） |
| 路线图 | `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节第 7 行 |

## 1. 目标

简报的大纲每一节都写明要回答哪个问题、答案是什么、拿哪份材料来回答；大纲先写第一版，自审，再出第二版，改了什么、还剩什么问题都存成文件。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| A·09 语义基准：术语表分配到章节 | 要 NEURONwriter，路线图暂缓 |
| A→B 阶段门 | 路线图第 8 个分支 feat/blog-brief-gate-a-to-b |
| `/blog write` 直接读大纲和证据表 | 路线图第 9 个分支 feat/blog-write-use-brief |
| 任务单加站内页面清单，让内链和「与同站文章的边界」有输入。第 01 课资料盘点单有「产品网址清单、同站博客清单」（p.110），我们的任务单没有 | 以后改 Step 1 时再定。这次没有清单的地方写 `missing` |
| 改 E-E-A-T、分发计划、封面图、字数这些段。它们不属于 A·10 | 以后再定 |
| 大纲要不要按 Step 5 选的内容模板分节。课程没讲内容模板 | 不改。Step 5 照旧读模板文件，选定的模板照旧写进简报的 Template 段 |
| 计算器怎么做、怎么隔离 | 第 07 课的事。这次只在第一版写一行取舍 |
| 计算器候选是否和已有页面冲突（p.125） | 没有站内页面清单，查不了。随任务单加站内页面清单的分支一起定 |

## 3. 原因

### 3.1 现在的问题

例子是 Coofandy「can you wear linen in winter」第 5 次重跑的简报，文件在 `rerun-2026-10-24-gain-list-5/can-you-wear-linen-in-winter-brief.md`。

1. 8 个 H2 的 Answer-first 行一字不差，都是 `Open with the section's useful conclusion and support it`。大纲没写答案。a07 开发文档已经把它记成遗留问题：「Answer-first 仍是模板空话」。
2. Cover 行每节八十到一百二十个词，还夹着写给写手的话，例如 `Say nothing about how fast linen dries` 和 `No source gives a check for weave density`。第 05 课说「不把大纲做成长篇提示词」（p.125）。
3. 同一份材料的数字在一份简报里出现好几次：大纲的 Key stat 行和 Chart 行、Statistics to Include、Evidence-Backed Section Plan、Visual Element Plan。#16 之后 91.34 从 6 次降到 2 次，其他数字照旧重复。
4. 简报里有两套编号。统计表自己编 1 到 13，配图计划却写证据计划的材料号 8、14、16。同一份 Rani 2019，统计表叫 13，配图计划叫 16。
5. 衬衫、裤子、西装三节的 Gains 都只有 I2。没有一步问过「两节是不是在说同一件事」。
6. 内链 10 条全是猜的：`URL to confirm` 和 `not checked: may not exist`。Step 8 不读任务单，连支撑页都不知道。#16 已经记成遗留问题。
7. 结尾的 Call to action 写 `The task brief gives no supported page`，也是因为 Step 8 不读任务单。

### 3.2 问题从哪一步进来

问题出在 Step 8 的设计：它一次把模板填完。瑜东的大纲分三步（p.125）：

| 瑜东 | 做什么 | 现在的 Step 8 |
|---|---|---|
| 第一版 | 主标题与章节顺序；每节核心答案；常见问题与决策框架 | 没有，直接填简报 |
| 逐项自审 | 意图是否一致；问题是否遗漏或重复；证据和信息增量能否落实 | 没有 |
| 第二版 | 合并重复章节；补齐关键问题与依据；确定表格、案例、内链的位置 | 只有图片和图表的位置 |

讲师备注里的自审四问：读者进来先需要知道什么？是不是先解释概念，却迟迟不回答主问题？两个章节是不是在反复说同一件事？关键结论有没有证据计划？

Ebestron 的大纲修改单（p.126）一行一项「V1 → V2」，最后一行是「反思保留项」：第二版里「几乎都是硬件原因」仍然说得太绝对。表上写着「版本升级不代表里面每句话都正确」。现在的简报没有地方写这种话。

计算器是条件分支：「不是每篇博客都要添加」（p.125），「有公式依据才考虑计算器」（p.133）。A→B 门要求写清「计算器候选的取舍」（p.127）。

## 4. 方案

在 Step 7 信息增量之后，加一步新的 Step 8「大纲」。原 Step 8 生成简报改为 Step 9，原 Step 9 保存改为 Step 10。

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| `templates/outline.md` | 要填的模板 |
| `briefs/[slug]-search-intent.md` | Reader Task：自审「意图是否一致」 |
| `briefs/[slug]-task-brief.md` | Reader decision：决策框架；Page this post supports 和 Reader next step：内链和结尾的行动；Does not sell or claim：不能写的话 |
| `briefs/[slug]-demand-facets.md` | Kept Facets：要回答的问题，每个保留面至少进一个 H2 |
| `briefs/[slug]-evidence-plan.md` | Questions 的 Facet 和 Weak 列：哪个面证据不够；Sources 的 #、Question、Finding、Status、Chart 列：每节拿哪份材料回答，有没有公式，哪里放图表 |
| `briefs/[slug]-information-gain.md` | 增量 ID 和 Use：每节兑现什么；Evidence requirement：收窄说法，推算或示例的标记；First-Party Evidence：能不能写第一手经验或案例 |

### 4.2 处理步骤

1. 写第一版：标题；H2 表，每个 H2 写回答哪几个面、兑现哪几个增量、一句核心答案；决策框架（这篇怎么带读者做完任务单里的那个决定，放在哪一节）。增量列是课程第一版没有的，加上它，自审时才能查「信息增量能否落实」。
2. 常见问题只从保留面里取需要单独短答的问题，放进 FAQ 的面仍要有一个 H2。课程没说常见问题从哪来，这里只用已有的需求面，不另加输入。
3. 计算器：采用的材料里没有公式就写 none；有公式时，判断计算器能不能帮读者做决定，写主计算器、段落计算器或 none，以及取舍的理由（A→B 门要求写「取舍」）。
4. 按四个检查项自审第一版，每项写发现：意图（顺序是否对得上读者任务，第一个 H2 是否先回答主问题）；问题（有没有漏掉的保留面，有没有两节回答同一个问题）；证据（每个核心答案有没有采用的材料或收窄说法）；增量（每个增量有没有一节兑现）。
5. 写修改单：一行一项，写第一版、第二版和理由。写完再把修改编号填回自审表。
6. 写第二版。每个 H2 五行，每行最多两句，每句最多 25 个词：

   ```markdown
   ### H2: Can You Wear Linen in Winter? Yes, as a Layer
   - Facets: F1, F4
   - Answer: Yes, as a layer. Linen lets heat out fast, so the warmth comes from what goes over it.
   - Evidence: 1, 16. Narrower claim: lab values on flat fabric; no warmth figure for a linen outfit.
   - Gains: I3
   - Components: concept card for I3, linen against cotton on three properties; image, a linen shirt under a knit.
   ```

   Evidence 只写证据计划的材料号；增量的证据要求标了推算或示例的，在材料号后面写 `estimated` 或 `example`。Components 只写表格、图表、图片、案例、内链、计算器，每样写它的任务；决策框架和留下的计算器放进它所在那一节；图表只用 Chart 为 yes 的材料；案例只用采用的材料或用户给的第一手证据；内链只连支撑页，支撑页是 `missing` 就不放内链。
7. 第二版最后写 Still Open：第二版里还说得太满、或证据还不够的话，没有写 none。

规则沿用原 Step 8 的五条，都有出处：只用增量文件里的增量，不抄增量清单的格子；大纲不写竞品页面、排名或差距（#14）；缺证据就收窄说法，增量的证据要求里有收窄说法就用它，不保留说法再加免责（第 04 课）；没有用户给的方法、证据和结果，不写第一手经验（原 Step 8）。新增两条：只写材料号，不把材料的数字抄进大纲，数字只在简报的统计表里出现；每行最多两句、每句最多 25 个词，不写成长提示词（p.125）。

### 4.3 输出

`briefs/[slug]-outline.md`：

| 段 | 写什么 |
|---|---|
| Outline V1 | 标题；H2 表（序号、H2、Facets、Gains、核心答案）；FAQ；决策框架；计算器 |
| Self-Review | 四行：检查项、发现、修改编号或 none |
| Changes | 一行一项：编号、修改项、V1、V2、理由 |
| Outline V2 | 标题；Introduction（Hook、Problem、Promise）；每个 H2 五行；FAQ；Conclusion（要点、Call to action）；Still Open |

Still Open 对应 Ebestron 修改单的「反思保留项」。课程把它放在修改单里，这里放在第二版末尾：简报只抄第二版，放在修改单里写手就看不到这句还说过头的话。

### 4.4 下游怎么变

- Step 9 生成简报（原 Step 8）：
  - Content Outline 原样抄第二版（不抄标题行），Recommended Title 用第二版的标题。
  - 输入去掉需求面（覆盖检查挪到 Step 8），加上大纲文件和任务单。信息增量只读 First-Party Evidence，给 E-E-A-T 的 Experience 一行用。
  - 删掉 Key stat 行、Evidence-Backed Section Plan、Visual Element Plan。第二版每节的 Evidence 和 Components 已经写了这些。
  - Statistics to Include 的 # 改用证据计划的材料号，只列第二版引用的材料，一份材料一行，删掉 Section 列（第二版每节的 Evidence 行已经写了它在哪一节）。
  - Content Parameters 的 H2 数量从固定的 6-8 改成第二版的 H2 数。课程没给章节数。
  - Internal Link Architecture 只写任务单的支撑页；其他页面、Link FROM、支柱页、集群位置都写 `missing`，不再猜 URL。
- Step 2、Step 5 步骤文件里的「Step 8」改成「Step 9」。
- SKILL.md 步骤表加一行，Step 9 改成 Step 10。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-8-outline.md` | 新建 |
| `skills/blog-brief/templates/outline.md` | 新建 |
| `skills/blog-brief/references/step-9-generate-brief.md` | 由 `step-8-generate-brief.md` 改名重写：输入、规则、检查 |
| `skills/blog-brief/templates/brief-template.md` | Content Outline 改成抄第二版；删三处重复；改统计表、H2 数量、内链 |
| `skills/blog-brief/SKILL.md` | 步骤表加 Step 8，改 Step 9 的输入，保存改成 Step 10 |
| `skills/blog-brief/references/step-2-serp-intent-gate.md`、`step-5-template-recommendation.md` | 「Step 8」改成「Step 9」 |
| `tests/test_release_safeguards.py` | 第一手经验那条检查改读 `step-8-outline.md` |
| `CLAUDE.md` | blog-brief 目录说明：步骤文件 9 个，模板 10 个，SKILL.md 里是 Step 10 |
| `docs/plans/2026-10-23-blog-brief-a07-evidence-plan.md`、`2026-10-23-blog-brief-a08-gain-list-fix.md`、`2026-10-23-blog-brief-a08-information-gain.md` | 反引号里的 `step-8-generate-brief.md` 改成 `step-9-generate-brief.md`，否则 `consistency_check.py` 报 3 个 errors |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 在原 Step 8 里加第一版、自审、第二版，第二版直接写进简报 | Step 8 同时管大纲和简报其余十几段；第一版和修改单没有文件可存，阶段门要求落盘（p.127） |
| 简报的 Content Outline 只写大纲文件路径，不抄第二版 | `/blog write` 现在只读简报，要到第 9 个分支才改读大纲文件。现在就删，写手拿不到大纲 |
| 删重复的三处留到下一个分支 | 第二版每节已经写证据和组件，中间这段时间简报会把同一件事写两遍，改一处漏一处。用户 2026-10-24 选本分支一起做 |
| 第二版保留一行 Cover，写这一节怎么展开 | 又会长回长提示词。用户 2026-10-24 选五行 |
| 统计表保留 Section 列 | 它是第二版 Evidence 行的反向索引，两处要一起改，迟早对不上 |

## 6. 验证

| 验证项 | 结果 |
|---|---|
| 仓库检查 | pytest 1518 通过，6 跳过；`validate_skills.py` 通过；`consistency_check.py` 的 errors 为空（先报了 3 个：三份旧开发文档还写着 `step-8-generate-brief.md`，已改）；`lint_prose.py` 在跟踪文件里没有违规（43 处都在被忽略的 `docs/yudong/`） |
| 整篇重读 | 改了 4 处：「每行一句」和用户认可的例子冲突，改成一到两句；Step 8 的决策框架和结尾行动两条只重复模板占位符，删掉，出处写进模板；第一版的 FAQ 没有来源，补上只从保留面取；简报模板内链段的说明和 Step 9 规则重复，删掉。另删了统计表下「唯一一张写数字的表」一句，没人需要 |
| 测试 | 第一次跑 1 个失败：`test_release_safeguards.py` 找原句 `only when the user supplies supporting methodology`，新文件把它折成了两行。改回旧文件的折行后通过 |
| 新旧对照（子代理） | 报了 30 来条，修了这些：丢掉的「不抄增量表格子」「收窄说法取自增量的证据要求」「第一手经验的检查」「标题要求」补回；「a gap ID」改回「a gap」；FAQ、计算器、Still Open 的歧义和先后顺序；Still Open 挪进第二版，写手才看得到；第一版加 Gains 列，自审才能查增量；决策框架放进它所在那一节的 Components；Step 8 输入补证据计划的 Facet、Question、Finding 列；Step 9 输入补市场和日期；支柱页和集群位置没有输入，改成固定写 `missing` |
| 模拟跑 | 没有单独做。两次真实跑都要求子代理报告每一处不得不猜的地方，起到了模拟跑的作用，但只用了亚麻衬衫一组输入 |
| 真实跑第 1 次（输出在 Coofandy 工作区 `rerun-2026-10-24-outline/`） | 两步的 Check 全过。第一版 8 节，第二版 6 节，修改单 10 行：合并衬衫、裤子、西装三节，调整顺序，给 I6 加一节，收窄 4 处说法。Still Open 写了一句「冷档没有舒适区间」。问题：「0.65 clo」「21-25°C」在 Answer、Components、FAQ、结尾要点里各写一遍；一行 Components 六十来个词；结尾要点把每节答案又抄一遍；支撑页缺失时仍写了一条 `missing` 内链。据此加了「只写材料号、不抄数字」「每句最多 25 个词」，结尾要点改回固定写法，支撑页缺失就不放内链 |
| 真实跑第 2 次（输出在 `rerun-2026-10-24-outline-2/`） | 两步的 Check 全过。第一版 7 节，第二版 6 节，修改单 9 行，自审抓出「第一节先讲概念、第二节才回答主问题」和「两节用同一张表」。大纲里没有材料数字，最长一句 23 个词；统计表 13 行正好是大纲引用的 13 份材料；内链、Link FROM、支柱页、集群位置都是 `missing`。子代理为了凑「两句」删了 FAQ 问题的问号，已在规则里写明问题和标签不计入 |
| 对照瑜东第 05 课（提交前评估） | 七项里五项符合，两项有偏差，见 6.1 |
| 对照上游原版（提交前评估） | 大纲本身明显更好；但 `/blog write` 还不保证用它，增益要到第 9 个分支才进正文，见 6.2 |

### 6.1 对照瑜东第 05 课

| 课程要求（p.125-127） | 现在 | 结论 |
|---|---|---|
| 第一版：主标题与章节顺序；每节核心答案；常见问题与决策框架 | Outline V1：标题、H2 表（含核心答案）、FAQ、决策框架 | 符合 |
| 逐项自审：意图是否一致；问题是否遗漏或重复；证据和信息增量能否落实。备注四问 | Self-Review 四行，四问写进 Step 8 第 4 条 | 符合。真实跑第 2 次抓出「先讲概念，后答主问题」和「两节用同一张表」 |
| 第二版：合并重复章节；补齐关键问题与依据；确定表格、案例、内链的位置 | 修改单，加上第二版每节五行 | 符合。内链只能连支撑页，因为任务单没有站内页面清单（另开分支） |
| 修改单 V1 → V2，最后一行是反思保留项 | Changes 表；反思保留项叫 Still Open | 有偏差：放在第二版末尾，因为简报只抄第二版，放在修改单里写手看不到 |
| 计算器是条件分支；扫描候选，查适用性和是否与已有页面冲突 | 有公式才考虑，写取舍理由 | 有偏差：与已有页面冲突的检查缺站内页面清单，没做 |
| 不把大纲做成长篇提示词 | 每行最多两句，每句最多 25 个词 | 符合。25 个词是我们定的（simple-english 说明句的上限），课程没给数字 |
| 产物落盘（p.127） | `briefs/[slug]-outline.md` | 符合 |

课程里没有、我们自己加的有三条：第一版的 Gains 列，为了自审能查「增量能否落实」；大纲只写材料号、不抄数字，来自用户 2026-10-24 定的去重；FAQ 只从保留面取，因为课程没说常见问题从哪来。三条都不和课程冲突。

### 6.2 对照上游原版

上游原版是 fork 基点 `3544423` 里 `skills/blog-brief/SKILL.md` 的 Step 5 Generate the Brief：一次填完模板，每节 Answer-first、Cover、Image、Key stat，后面跟统计表、证据段落计划、配图计划，内链 5 条连出、5 条连入。本分支之前的大纲和它一样，只多了 Facets、Gains 两行，所以「改前」用 `rerun-2026-10-24-gain-list-5` 的简报对照。上游自己的研究步骤和这里不同，没有用上游原版完整跑过亚麻衬衫。

| 方面 | 上游原版的大纲 | 本分支（真实跑第 2 次） |
|---|---|---|
| 每节答案 | 8 节都是同一句 `Open with the section's useful conclusion and support it` | 6 节各有一句具体答案 |
| 自审 | 没有 | 4 项发现，9 行修改，每行有理由 |
| 重复章节 | 衬衫、裤子、西装三节都只兑现 I2 | 合成一节 |
| 数字 | 同一份材料的数字在 4 处出现，统计表和配图计划两套编号 | 只在统计表出现，用证据计划的材料号 |
| 内链 | 10 条，全是猜的 | 只写支撑页，缺就写 `missing` |
| 说过头的话 | 没有地方记 | Still Open 一句，写手能看到 |

代价：

- 多一个步骤。真实跑 Step 8 和 9 每次约 10 到 13 分钟、15.6 万到 17.5 万个子代理 token。上游同一步没有单独计过，无法对比。
- 增益还没进正文。`/blog write` 读到简报后，Phase 3 仍按内容模板自己写大纲（`skills/blog-write/SKILL.md` 第 160 行起），不保证用第二版。要到路线图第 9 个分支 feat/blog-write-use-brief 才兑现。
- 写手要拿材料号去统计表查数字，多一步查找。
- 没有用新简报跑过 `/blog write`，正文是否更好，未验证。

留给后面分支的问题：

- 简报里字数、格式、备选标题、Meta、封面图、E-E-A-T 的 Expertise 和 Authority、分发计划仍然没有输入，子代理只能自己写或写 `missing`。
- 简报模板里没改的老段落还有 13 处 simple-english 违规（分号、`Should`、条件放句尾），这次不动。
- Step 5 选的模板照旧只留在对话里，没有文件。

## 7. 提交拆分

1. `docs(blog-brief): add design for the A·10 outline step`
2. `feat(blog-brief): plan the outline in two versions before the brief`
