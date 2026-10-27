# 开发文档：blog-write 拆成步骤文件，有 brief 就照 brief 写

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 计划中，等用户确认方案。2026-10-26 补记：基线实跑后部分前提变了。原版其实照 brief 的模板和 H2 写，问题主要出在 brief 的定位和篇幅，已由 #24、#25 改掉。动手前先按 `docs/reviews/2026-10-25-blog-write-baseline-winter.md` 的「对开发计划的含义」一节重新评估 |
| 分支 | 两个分支，先后做：`refactor/blog-write-step-files`（只搬家，不改行为），`feat/blog-write-use-brief`（有 brief 就强制用）。都从最新的 `main` 开；第二个等第一个合并后再开 |
| 依据 | 第 00 课「每一步都有明确输入、产物和验收」（p.106）；第 05 课 A→B 阶段门「方向、结构、证据三清才进写作」（p.127）；第 06 课 B·11 从研究计划出发（p.128）；Anthropic 官方 Skill authoring best practices：SKILL.md 正文保持在 500 行以内，超出就拆成单独文件按需读取（progressive disclosure，渐进披露：先读目录，用到哪步再读哪步），https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| 路线图 | `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节第 9 行 `feat/blog-write-use-brief` |
| 先例 | blog-brief 拆文件：`docs/plans/2026-10-22-blog-brief-step-files.md`（PR #10），可勾选清单：PR #18 |
| 用户意见 | 2026-10-25 提出四条：SKILL.md 太长，要不要像 brief 一样拆；强制读 brief 和它的 reader task；Phase 1.5 选模板和 brief 重复，以 brief 为准；Phase 3 大纲和 brief 是否重复。同日回答三个问题，见第 3.4 节 |

## 1. 目标

跑 `/blog write` 时，如果项目里已经有这篇文章的 brief，文章就照 brief 选好的模板、读者任务和第二版大纲来写，不再自己重选模板、重出大纲。SKILL.md 从 429 行缩成只管步骤顺序的总控，每一步一个文件，用到哪步才读哪步。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 没有 brief 就拒绝写 | 不做。`blog-cluster` 和 `blog-multilingual` 只传主题就调用 `/blog write`，拒绝会让它们跑不通。用户 2026-10-25 定：有 brief 必须用，没有就走原来的流程。以后这两个调用方改成先跑 `/blog brief`，再重新讨论 |
| 把 Phase 1.5 的模板证据检查挪进 brief Step 5 | 用户 2026-10-25 定：以后另开分支 |
| Phase 2 研究改成从 brief 的证据计划出发（B·11，p.128） | 以后单独讨论。注意：2026-10 曾做过 b11、b12（章节研究、四段式正文），同一份 brief 下原版写作的盲评分高 4 到 6 分，已放弃。记录在 playground `_archive/2026-10-21/comparisons/2026-10-linen-pants/README.md` |
| 正文按四段式写（B·12，p.130）、组件和原稿验收（B·13、B·14，第 07 课） | 同上，以后单独讨论 |
| 读 A→B 阶段门的结果，没过就不写 | 等 `feat/blog-brief-gate-a-to-b` 做完。见 `docs/plans/2026-10-25-blog-brief-run-state-and-gate.md` |
| Phase 0 按 brief 的 SERP Features 定目标渠道 | 不做，用户没提 |
| 交付闸门（Phase 6.5）和交付（Phase 7）的内容 | 不改，也不搬出 SKILL.md。原因见第 5 节 |
| 第一个分支里改任何一句规则，或把搬出去的文字改成六段格式（Goal、Inputs、Rules、Steps、Outputs、Check） | 不做。第一个分支只搬家。哪一步以后要改内容，那个分支再按 `skill-file-format.md` 改格式，和 brief 的做法一样 |
| 修 `drafting-reference.md` 和 SKILL.md 的一处矛盾（见第 3.3 节） | 不在这两个分支里修。另开一个 `fix/` 小分支，等用户定 |
| 改 `blog-rewrite` | 不做 |

## 3. 原因

### 3.1 SKILL.md 太长

`skills/blog-write/SKILL.md` 有 429 行，接近项目规定的 500 行上限。上限写在 `CLAUDE.md` 开发规则里，由 `test_skill_entrypoints_stay_under_500_lines` 检查。它从 fork 基点 `3544423` 到现在一行没改过，是上游原版。

每次跑 `/blog write`，这 429 行都一次读进上下文。其中 Phase 5 写作规则占 171 行（第 193 到 363 行），只有写正文时才用得上。

blog-brief 有同样的问题，拆成步骤文件后，后来每个分支只换一个步骤文件（路线二的做法）。blog-write 以后也要一步一步改，先拆开，后面每个分支的改动才小。

### 3.2 有 brief 时，写作还在重做阶段 A 的事

现在 Phase 1 第 2 条说：有 brief 就读它，然后跳到 Phase 1.5（SKILL.md:83）。读了 brief 以后，还会接着做两件 brief 已经做过的事：

| blog-write 现在做的 | brief 里已经有的 | 问题 |
|---|---|---|
| Phase 1.5（SKILL.md 第 85 到 120 行）：按标题里的字猜模板，比如有 "How to" 就选 `how-to-guide` | Step 5 按排名页面实际用的格式选模板，规则写明不按标题里的字选（`step-5-template-recommendation.md` 的 Rules） | 两次可能选出不同的模板，文章结构就和 brief 的大纲对不上 |
| Phase 3（SKILL.md 第 160 到 167 行）：用通用骨架（`drafting-reference.md` 第 9 到 70 行）重新出大纲，等用户批准 | Step 8 做了第一版、自审、第二版，每个 H2 都写了需求面、证据号、增量号和收窄的说法（`templates/outline.md`） | 第二版大纲可能被改掉，H2 和证据、增量的对应关系就丢了 |
| Phase 1 第 1 条：问读者是谁、主关键词是什么 | brief 的 Search Intent 一节有 Reader task，Target Keywords 一节有主关键词 | 重复问用户 |

真实例子在 2026-10 亚麻裤对照测试里。新版 brief 的大纲有 7 个 H2（`new-brief-original-write/briefs/what-to-wear-with-linen-pants-men/brief.md` 第 89 到 148 行）。原版 blog-write 写出的文章有 8 个 H2，多出的一节「Is Linen Cooler Than Cotton?」在大纲里没有（文章第 153 行）。同一次测试里，原版 brief 配原版写作，8 个 H2 和大纲完全一致。所以现在的写法不是每次都偏，而是没有规则保证不偏。

那两次用的都是 Step 8 加入前的旧 brief。按现在的 brief（带第二版大纲）跑 blog-write，还没有测过。

### 3.3 顺带发现的矛盾

SKILL.md 5f 说内链标记「must not reach the render」，由 Phase 6.5 第 2 小步换成真链接或删掉（SKILL.md 第 303 到 307 行）。`drafting-reference.md` 第 117 到 118 行却写着「The user (or a follow-up pass) will resolve these to actual URLs」。测试只检查 SKILL.md 里没有这句（`test_markers_are_resolved_by_orchestrator_not_writer_agent`），没查 `drafting-reference.md`。第一个分支只搬家，不修，见第 2 节。

### 3.4 用户的决定（2026-10-25）

| 问题 | 用户的回答 |
|---|---|
| 「以这里为准」指哪边 | 以 brief Step 5 为准，blog-write 删掉 Phase 1.5 的自动选模板。证据检查留下：读 brief 选定的模板，检查它的 Evidence gate，证据不够就停下，不编造 |
| `blog-cluster` 和 `blog-multilingual` 没有 brief 怎么办 | blog-write 先检查有没有 brief，有就必须用 |
| 拆文件和改行为分不分开 | 分两个分支 |

第二条回答改了最初第 1 条「brief 必须存在」。现在的规则是：有就必须用，没有就走原流程。所以 Phase 1.5 和 Phase 3 不删，改成只在没有 brief 时运行。

### 3.5 Phase 3 是否重复：结论

有 brief 时重复，没有 brief 时不重复。brief 的第二版大纲就是瑜东 A·10 的产物（p.125），写作阶段不该再改结构（p.127）。但 Phase 3 还有一件 brief 没做的事：在大纲里标出配图和图表的位置（`[IMAGE]`、`[CHART]`、`[VIDEO]`、`[CALLOUT]`）。第二版大纲的 Components 只管表格、FAQ、计算器这类组件。所以有 brief 时，Phase 3 只保留「标视觉位置」这一件事。

## 4. 方案

### 4.1 第一个分支：`refactor/blog-write-step-files`

#### 输入

| 输入 | 拿它做什么 |
|---|---|
| `skills/blog-write/SKILL.md`（429 行） | 按 Phase 切开，原文搬进步骤文件 |
| `skills/blog-brief/SKILL.md` 的 Workflow 一节 | 照抄它的清单写法 |
| 引用 blog-write Phase 编号的文件 | 跟着改编号 |

#### 处理步骤

1. 按下表把每个 Phase 的原文搬进 `skills/blog-write/references/` 下的一个文件。编号改成连续的 Step 1 到 Step 10，和 brief 一样。

   | 原来 | 新的 | 去处 | 行数 |
   |---|---|---|---|
   | Phase 0 Surface Targeting | Step 1 | `step-1-surface-targeting.md` | 约 25 |
   | Phase 1 Topic Understanding | Step 2 | `step-2-topic-understanding.md` | 约 10 |
   | Phase 1.5 Template Selection | Step 3 | `step-3-template-selection.md` | 约 36 |
   | Phase 2 Research | Step 4 | `step-4-research.md` | 约 38 |
   | Phase 3 Outline Generation | Step 5 | `step-5-outline.md` | 约 16 |
   | Phase 4 Chart Planning | Step 6 | `step-6-chart-planning.md` | 约 17 |
   | Phase 5 Content Writing（5a 到 5n） | Step 7 | `step-7-content-writing.md` | 约 171 |
   | Phase 6 Quality Check | Step 8 | `step-8-quality-check.md` | 约 36 |
   | Phase 6.5 Delivery Contract Enforcement | Step 9 | 留在 SKILL.md | 约 25 |
   | Phase 7 Delivery | Step 10 | 留在 SKILL.md | 约 4 |

2. SKILL.md 只留：frontmatter、开头的路径和不可信输入说明、Key references、Workflow 清单（照 brief 的写法：先读步骤文件，Check 全过才勾选）、Step 9 和 Step 10 原文。
3. 改所有「Phase N」的指代：SKILL.md 和步骤文件内部（例如「Phase 6.5 step 2」改成「Step 9 item 2」）、`drafting-reference.md` 第 9 和 11 行、`skills/blog-cluster/references/execution-workflow.md` 第 82 行「Phase 1 of blog-write」。
4. 改测试，断言内容不变，只换读的文件：

   | 测试 | 改法 |
   |---|---|
   | `test_editorial_contracts.py` 检查 "Check template evidence before selection"、"do not simulate it" | 读 `step-3-template-selection.md` |
   | 同上，检查 "The `blog-writer` agent cannot call" | 读 `step-6-chart-planning.md` |
   | 同上，检查 "They must not reach the render" 和 "#### 5a. Frontmatter" 的字段 | 读 `step-7-content-writing.md` |
   | 只查「不能出现某句话」的几个测试（固定配图数量、外链图床、旧模型名、"no repeated types per post"） | 改成读 SKILL.md 加全部步骤文件，免得搬走后漏查 |
   | `test_skill_frontmatter.py`、`test_blog_delivery_contract.py`、交付顺序、`hero-credit.txt`、untrusted | 不改，这些文字留在 SKILL.md |

5. 改 `CLAUDE.md` 目录树：`blog-write/SKILL.md` 一行改成目录，列出 `references/` 里的 8 个步骤文件和 2 个原有文件。

#### 输出

- `skills/blog-write/SKILL.md`：约 95 行。
- `skills/blog-write/references/` 下 8 个步骤文件。`delivery.md` 和 `drafting-reference.md` 不变，只改编号。

#### 下游怎么变

不变。跑 `/blog write` 的结果和现在一样，只是每一步读自己的文件。

#### 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-write/SKILL.md` | 只留总控、清单和 Step 9、10 |
| skills/blog-write/references/ 下的 step-1 到 step-8 文件（本分支新建） | 新建，原文搬入 |
| `skills/blog-write/references/drafting-reference.md` | 两处 Phase 编号 |
| `skills/blog-cluster/references/execution-workflow.md` | 一处 Phase 编号 |
| `tests/test_editorial_contracts.py` | 换读的文件，见上表 |
| `CLAUDE.md` | 目录树 |

### 4.2 第二个分支：`feat/blog-write-use-brief`

#### 输入

| 输入 | 拿它做什么 |
|---|---|
| `briefs/[slug]-brief.md` 的 Template 一节 | 定模板，不再自动选 |
| 同上，Search Intent 一节的 Reader task | 定这篇文章要帮读者完成什么，不再问用户 |
| 同上，Target Keywords 一节的 Primary | 主关键词，也用来找对应的 brief |
| 同上，Content Outline 一节（就是第二版大纲） | 定标题、H2 顺序、FAQ，不再出大纲 |
| `skills/blog/templates/[type].md` 的 Evidence gate | 检查这个模板要的证据有没有 |

brief 其余各节（Statistics to Include、内链、E-E-A-T 等）照现在的做法整份交给 `blog-writer`，这个分支不改。

#### 处理步骤

1. Step 2 先找 brief：
   1. 用户给了 brief 路径，就用它。
   2. 没给，就在项目的 `briefs/` 里找 `*-brief.md`（不含 `*-task-brief.md`），比对 Primary 关键词和这次的主题。
   3. 找到一份，必须用。找到多份，停下问用户用哪份。一份都没有，告诉用户「没有找到 brief，按主题写；建议先跑 `/blog brief`」，然后走原流程。
2. 有 brief 时，Step 2 不再问读者和主关键词，只确认输出格式（MDX、markdown、HTML，能自动判断就不问）。
3. 有 brief 时，Step 3 不自动选模板。读 brief 选定的模板文件，检查它的 Evidence gate。证据不够就停下，告诉用户缺什么；不编造，也不自己换模板，因为大纲是按这个模板写的。
4. 有 brief 时，Step 5 不出新大纲，也不再请用户批准。直接用第二版大纲，标题、H2 文字和顺序、FAQ 都不改；只在里面标出配图和图表的位置。
5. Step 7 交给 `blog-writer` 时写明：H2 照第二版大纲，不增不删；大纲里写了 Narrower claim 的地方，按收窄的说法写。
6. Step 8 加两项检查（只在有 brief 时）：文章的模板等于 brief 的模板；文章的 H2 和第二版大纲的 H2 一一对应、顺序相同。
7. 没有 brief 时，Step 3 和 Step 5 完全照旧。
8. 交付总结里写一行：用了哪份 brief，或者没有找到 brief。

#### 输出

不新增文件。文章、交付闸门的产物都和现在一样。

#### 下游怎么变

- `blog-writer` 拿到的大纲从「blog-write 自己出的」变成「brief 的第二版」。
- `blog-cluster` 和 `blog-multilingual` 不受影响：它们的项目里一般没有 brief，会走原流程。
- 总控 `skills/blog/SKILL.md` 和 `orchestration-details.md` 里「Preparation for `/blog write`」写的是「select template」「build the outline from the template」，要加上「有 brief 时用 brief 的」。

#### 改动文件

| 文件 | 改什么 |
|---|---|
| skills/blog-write/references/step-2-topic-understanding.md（第一个分支新建） | 找 brief 的规则 |
| skills/blog-write/references/step-3-template-selection.md（第一个分支新建） | 有 brief 时用 brief 的模板，只查 Evidence gate |
| skills/blog-write/references/step-5-outline.md（第一个分支新建） | 有 brief 时用第二版大纲，只标视觉位置 |
| skills/blog-write/references/step-7-content-writing.md（第一个分支新建） | 交给 `blog-writer` 时的两条要求 |
| skills/blog-write/references/step-8-quality-check.md（第一个分支新建） | 两项检查 |
| `skills/blog-write/SKILL.md` | 清单里 Step 3、5 写明「有 brief 时」 |
| `skills/blog-write/references/delivery.md` | 交付总结模板加一行：用了哪份 brief |
| `skills/blog/SKILL.md`、`skills/blog/references/orchestration-details.md` | Preparation 一句 |
| `skills/blog/references/content-templates.md` | 「How `/blog write` Uses Templates」加一句：有 brief 时用 brief 的模板，只有没有 brief 才自动选 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 没有 brief 就拒绝写（最初第 1 条） | `blog-cluster` 和 `blog-multilingual` 会跑不通。用户改成「有就必须用」 |
| 以 Phase 1.5 为准，把它搬进 brief Step 5 | Phase 1.5 按标题里的字猜，brief Step 5 按排名页的实际格式选，后者有数据依据；而且 brief 的大纲是按它选的模板写的。用户选了以 brief 为准 |
| 一个分支同时拆文件和改行为 | 搬家和改动混在一个 diff 里，不好审，测试挂了也分不清是哪一类引起的。用户选了分两个 |
| 保留 Phase 编号（0、1、1.5 到 7），不改成 Step 1 到 10 | 少改几处指代，但有小数编号，和 brief 的 Step 1 到 10 不一致；以后插步骤更乱 |
| 把交付闸门（Phase 6.5）也搬进步骤文件 | 它是安全的核心，至少 3 个测试要求它在 SKILL.md 里（`test_blog_write_skill_references_contract`、`test_every_write_path_doc_runs_render_then_nonce_then_review_then_gates`、检查 `hero-credit.txt` 的那个）；`CLAUDE.md` 也要求各 skill 只写短版并链接到 `blog-delivery-contract.md`。搬出去收益小、风险大 |
| 有 brief 时仍请用户批准一次大纲 | brief 的第二版大纲已经过自审；课程写明全程已授权时「检查通过后继续执行」（p.127）。如果用户想保留这一问，Step 5 改回「展示大纲，等批准」即可 |
| 内部调用（cluster、multilingual）不检查 brief，只有用户直接跑才检查 | 要按「谁在调用」分支，规则更复杂；按「有没有 brief」分支，效果一样，更简单 |

## 6. 验证

开工前写的是打算怎么验，做完改成实际结果。

### 6.1 第一个分支

| 验证项 | 结果 |
|---|---|
| 内容没丢：把 `main` 上 SKILL.md 每个 Phase 的原文和对应步骤文件逐段比对，只允许标题行和编号指代不同 | 待做 |
| 仓库检查：`python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`（看 errors，不只数 warnings）。`claude plugin validate .` 只允许插件名 `claude-blog` 被保留这一条已知错误 | 待做 |
| SKILL.md 行数，开跑时读进上下文的行数 | 待做（预计 429 行降到约 95 行） |
| 对照瑜东 | 待做。预计：只改文件组织，对应 p.106「每步有输入、产物、验收」的前提；内容不变，不涉及具体某一课 |
| 对照上游原版（`3544423`） | 待做。预计增益：开跑时少读约 330 行；代价：每步多一次读文件。行为不变 |

### 6.2 第二个分支

| 验证项 | 结果 |
|---|---|
| 有 brief：在 claude-seo-playground 用现在的 `/blog brief` 跑一个新关键词（带第二版大纲），再跑 `/blog write`。查：模板等于 brief 的模板；H2 和第二版大纲一一对应、顺序相同；没有再问读者和关键词；没有再请用户批准大纲 | 待做。会花一次完整 brief 的 DataForSEO 和 Firecrawl 积分，开跑前先报预计花费 |
| 没有 brief：空文件夹里只给主题跑 `/blog write`。查：提示「没有找到 brief」，之后和原流程一样 | 待做 |
| 多份 brief：`briefs/` 里放两份同关键词的 brief。查：停下问用户 | 待做 |
| 证据不够：brief 选了 `product-review`，项目里没有亲测记录。查：停下说缺什么，不换模板，不编 | 待做 |
| 仓库检查（同 6.1） | 待做 |
| 对照瑜东 | 待做。预计：有 brief 时符合 p.127「阶段 A 定方向和结构，写作不回头改」；没有 brief 的原流程不符合课程（课程里不存在没有阶段 A 的写作），这是为 cluster 和 multilingual 保留的，单独标出 |
| 对照上游原版（`3544423`） | 待做。上游有 brief 时仍重选模板、重出大纲。拿真实产物比：文章 H2 是否和大纲一致（上游的反例见第 3.2 节） |

## 7. 提交拆分

第一个分支 `refactor/blog-write-step-files`：

```
docs(blog-write): add design for step files and brief use
refactor(blog-write): move each workflow phase into a step file
```

第二个提交同时改步骤文件、测试、`CLAUDE.md` 和 cluster 的一处编号，保证这个提交单独拿出来测试也能全过。

第二个分支 `feat/blog-write-use-brief`：

```
feat(blog-write): follow the brief template, reader task and outline when a brief exists
```

每个分支合并后，在 `main` 上单独提交 `docs: log fork change NNN`。
