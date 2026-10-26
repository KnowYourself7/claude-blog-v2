# 开发文档：任务单定下文章定位和交付物

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-26 |
| 状态 | 已实现，真实跑已做，未提交 |
| 分支 | `feat/blog-brief-positioning`，从最新的 `main` 开 |
| 依据 | 瑜东步骤 01 的四组输入：主题与读者、客户与品牌、页面与转化、执行与交付（p.107）；Ebestron 任务启动单的「文章定位」「交付约 2.8K 词、7 个故障主题」（p.108）；A→B 阶段门「方向清楚：读者任务和页面职责」（p.127）；信息增量要让读者「多理解、多判断、多完成」（p.53） |
| 来源 | `docs/reviews/2026-10-25-blog-write-baseline-winter.md` 的「改 brief 的必要性判断」「定位为什么会偏成学术论文」两节 |
| 用户决定 | 2026-10-26：Step 1 加文章定位和交付物；读者画像从 `BRAND.md` 取；商业页和读者下一步缺了就问用户；Step 7、Step 8 读交付物（新的步骤依赖，用户同意） |
| 顺序 | 同站页面清单的计划文档 2026-10-24-blog-brief-internal-link-pages.md（还没提交）也改 Step 1 任务单和 Step 8。本分支先做，那份等本分支合并后再按新模板改 |

## 1. 目标

跑 `/blog brief` 时，任务单先写清这是一篇什么文章、写给谁、为品牌做什么、读者最后能拿走什么。后面的信息增量和大纲都围着这个交付物排，文章不再滑成和品牌无关的学术论证。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| Step 6 证据计划只收会改变读者选择的问题，背景知识压成一段 | 第二个分支，依据 A·07（p.119）。本分支改完先看材料学问题会不会自己变少 |
| Step 2 的读者任务读文章定位 | 不做。读者任务来自实时搜索结果，定位来自品牌，两者分开。真实跑时看 Step 2 是否仍然偏，再讨论 |
| Step 4 的 `weak evidence` 差距类型 | 不做。前两个分支改完后看它还会不会把科学出处变成差异点 |
| Step 11 阶段门加「定位」检查 | 以后再定。本分支让 Step 1 在缺定位时停下问，阶段门暂时不用再查 |
| brief 模板里写死的「Word count 2,000-2,500」「Flesch 60-70 (expert-accessible)」 | 不改。篇幅以后可以从交付物来，另外讨论 |
| 按话题类型写死交付物，例如「穿搭类一律要完整造型」 | 不做。课程没有这条规则。交付物每篇在 Step 1 定 |
| blog-write、审稿加消费者视角检查、修复循环限篇幅 | 不在 blog-brief 里。见 blog-write 的计划文档 2026-10-25-blog-write-step-files-and-use-brief.md（还没提交） |
| 同站页面清单 | 见「顺序」一行 |

## 3. 原因

### 3.1 现在的问题

2026-10-25 的基线实跑（关键词 `can you wear linen in winter`，COOFANDY 男装）写出了一篇材料学论证：导热率、回潮率、clo 值、经纬纱占了大量篇幅，没有一套能照着穿的造型。你给的 ChatGPT 消费者视角评价是 65 分，我们的审稿是 93 分。

追到 brief，问题从 Step 1 就进来了。下表的文件在 `claude-seo-playground/_archive/2026-10-26-winter-baseline/briefs/`：

| 环节 | 实跑产物 | 缺了什么 |
|---|---|---|
| Step 1 页面与转化 | `briefs/can-you-wear-linen-in-winter-task-brief.md` 第 25、26 行：Page this post supports 和 Reader next step 都是 `missing` | 没有东西把文章和卖男装连起来。Step 1 规定缺了就写 `missing`，不问用户 |
| Step 1 读者 | `BRAND.md` 第 13 行写着多数读者「需要明确的穿搭答案，而不是时尚理论」 | Step 1 只抄品牌、域名、卖什么、不能说什么四格，读者画像没进 brief |
| Step 1 执行与交付 | 任务单模板没有这一组 | 文章定位和交付物没有地方写 |
| Step 2 读者任务 | `search-intent.md` 第 53 行：读者想知道「哪些单品、层次和颜色能让亚麻保暖」 | 没有定位约束，方向从穿搭滑到了保暖 |
| Step 7 信息增量 | 5 条增量全是数据卡：纤维事实卡、保暖层数值卡、克重分档等 | 没有一条是读者能照着做的造型 |
| Step 8 大纲 | 第二版大纲第一个 H2 用实验数据回答「亚麻能不能过冬」 | 自审只查意图、问题、证据、增量，不查是否服务于品牌定位 |

### 3.2 课程怎么要求

瑜东步骤 01 要求开工前交代四组信息（p.107）。我们的任务单有前三组的一部分，第四组「执行与交付」整组没有。阶段 A 对照文档（`docs/reviews/2026-10-25-blog-brief-vs-yudong-phase-a.md` 第 31 行）已经记过这个缺口。

Ebestron 的任务启动单写了「文章定位：故障排查型支持博客，引导读者了解对应产品」和「交付约 2.8K 词、7 个故障主题」（p.108）。这两格决定了后面的研究查什么、大纲排什么。

步骤 01 的工具一栏写的是「人工 / 客户资料」：这些信息由人给，不由模型补。所以缺了要问。

### 3.3 上游原版

上游原版的 Step 1 会问「Target audience」和「Business context: What's the CTA?」（`git show 3544423:skills/blog-brief/SKILL.md` 第 52、54 行），只给主题时从上下文推断。我们拆步骤时丢了读者这一项。本分支把读者补回来，并加上定位和交付物。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 用户的话 | 定位、交付物、商业页、读者下一步，用户说了就照抄 |
| SKILL.md 已经加载的 `BRAND.md` | Audience 一节抄进新的 Reader 行。品牌、域名、卖什么、不能说什么也从这里抄，标明来自 `BRAND.md` |
| `briefs/[slug]-task-brief.md` 的 Positioning、Deliverable 两行 | Step 7 定一条交付物增量，Step 8 自审和排 H2，Step 9 抄进 brief |

### 4.2 处理步骤

1. Step 1 任务单模板改三处：
   1. Topic 表加一行 Reader：读者是谁、懂多少。来自 `BRAND.md` 的 Audience，或用户的话。都没有就写 `missing`，不推断。
   2. 加一张新表 Delivery，两行。Positioning：文章类型、写给谁、为品牌做什么。Deliverable：读者看完能拿走、能照着用的那个东西，以及它的规模，例如「3 套按场合分的完整造型」。
   3. Page 表不变。
2. Step 1 的规则和步骤：
   1. 品牌事实和读者画像只从用户的话和 `BRAND.md` 抄，不打开网站，不推断。
   2. 用户没说定位或交付物时，按读者决策、读者画像和 Sells 起草，标 `draft`。
   3. 只要有一行是 `draft`，或 Page this post supports、Reader next step 是 `missing`，就停一次，在一条消息里一起问。用户说没有商业页，就写 `missing, the user has none`，阶段门照旧给 warn。
   4. 用户给了全部四项时不停。
3. SKILL.md 清单的 Step 1 一行加 `Can stop.`。
4. Step 7：
   1. Inputs 里任务单那一行，加上 Positioning 和 Deliverable。
   2. 加一步：先规划一条兑现交付物的增量，它的 Use 以「读者能做什么」结尾。
   3. 信息增量模板在 Gains 表下加一行 `Deliverable gain: [gain ID]`。
   4. Check 加一条：Deliverable gain 指向一条存在的增量，它兑现了任务单的 Deliverable。
5. Step 8：
   1. Inputs 里任务单那一行，加上 Positioning。
   2. 自审表加一行 Positioning，问两件事：每个 H2 是否服务于定位；交付物增量有没有自己的 H2。
   3. 大纲模板的自审表加同一行。
   4. Check 加一条：Deliverable gain 在第二版大纲里有自己的 H2。
6. Step 9（用户的决定里没有这一步，是我加的，等用户确认。不加的话，blog-write 只读 `briefs/[slug]-brief.md`，看不到定位）：
   1. brief 模板在 Template 之前加一节 Positioning，抄任务单的 Positioning、Reader、Deliverable 三行。
   2. Inputs 里任务单那一行，加上这三行的用途。
   3. Check 加一条：Positioning 一节和任务单一致。
7. 测试：加一条，Step 7、8、9 的 Inputs 里点名的任务单行，在任务单模板里都存在。防止以后改模板行名时漏改步骤文件。

改动的英文按 `skill-file-format.md` 第五节写，规则只写在一处：判断规则进步骤文件，填表规则进模板。

#### 实现中按检查结果做的调整

新旧对照和模拟跑（见第 6 节）找出的歧义，按下面改了：

1. `draft:` 前缀和 `missing, the user has none` 是填表规则，放进任务单模板的注释，步骤文件不再写。
2. Step 1 补了五条：用户的话和 `BRAND.md` 都有值时，用用户的话；Delivery 草稿不算品牌事实；Positioning 写的是这篇文章，不抄 `BRAND.md` 自己的品牌定位一节；先存任务单再停；用户否掉草稿又没给新值，就再问一次。
3. Step 1 停下的条件改成 Page 行「正好是 `missing`」，`missing, the user has none` 不会再触发第二次停。
4. Step 1 的验收允许 Positioning 里某一部分写 `missing`。没有品牌信息时，「为品牌做什么」写不出来。
5. Step 7 写明「服务于定位」是指合乎文章类型和读者。Our Difference 里不服务于定位的部分，不规划增量。交付物里没有来源的部分（例如造型的具体单品）标 `example`。
6. Step 8 的定位自审改成两问：交付物增量是不是某个 H2 的主要任务；有没有 H2 在讲读者用不上的背景。Changes 一步写明：这类 H2 缩短或合并，它的需求面要留在某个 H2 里，免得阶段门因为需求面丢失而失败。

### 4.3 输出

| 文件 | 变化 |
|---|---|
| `briefs/[slug]-task-brief.md` | Topic 表多一行 Reader；多一张 Delivery 表（Positioning、Deliverable） |
| `briefs/[slug]-information-gain.md` | Gains 表下多一行 `Deliverable gain: [gain ID]` |
| `briefs/[slug]-outline.md` | 自审表多一行 Positioning |
| `briefs/[slug]-brief.md` | 多一节 Positioning |

### 4.4 下游怎么变

- Step 1 从「永不停」变成「缺了就停一次」。用户一次说全四项就不停。
- blog-write 读 `briefs/[slug]-brief.md`，写稿子代理会看到 Positioning 一节和兑现交付物的 H2。blog-write 本身不改。
- 阶段门脚本 `brief_state.py` 不改。它按行名读 Page this post supports，新加的行不影响。
- 测试 `test_checklist_uses_match_step_file_inputs` 不受影响：Step 7、8、9 本来就读任务单，Uses 不变。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/SKILL.md` | 清单 Step 1 加 `Can stop.` |
| `skills/blog-brief/references/step-1-topic-intake.md` | Inputs 加 `BRAND.md`；规则和步骤见 4.2 第 2 条；Check 加定位、交付物、停下问过 |
| `skills/blog-brief/templates/task-brief.md` | Reader 行、Delivery 表 |
| `skills/blog-brief/references/step-7-information-gain.md` | 见 4.2 第 4 条 |
| `skills/blog-brief/templates/information-gain.md` | `Deliverable gain` 一行 |
| `skills/blog-brief/references/step-8-outline.md` | 见 4.2 第 5 条 |
| `skills/blog-brief/templates/outline.md` | 自审表 Positioning 行 |
| `skills/blog-brief/references/step-9-generate-brief.md` | 见 4.2 第 6 条 |
| `skills/blog-brief/templates/brief-template.md` | Positioning 一节 |
| `tests/test_blog_brief_workflow.py` | 任务单行名一致的测试 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 按话题类型写死交付物，例如穿搭类一律要完整造型 | 课程没有这条规则，话题类型也分不完。每篇在 Step 1 定，你确认 |
| Step 1 每次都停下，把四项全问一遍 | 用户一次说全时多停一次没有用。你定的是「缺了就问」 |
| 照旧写 `missing`，只在阶段门 warn | 这就是基线的做法，warn 之后流程照常往下走，文章还是偏了 |
| 让 Step 2 从搜索结果推出定位 | 搜索结果只能说明「该写博客还是别的页面」。品牌要这篇文章做什么，只有人知道（步骤 01 的工具是「人工 / 客户资料」） |
| 在 blog-write 里补定位 | 太晚。大纲在 brief 里已经定了，基线显示 blog-write 照大纲写，不会改结构 |
| 阶段门脚本同时加「定位」检查 | Step 1 已经保证定位不会缺。先不加代码，见第 2 节 |

## 6. 验证

开工前写的是打算怎么验，做完改成实际结果。

| 验证项 | 结果 |
|---|---|
| 仓库检查：`python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`（看 errors） | 通过。测试 1542 个通过、56 个跳过，新测试先失败后通过。skill 校验通过。破折号违规只在被 git 忽略的本地 `docs/yudong/`。一致性检查 6 个 errors 全部来自未提交的 blog-write 计划文档，本分支不提交它。`skills/blog-brief/SKILL.md` 103 行 |
| 新旧对照：子代理读改前改后的 Step 1、7、8、9 和模板，列出含义变了的规则、能两读的句子、仍然重复的地方 | 做了。没有规则丢失。找出 6 处两读、7 处重复或冲突、6 处要猜，按 4.2 节「实现中按检查结果做的调整」改了。没改的两处：Step 1 起草 Positioning 时会用到 Sells 行，和模板注释「不推断品牌事实」字面上冲突，已在规则里写明草稿不算品牌事实；slug 为空时 Step 1 停下，但这时 `init` 还没法运行、记不了状态，这是改动前就有的问题 |
| 模拟跑 Step 1（子代理）：三种情况 | 做了，改动后的结果。只给关键词、有 `BRAND.md`：停一次，起草定位（给 25 到 45 岁美国男性的季节穿搭指南，引向亚麻系列）和交付物（5 套冬季造型），问商业页和下一步，五项验收全过。四项都给：不停，五项验收全过。没有 `BRAND.md`（铸铁锅清洁）：停一次，Reader 和业务四格写 `missing`，定位里「为品牌做什么」写不出来，按调整第 4 条处理。子代理建议的「Reader 和业务行缺了也问」没做，你定的范围是只问商业页和读者下一步 |
| 模拟跑 Step 7、8（子代理）：用基线的需求面、竞品差距、证据计划，加一份填好定位和交付物的任务单 | 做了。交付物增量是「3 套冬季造型：上班、短时间外出、长时间户外」。第二版大纲从基线的 8 个 H2 变成 5 个，造型单独占第 3 个 H2。5 个 H2 里 4 个是穿搭，1 个仍偏科学（第一个 H2 用实验数据答「能不能穿」）。最大的问题在证据计划：9 个证据问题大多是纤维和热学，颜色、版型、场合、鞋都没有对应问题，造型内容只能标 `example`。这证明第二个分支（Step 6 按读者选择定证据问题）是必要的 |
| 真实跑（playground）：同一个关键词 `can you wear linen in winter` 重跑完整 brief，和基线对比 | 做了，2026-10-26，约 25 分钟（其中约 8 分钟等用户回答）。花费：DataForSEO 0.053 美元、Firecrawl 26 积分、Exa 7 次。产物在 `claude-seo-playground/briefs/`，笔记是 `can-you-wear-linen-in-winter-positioning-notes.md`。对比见下面 6.1 节 |
| 对照瑜东 | 符合步骤 01：补上第四组「执行与交付」里的交付目标和 p.108 的文章定位。页面与转化缺了就问用户，对应工具一栏的「人工 / 客户资料」，这次用户补上了商业页和下一步。也符合 A·08「多完成」：交付物增量是能照着穿的造型表。没做的：第四组的发布授权、接口预算、作者和平台，见第 2 节。我们自己加的：Step 8 自审的定位一行，课程没有这一检查，依据是 A→B 阶段门「方向清楚：读者任务和页面职责」(p.127) |
| 对照上游原版（`3544423`） | 增益：上游 Step 1 问读者和 CTA，但只给主题时自己推断。新版的读者从 `BRAND.md` 取，定位和交付物要用户确认。真实跑里大纲从数据卡转向了造型，见 6.1 节。代价：Step 1 多停一到两次，这次等了约 8 分钟；每个 brief 文件多几行。未验证：照这份 brief 写成的文章，读者体验是否更好，要等文章写完再比 |

### 6.1 真实跑和基线的对比

| 项 | 基线（2026-10-25） | 新版（2026-10-26） |
|---|---|---|
| 任务单 | 没有定位和交付物。商业页、读者下一步都是 `missing` | 定位：给 25 到 45 岁美国男性的季节穿搭指南，引向 COOFANDY 亚麻单品和冬季外搭。交付物：6 个场合各一套造型的表。读者画像来自 `BRAND.md`。商业页和下一步由用户补上 |
| 阶段门「支撑页面」 | warn | pass |
| 信息增量 | 5 条，全是数据卡 | 4 条。交付物增量 I1 是造型表，I2 是「今天能不能穿亚麻」的判断表，I4 是选购时看克重的检查表。只有 I3 讲保暖原理 |
| 第二版大纲 | 8 个 H2，没有一个是造型 | 6 个 H2，造型表排第 2 |
| 自审起的作用 | 无定位一行 | 定位一行发现「面料科学单独成节，读者用不上」，并入分层一节（C1）。意图一行把造型表从第 6 提到第 2（C3） |
| brief.md | 无定位 | 开头有 Positioning 一节，blog-write 能读到 |
| 证据计划 | 9 个问题，5 个是面料和热学 | 7 个问题，4 个是面料和热学。Step 6 不读任务单，这一项没变是预期的，属于第二个分支 |
| 没有来源的部分 | 无 | 秋季、颜色和鞋三节只能写成风格建议，阶段门对 Still Open 给 warn |

两点要注意：

1. Step 2 到 Step 6 每次跑结果都会有出入。比如这次 Step 4 的 Our Difference 自己就提到了造型表，这一点不能算在本分支头上。只跑了一次，差距只说明方向。
2. 实跑发现的问题：用户第一次只回答了商业页和下一步，没提两份草稿。Step 1 按验收规则又问了一次，多等了约 3 分钟。用户 2026-10-26 定：保持现在的做法，草稿必须明确回答。

## 7. 提交拆分

```
docs(blog-brief): add design for positioning and deliverable in the task brief
feat(blog-brief): set the post positioning and deliverable in Step 1 and plan around them
```

第二个提交同时改步骤文件、模板和测试，保证它单独拿出来测试也能全过。合并后在 `main` 上单独提交 `docs: log fork change NNN`。
