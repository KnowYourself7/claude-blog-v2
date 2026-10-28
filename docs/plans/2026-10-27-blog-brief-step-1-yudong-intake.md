# 开发文档：Step 1 任务单按瑜东步骤 01 的四组输入、红线和例子改写

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-27 |
| 状态 | 已实现，检查已过，待用户审阅后提交。真实跑没有做，原因见第 6 节 |
| 分支 | `feat/upgrade-step-1-topic-intake`，从 #27 合并后的 `main` 开 |
| 依据 | 瑜东步骤 01「输入与任务范围」：工具是人工和客户资料；四组输入（主题与读者、客户与品牌、页面与转化、执行与交付）；动作「已有站点再结合站内覆盖、支柱页、锚文本清单判断」；产物 `_blog_workflow_state.json`、`_research_plan.json`；三条红线（缺少的品牌事实去核实、官网描述分清声明和证据、产品能力证书专利案例不得凭空补全）；Ebestron 任务启动单和它的警示（p.107 到 108）。整理稿第 01 课，本地副本在 docs/yudong/（已被 .gitignore 排除，不进仓库） |
| 来源 | `docs/reviews/2026-10-25-blog-brief-vs-yudong-phase-a.md` 的 A·01 一节（缺三样：站内已有文章、一手资料、执行与交付）；`docs/reviews/2026-10-27-linen-winter-article-review.md` 第 3 节第 1 项（任务单收同站页面清单，Step 1 查撞题）；`docs/reviews/2026-10-27-information-gain-and-reader-experience.md` 第 4 节第 1 项（任务单加一手资料一格，和页面清单并进同一个 Step 1 分支） |
| 用户决定 | 2026-10-27：Step 1 按瑜东的思路和结构改写，要有明确输入、产物落盘、红线和例子；英文按 simple-english 写 |

## 1. 目标

跑 `/blog brief` 时，Step 1 把瑜东步骤 01 要交代的四组信息收齐进任务单，站内已有同题文章时先停下问「新建、更新旧文，还是换角度」，品牌没给的能力、证书、案例一律写 `missing`，不由模型补。步骤文件末尾有一份填好的 Ebestron 例子，模型照着填。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| Step 7 读「一手资料」行，`missing` 时在增量单写「若品牌提供 X，增益 I 可以变成 Y」 | 下一个分支。依据 2026-10-27 信息增益评审第 4 节第 1 项。本分支只收这一格 |
| Step 8、Step 9 按 Existing Pages 表安排内链 | 已有计划 `docs/plans/2026-10-24-blog-brief-internal-link-pages.md`。它的 Step 1 部分（加表）由本分支做掉，剩下 Step 8、9 的部分照那份计划另开分支 |
| 用户选「更新旧文」时，slug 和支撑页怎么跟着旧文走 | 以后再定。本分支只把选择记进任务单，简报照常往下跑 |
| 锚文本清单（瑜东动作里提到） | 不做。锚文本是内链的事，归 Step 8 那个分支 |
| 按「发布授权」决定 Step 2、Step 11 要不要停 | 不做。那两处停下是让用户做判断，不是等人点头。本分支只把授权记进任务单 |
| 按「接口预算」限制 Step 2 到 4 的付费调用，余额与配额检查 | 以后再定，属于 A·02。本分支只收这一格 |
| 自动读 sitemap.xml 拿页面清单 | 不做。2026-10-24 用户选了「用户给清单」，Step 1 不打开网站的规则不变 |
| 把瑜东的 `_research_plan.json` 搬过来 | 不做。我们的研究计划分散在 Step 2 到 Step 6 的产物里，没有单独一份 |

## 3. 原因

### 3.1 现在的问题

任务单的四张表（Topic、Business、Page、Delivery）和瑜东的四组输入名义上对应，但每组都缺格子。阶段 A 对照评审（2026-10-25）早就记了，两份 2026-10-27 评审又各推了一项：

| 瑜东输入 | 任务单现状 | 后果 |
|---|---|---|
| 客户与品牌：可公开的一手资料 | 没有这一格 | 亚麻那篇的 First-Party Evidence 是 `none supplied`，四条增益全是公开来源综合，竞品花同样的钱也做得出来（信息增益评审 2.1 节） |
| 页面与转化：站内已有文章是否覆盖过 | 没有这一格，也没有页面清单 | 亚麻那篇和站内旧文撞题，审稿查出来了但不计分，文章照样放行（亚麻评审 C·17 行）。撞题是唯一会让发布变成净损失的问题 |
| 执行与交付：本轮范围与发布授权、接口预算与权限、作者/平台/交付目标 | 只有定位、角色、交付物 | 阶段 A 评审列为缺口。没有地方记用户授权了什么、付费调用有没有上限 |
| 红线：官网描述分清声明和证据；能力、证书、专利、案例不得补全 | 只有「不打开网站、不推断品牌事实」两句 | 用户的话或 `BRAND.md` 里「行业领先」这类说法，现在没有规则拦住它进 Sells 行 |
| 例子 | 没有 | Positioning 和 Deliverable 的定义表里各有一句 Ebestron 的例子，其余行没有。模型第一次填表看不到一份完整的样子 |

### 3.2 课程怎么要求

步骤 01 的工具一栏写「人工 / 客户资料」，所以 Step 1 不调接口、不打开网页，缺了就问人。瑜东最强调的一条是「缺少的品牌事实需要核实；不能由模型补成客户能力或案例」（p.107）。Ebestron 任务启动单里「业务边界」那格写了「不能冒称生产胶水配方」，警示写「不能为了卖耗材把所有故障都归因于硬件」（p.108）。这两句都是用户给的限制，任务单要有地方装。对已经运营的网站，要「结合站内覆盖、支柱页、锚文本清单判断」（p.107），这是 Step 1 自己的动作，不是后面步骤的。

### 3.3 结构

瑜东每一步的讲法是：工具、输入、动作、产物/落盘、红线、例子。`essentials/skill-file-format.md` 定的六段（Goal、Inputs、Rules、Steps、Outputs、Check）已经一一对应前五样，只差例子。本分支在六段后加第七段 `#### Example`。工具写进 Goal 的最后两句。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 用户的话 | 四组信息全部先从这里抄：一手资料、同站页面、本轮范围、预算、作者和平台都是新加的 |
| SKILL.md 已经加载的 `BRAND.md` | 和以前一样：品牌事实和 Audience。不从里面抄声明 |
| `templates/task-brief.md` | 改后的模板，多一张表、多五行 |

### 4.2 处理步骤

1. 模板 `task-brief.md`：
   1. Business 表加 First-party material 行：品牌自己拥有、可以公开的材料，每项写是什么、在哪。Does not sell or claim 行的占位说明加上「用户给的警示」。
   2. 新表 Existing Pages，三列：URL、Covers（用用户的话写页面讲什么）、Type（pillar、post、product、category、other）。没给就一行 `missing`。
   3. Page 表加 Existing post on this topic 行：`[URL], [用户的选择]`、`none in the list`、`missing` 三种之一。
   4. Delivery 表加三行：Scope（本轮交付什么、谁批准发布）、API budget（付费调用上限）、Author and platform。都允许 `missing`，不起草，不停。
2. 步骤文件 `step-1-topic-intake.md`：
   1. Goal 加两句：来源是用户和 `BRAND.md`；不调接口、不打开网页。
   2. Rules 加三条红线：不写用户没给的能力、证书、专利、案例、测试数据；没有证据的说法是声明，不进 Business 表；不打开 Existing Pages 里的网址。
   3. Steps 加两项：填 Existing Pages 表；在 Page 表里比对 Covers 和读者决策，同题就写 URL 加 `ask`。停下那一项改成：草稿、Page 缺、`ask` 三种情况之一就停，一条消息里一起问，并列出其余 `missing` 格让用户选填。
   4. Outputs 加 `briefs/[slug]-state.json`，指向 SKILL.md 的 State File 一节，不重复写规则。
   5. Check 合并成五条，加上 Existing Pages 和声明两项。
   6. 末尾加 `#### Example`：Ebestron 任务启动单填成任务单，每行标来源（用户、默认、推断、起草），最后说明这一步为什么停、问什么。
3. 测试 `tests/test_blog_brief_workflow.py` 加一条：任务单模板有五张表，Existing Pages 表有三列，Page 表有 Step 11 阶段门读的那一行。
4. 待办计划 `2026-10-24-blog-brief-internal-link-pages.md` 的状态行补记：Step 1 部分由本分支做了。
5. `docs/FORK-DEVLOG.md` 补 022（#27 欠的）和 023（本分支）。

### 4.3 输出

| 文件 | 变化 |
|---|---|
| `briefs/[slug]-task-brief.md` | Business 多 First-party material 行；多一张 Existing Pages 表；Page 多 Existing post on this topic 行；Delivery 多 Scope、API budget、Author and platform 三行 |
| `briefs/[slug]-state.json` | 不变。只是在 Step 1 的 Outputs 里写明它在这一步产生 |

### 4.4 下游怎么变

- Step 2、3、7、8、9、11 读任务单的行名不变，不受影响。`brief_state.py` 的阶段门按行名在 `## Page` 一节里找 Page this post supports，新表 `## Existing Pages` 是独立的二级标题，不会混进去。
- Step 1 多一种停下的情况：同题旧文。用户没给页面清单时和以前一样。
- 新加的六个格子现在没有下游读。它们是给下一个分支（Step 7 读一手资料，Step 8、9 按清单排内链）准备的输入。

### 4.5 附带：Step 2 加文章体裁

用户 2026-10-27 先提出把 Step 5 模板选择并进 Step 2。这和 2026-10-23 的决定冲突（模板要看竞品页面结构选，Step 2 不打开页面），用户改定为：Step 2 只按瑜东步骤 03 的「页面选择：故障排查型博客」加一行 Post type，Step 5 和编号不动。改动：`step-2-serp-intent-gate.md` 加 Steps 第 6 条（从读者任务和博客标题写两三个词的体裁，和任务单 Positioning 不一致时两个都写）、Rules 补回「30% 是本 skill 的规则」、Example 段（Ebestron 搜索意图单，p.112）、规则各加半句原因；`templates/search-intent.md` 的 Reader Task 下加 Post type 一行。下游暂时没有步骤读 Post type。

### 4.6 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/templates/task-brief.md` | 见 4.2 第 1 条 |
| `skills/blog-brief/references/step-1-topic-intake.md` | 见 4.2 第 2 条 |
| `skills/blog-brief/references/step-2-serp-intent-gate.md`、`skills/blog-brief/templates/search-intent.md` | 见 4.5 |
| `tests/test_blog_brief_workflow.py` | 见 4.2 第 3 条 |
| `docs/plans/2026-10-24-blog-brief-internal-link-pages.md` | 状态行补记 |
| `docs/FORK-DEVLOG.md` | 022、023 两行 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 例子单独放一个文件 `references/example-task-brief.md` | 多一个要读的文件。例子只有二十来行，放在步骤文件末尾，读步骤时顺便看到 |
| 例子用亚麻那篇真实产物 | 那份任务单是 #24 之前跑的，没有 Role 行，而且是用户的测试场数据。Ebestron 是课程里的公开例子，每一格都有页码 |
| 缺品牌事实就停下问，和缺 Page 一样 | 品牌事实的格子多（五行加一张表），每次都停会让一句话的请求也要来回两轮。改成：只要停了就把 `missing` 格一起列出来让用户选填；没停就留 `missing` |
| 同题检查打开页面读正文 | 违反「不打开网站」。只按用户写的 Covers 判断，判断不了就不算同题 |
| Scope、API budget、Author and platform 也起草 | 这三样只有人知道（工具是「人工 / 客户资料」），模型起草没有依据 |
| 把 `_research_plan.json` 也落盘 | 我们没有单独的研究计划文件，造一个空壳没有读者 |

## 6. 验证

| 验证项 | 结果 |
|---|---|
| `python3 -m pytest tests/` | 1545 passed，55 skipped（新加 1 条模板测试） |
| `python3 scripts/lint_prose.py` | 本分支改的文件 0 处。整体报的 43 处全在本地未入库的 docs/yudong/，和本分支无关 |
| `python3 scripts/validate_skills.py --root .` | 通过 |
| `python3 scripts/consistency_check.py` | errors 为空，warnings 0 |
| 句长 | 步骤文件最长句 23 词，没有 should、may、分号、破折号、缩写（`men's` 是代码里的输入例子） |
| 整篇重读 | 用户 2026-10-27 看过第一版后说太啰嗦，整篇压到 103 行（原 193 行）：删掉 Delivery 定义表（模板占位符已经说明每行）、slug 规则合成一句、Check 压成四条、例子表把 missing 行合并成一行；模板注释也压成五句。之后按 skill-creator 的写法规则再过一遍：每条红线加半句原因，例子标成 Input 和 Output，116 行 |
| 新旧对照（子代理） | 报 3 处含义变化、5 处要猜、4 处重复、4 处例子和规则不符。已改：Goal 补回「读者得到什么」；草稿定义限定为 Positioning、Role、Deliverable 三行；Existing Pages 缺 Covers 或 Type 时写 `missing`、不从网址推断类型；同题多页时每个网址都写；`ask` 没选就再问；Check 第 5 条写明两行 Page 的来源；例子里「不冒称胶水厂」改成用户原话。没改的重复：模板列值、步骤写判断（声明写哪行、`none in the list` 怎么判），按「填表规则归模板、判断规则归步骤」的分工各写一遍 |
| 模拟跑（子代理，Ebestron 和 COOFANDY 两个场景） | 报 7 处要猜。已改：用户给的标题没处放，Topic 表加 Working title 行；Existing post 行的 `missing` 不再算「Page 缺」，只列出不追问；「行业领先」这类声明以前会被静默丢掉，现在写进 Does not sell or claim 行并标 `no proof given`；Positioning 和 Deliverable 「给没给」有了判断标准，用户给了一部分就保留那部分再起草；规模定义为计数或长度；例子的 Positioning 改成草稿、读者决策不再偏向「换零件」。没改：英国市场的 DataForSEO 代码靠模型记忆（2826），这是 #27 之前就有的规则，Step 2 调接口时错码会报错，另议 |
| 真实跑 | 没做。Step 1 不调接口，模拟跑覆盖了全部动作；真实跑等 Step 7、8 读新格子的分支一起在 playground 做 |
| 对照瑜东步骤 01 | 四组输入各有格子：主题与读者（Topic 表 6 行）、客户与品牌（Business 表含一手资料）、页面与转化（Page 表含同题旧文、Existing Pages 表）、执行与交付（Delivery 表含范围、预算、作者平台）。三条红线进了 Rules。动作「结合站内覆盖判断」是 Steps 第 5 条。产物对应 `briefs/[slug]-task-brief.md` 和 `briefs/[slug]-state.json`。Ebestron 例子在 Example 段。没搬的：`_research_plan.json`、锚文本清单，见第 2 节 |
| 对照上游原版（3544423） | 原版 Step 1 收话题、读者、搜索意图、业务背景四项，缺了「从上下文推断」。本分支保持 fork 的做法：品牌事实不推断、写 `missing`，搜索意图留给 Step 2；读者和业务背景都保留，只是分了格子 |

## 7. 提交拆分

1. `docs(blog-brief): add design for the Step 1 task brief after Yudong step 01`
2. `feat(blog-brief): collect the four Yudong input groups in Step 1 and add the Ebestron example`
