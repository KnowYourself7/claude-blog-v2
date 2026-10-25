# 开发文档：blog-brief Step 6 从「搜统计数字」改成「证据计划」

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已实现，待提交 |
| 分支 | feat/blog-brief-a07-evidence-plan |
| 依据 | 瑜东 A·07「证据计划」卡片和第 04 课（p.119-120，背景 p.44）；路线图 `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节第 6 行 |
| 已定 | 用户 2026-10-23：查资料用 Exa 找、Firecrawl 抓；产物用 md，等阶段门要脚本检查时再加 JSON |

## 1. 目标

文章里每个影响读者判断的说法，在写大纲之前就有对应的证据，或者被明确标成薄弱项。

## 2. 不做什么

- 不改 Step 7 信息增量的规则，只把它的输入从「上下文里的统计数字」换成证据计划文件。
- 不改大纲每一节的字段（Cover 这些）。这是另一个分支。
- 不加大纲 v1、自审、v2。这是路线图第 7 个分支。
- 不做按章节的深度研究。那是瑜东阶段 B 的 A·11，写作时才做。
- 不改 blog-write 和 blog-reviewer。

## 3. 原因

现在的 Step 6 拿主题去搜「`[topic] study 2025 2026 data statistics research`」，捞 8 到 12 条数字，能核实的就留下，不写文件。

瑜东的做法正好相反。他说研究计划的本质是「问题 → 证据」的映射，不是一张网址列表（p.119）。

亚麻衬衫这篇能看出差别：

1. 最关键的说法是温度分段，也就是「多冷算太冷」，读者靠它做决定。Step 6 按主题搜数字，没有针对它找证据，结果这个说法没有证据，正文里只能写免责句。
2. Step 6 却留下了「linen pants in winter 每月 320 次搜索」。这条能核实，但对读者没用，最后被放进了裤子那一节当 Key stat。
3. Step 6 不落盘，Step 7 信息增量只能读上下文里的数字，违反「产物落盘、下一步读文件」的规矩。

另外，统计数字只是证据的一种。瑜东列的证据类型还有标准、论文、技术文档、厂商资料和真实案例；论坛只能当线索（p.119）。

## 4. 方案

Step 6 改名为「Evidence Plan」，步骤文件改名为 `step-6-evidence-plan.md`，新建模板 `templates/evidence-plan.md`。步骤号不变。

### 4.1 输入

和瑜东卡片一致，只有两份产物，加上要填的模板：

| 输入 | 拿它做什么 |
|---|---|
| `briefs/[slug]-competitor-gaps.md` | 整份差距清单：竞品没讲清、没给证据的地方 |
| `briefs/[slug]-demand-facets.md` | 保留的需求面：读者的问题，也是查询的分组 |
| `templates/evidence-plan.md` | 要填的表 |

### 4.2 处理步骤

按卡片的四个动作：

1. 列关键问题：读者要做什么判断，哪些数字必须核实。每个问题标上需求面编号。
2. 指定证据类型：标准、论文、技术文档、厂商资料、真实案例；论坛只作线索。
3. 安排查询：按需求面分组（瑜东是按章节，我们这一步还没有章节，需求面就是以后的章节）。每组写计划用几次 Exa 搜索、抓几页 Firecrawl，加总成预计花费。查不到或只有论坛线索的问题，标为薄弱项。
4. 抓取后阅读判断：用 Exa 找候选，用 Firecrawl 抓原文，读完给每份材料标状态：采用、参考、拒绝、抓取失败。

规则（卡片的两条红线，加工具规定）：

- 抓过不能冒充用过。只有状态为「采用」的材料能进简报。
- 搜索摘要只用于筛选。正式采用的关键事实，必须读 Firecrawl 抓回的原文，并写下适用条件。
- 找候选用 `mcp__exa__web_search_exa`，抓原文用 `mcp__firecrawl__firecrawl_scrape`。不用 WebSearch。任一工具缺失就停下说明原因。

### 4.3 输出

`briefs/[slug]-evidence-plan.md`，三部分。

查询计划，每个需求面一行：

| 列 | 写什么 |
|---|---|
| Facet | 需求面编号 |
| Questions | 这组的问题编号 |
| Planned | 计划 Exa 搜索几次、Firecrawl 抓几页 |
| Actual | 实际次数和花费，做完再填 |

问题表，每行一个关键问题，对应瑜东的「证据研究任务单」：

| 列 | 写什么 |
|---|---|
| ID | E1、E2 |
| Facet | 需求面编号 |
| Question | 要证明的说法或要核实的数字 |
| Source type | 证据类型：标准、论文、技术文档、厂商资料、案例、论坛线索（不叫 Evidence type，避免和需求面表的 Evidence types 列撞名） |
| Use | 怎么用、要注意什么（例如「保留适用条件」「不虚构推力数字」「注意专利归属」）。用在哪一节看 Facet 列 |
| Weak | 是或否：没有采用的材料，或只有论坛线索 |

材料表，每行一份抓过的材料：

| 列 | 写什么 |
|---|---|
| Question | 问题编号 |
| Source | 出处、标题、网址、日期 |
| Finding | 原文里的话或数字，和适用条件 |
| Status | 采用、参考、拒绝、抓取失败 |
| Chart | 采用的材料里，数字用图表比文字讲得清楚就写 yes；简报的 Visual Element Plan 从这里取图表数据（用户 2026-10-23 要求保留旧 Step 6 的这一条） |

预计花费和实际花费分开写，对应卡片的「计划 11 个检索、预计 24 积分，是计划值，不是实际花费」。

### 4.4 下游怎么变

- Step 7 信息增量：输入里「Step 6 保留的统计数字」换成证据计划文件；Evidence 列只能填状态为「采用」的材料。薄弱项照现有规则收窄说法。
- Step 8 生成简报：Statistics to Include 表只从「采用」的材料里来。
- SKILL.md 步骤表：Step 6 一行改名，「其他文件」列从 None 改成模板和两个产物文件。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-6-evidence-plan.md` | 由 step-6-statistics-research.md 改名并重写 |
| `skills/blog-brief/references/step-4-competitor-gaps.md` | 规则里「Step 6 确认后才算事实」改成「Step 6 采用了来源」 |
| `skills/blog-brief/templates/evidence-plan.md` | 新建 |
| `skills/blog-brief/references/step-7-information-gain.md` | 输入和 Evidence 的填法 |
| `skills/blog-brief/references/step-9-generate-brief.md` | Statistics to Include 的来源 |
| `skills/blog-brief/templates/brief-template.md` | Statistics to Include 表的来源说明 |
| `skills/blog-brief/SKILL.md` | 步骤表 Step 6、7、8 三行的「其他文件」；第 40 行 DISCOURSE.md 里的数字改为交给 Step 6 当问题 |
| `CLAUDE.md` | 目录树里的模板数量；SKILL.md 那行的「Step 6」改成「Step 9」（上个分支漏改） |

### 4.6 课程没写明、这次怎么处理

1. 预算：不设上限，只把计划次数和实际次数分开记。卡片只说「分配来源与预算」，第 04 课说预算怎么分没有公式，所以不编阈值。用户没选时按这条实现，要设上限以后改一句。
2. 问题数量：不设上限。Ebestron 例子是 4 个研究问题、11 个检索。
3. Exa 的花费：本仓库里没有 Exa 计费的依据，计划表只记搜索次数，不换算成钱。Firecrawl 按每页 1 积分记。

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 保留按主题搜数字，只加一张问题清单 | 起点还是主题，不是问题；温度分段这类说法还是可能漏掉 |
| 证据计划放在 Step 7 信息增量之后 | 信息增量的证据列要用证据计划的结果；瑜东也是先 A·07 后 A·08 |
| 只让 Step 6 把现有结果写成文件 | 解决了落盘，没解决「先定要证明什么」 |
| 照瑜东写成 JSON 文件 | 这条流程里各步产物都是 md，下一步和用户都直接读；md 表格同样能落盘和核对 |
| 照瑜东全用 Firecrawl 找和抓 | 用户定：Exa 找候选，Firecrawl 只抓原文 |
| 输入加任务单，或只取 weak evidence 类差距 | 瑜东卡片的输入只有差距清单和需求面，加或筛都是自己编的 |

## 6. 验证

| 验证 | 结果 |
|---|---|
| 仓库检查 | pytest 1518 通过 6 跳过；validate_skills、consistency_check 通过；lint_prose 在跟踪文件里无违规 |
| 整篇重读 | 删掉模板和步骤文件里重复的三句（计划与实际的填写时机、摘要不能填 Finding、开搜前先填问题表）。旧 Step 6 删掉三样：8 到 12 条候选池、tier 1 到 3 优先、挑 TL;DR 用的数字；按用户要求保留「标出适合画图的数字」，成为材料表的 Chart 列 |
| 模拟跑（子代理，不调接口） | 发现 5 处没写清并已修：没有需求面的差距、查询计划按哪些需求面分行、Evidence type 和需求面表撞名（改为 Source type）、工具检查的时机、Exa 的 objective 写法 |
| 真实跑（Coofandy 会话，亚麻衬衫已有的 Step 1 到 5 产物，输出在 `rerun-2026-10-23-evidence-plan/`） | 9 个问题，计划 9 次搜索、18 次抓取，实际 9 次、16 次；16 份材料 13 采用、3 参考。温度分段列成 E3，采用 CCOHS 引用的 ASHRAE 55 室内舒适温度表，简报把说法收窄到室内范围，没有写免责句。搜索量数字没有出现。大纲里无竞品页面、排名或差距。配图计划的 3 张图都来自 Chart 为 yes 的材料 |
| 真实跑发现、已修 | 积分：计划 16，实际 43，因为 PDF 按页计费。模板改为写明 PDF 按页计费，查询计划加「实际积分」列。一份材料回答多个问题：材料表允许填多个问题编号。摘要页：材料 3、14、15 只抓到论文摘要页就标了采用；用户 2026-10-23 定，摘要里有数字和适用条件才能采用，否则标参考，已写进 Step 6 规则 |

真实跑发现、留给后面分支的问题：

- 部分回答的问题只能标 Weak 为 no（E2、E4）。课程没给中间值，没加。
- Step 7：差距 G10（可持续性说法）写不出读者收益，和「每条差距一行」冲突；Evidence 列放不下「采用来源加收窄说法」。
- Step 8：内链没有输入来源。
- SKILL.md：没说 Step 6 到 8 要不要读 orchestration-details.md 和 BRAND.md、VOICE.md。
- Coofandy 的花费保护钩子会拦下并行的抓取调用，这是那个项目的配置，不归 skill 管。

## 7. 提交拆分

1. `docs(blog-brief): add design for the evidence plan step`
2. `feat(blog-brief): plan evidence by question in Step 6`
