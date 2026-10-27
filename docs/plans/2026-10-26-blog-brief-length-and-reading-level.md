# 开发文档：brief 按文章角色和读者定篇幅与难度

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-26 |
| 状态 | 已实现，未提交 |
| 分支 | `feat/blog-brief-length-and-reading-level`，从合并了 #24 的 `main`（`9ee27bf`）开 |
| 依据 | 瑜东第 06 课：字数只是容纳完整回答的结果（p.130）。第 01 课 Ebestron 任务启动单写了「交付约 2.8K 词」，篇幅在开工时作为估计写下（p.108）。Google 有用内容指南（2026-10-05 更新）问作者是不是为了字数而写，答案是 `(No, we don't.)`，https://developers.google.com/search/docs/fundamentals/creating-helpful-content |
| 用户决定 | 2026-10-26：brief 要按读者任务、读者画像和文章定位（pillar 还是 cluster）定篇幅长短和难易；skill 文字用精简准确的技术英语 |

## 1. 目标

跑 `/blog brief` 时，brief 的篇幅估计和可读性目标按这篇文章的角色（pillar、cluster 或独立文章）、读者和读者任务来定，不再是写死的「2,000 到 2,500 词、写给专家看」。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 写作风格：连接词、习语、语气 | 不做。`VOICE.md` 管风格，blog-write 已经读它 |
| 自己定新的字数或年级阈值 | 不做。只用仓库里已有的表，见第 3.3 节 |
| cluster 文章链到它的 pillar 页 | 同站页面清单那份计划（2026-10-24-blog-brief-internal-link-pages.md，还没提交）的事 |
| 修 `content-rules.md` 和 `cluster-architecture.md` 的 pillar 字数不一致（3,000 到 4,000 对 2,500 到 4,000） | 以后另开 `fix/` 小分支。本分支只用 `cluster-architecture.md` 一处 |
| Step 5 按 Role 选模板（pillar 用 pillar-page） | 以后单独讨论 |
| 直接读 persona 文件的可读性档 | 不做。`blog-brand` 生成 `VOICE.md` 时已经把 persona 的档写进 Readability target |
| brief 模板里其他没写来源的占位符（Format、备选标题、E-E-A-T、Distribution Plan） | 上游原有的问题，以后另开分支 |
| blog-write 怎么用这两个值 | 不改。blog-write 已经把 brief 整份交给写稿子代理，基线和新版实跑都照 brief 的字数写 |
| 写成文章后按字数拦截 | 不做。字数只是估计（p.130） |

## 3. 原因

### 3.1 现在的问题

brief 模板写死了两行（`skills/blog-brief/templates/brief-template.md` 的 Content Parameters）：

- `Word count: [2,000-2,500] words`
- `Reading level: Flesch 60-70 (expert-accessible)`

上游原版也是这两行，fork 拆步骤时原样保留：

- 出处：`git show 3544423:skills/blog-brief/SKILL.md` 第 143、144 行。

### 3.2 真实例子

两次实跑的对比：

1. 2026-10-25 的基线 brief 照抄了这两行。测试场的 `VOICE.md` 第 49、50 行却写着 consumer 档、年级 6 到 8、Flesch Ease 60 到 80。`BRAND.md` 也写着读者「需要明确的穿搭答案，而不是时尚理论」。brief 和品牌自己的设定冲突，写出的文章有 3,258 词。
2. 2026-10-26 的新版实跑，你在 brief 跑完后手动改成「1,500 词、9 年级能看懂」。ChatGPT 的消费者视角评价把这篇的可读性打到三篇最高（8.5），还说篇幅最短的一篇得分最高。

这一步现在靠人手改，skill 不会自己做。

### 3.3 仓库里已经有规则，brief 没用

| 文件 | 已有的规则 |
|---|---|
| `skills/blog/references/content-rules.md` 的 Readability Bands by Audience | consumer：年级 6 到 8、Flesch Ease 60 到 80；professional（B2B）：8 到 10、50 到 60；technical：10 到 12、30 到 50。有 persona 时用 persona 的档 |
| `skills/blog-cluster/references/cluster-architecture.md` | pillar：2,500 到 4,000 词；cluster 文章（spoke）：1,200 到 1,800 词 |
| `skills/blog/templates/*.md` 的 Target Word Count | 每个模板自带一个范围，例如 how-to-guide 2,000 到 2,500 |
| `skills/blog-brand/SKILL.md` 生成的 `VOICE.md` | Readability target 一节：Audience tier、Flesch Grade、Flesch Ease |

这些都是仓库自己的规划范围，不是 Google 标准，`content-rules.md` 也这么写了。本分支只是让 brief 读它们。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 用户的话 | 文章角色：pillar、cluster 或 standalone |
| `briefs/[slug]-task-brief.md` 的 Reader 行和新的 Role 行 | 定可读性档和字数范围 |
| `briefs/[slug]-search-intent.md` 的 Reader Task | 在范围里取低端还是高端 |
| SKILL.md 已经加载的 `VOICE.md` | 有 Readability target 就直接用 |
| `skills/blog/references/content-rules.md` 的 Readability Bands by Audience | 没有 `VOICE.md` 时，按 Reader 选档 |
| `skills/blog-cluster/references/cluster-architecture.md` | pillar 和 cluster 的字数范围 |
| Step 5 选定模板的 Target Word Count | standalone 文章的字数范围 |

### 4.2 处理步骤

1. Step 1 的 Delivery 表加一行 Role，三个值：
   - `pillar`：一个大主题的核心页，同主题的 cluster 文章都链向它。
   - `cluster`：回答大主题下的一个子问题，链回它的 pillar。
   - `standalone`：两者都不是。
   用户没说时，按 Positioning 起草，标 `draft:`，和别的草稿一起问。
2. Step 9 填 Content Parameters 的两行：
   1. Reading level：`VOICE.md` 有 Readability target，就照抄。没有，就按 Reader 行从 Readability Bands by Audience 选一档。写出档名、年级范围和 Flesch Ease 范围。
   2. Word count：先按 Role 定范围。pillar 和 cluster 用 `cluster-architecture.md` 的范围，standalone 用模板的 Target Word Count。再看 Reader Task：只问一个问题、能直接回答的，取低端；要一整份指南或几个决定的，取高端。写成「约 N 词（规划估计，不是目标）」，并写出依据的范围。
3. Step 9 的 Positioning 一节加一行 Role。
4. brief 模板的 Content Parameters 两行改成占位符，说明从哪来。
5. 测试：Step 9 读任务单的行名测试加上 Role。

「只问一个问题取低端」是本 skill 自己的规则，课程和 Google 都没有，skill 文字里写明。

#### 实现中按检查结果做的调整

新旧对照和模拟跑（见第 6 节）找出的问题，按下面改了：

1. Role 草稿一律写 `standalone`，不按 Positioning 推。pillar 还是 cluster 要看站点结构，从定位推不出来，交给用户确认。
2. 取低端还是高端，改成数 search intent 文件里 Reader Task 的需求：一个需求取低端，两三个取中间，整个主题的指南取高端。原来的「只问一个问题」对不上 Reader Task 的写法（它是一句「The searcher wants to…」）。
3. 选可读性档时，按读者是谁对 Audience 列，不按话题对。读者是 `missing` 或对不上任何一档时，用 `content-rules.md` 表下面的默认值（7 到 8 年级、Flesch Ease 60 到 70）。`VOICE.md` 的 Readability target 要有实际数值才照抄。
4. 有 4 个模板（data-research、faq-knowledge、news-analysis、tutorial）写的是 Target Length，不是 Target Word Count，两种都认。
5. 删掉 Step 9 里重复的「规划估计」规则，模板里已经写了。原来两条只讲道理的句子，改成一条禁止：不能把字数说成目标或 Google 的要求。
6. 模板的可读性一行改用来源里的叫法 Flesch Grade、Flesch Ease，来源一栏写明是 `VOICE.md`、读者画像还是默认值。

### 4.3 输出

| 文件 | 变化 |
|---|---|
| `briefs/[slug]-task-brief.md` | Delivery 表多一行 Role |
| `briefs/[slug]-brief.md` | Positioning 一节多一行 Role。Word count 和 Reading level 写的是推出来的值和依据 |

### 4.4 下游怎么变

- blog-write 的写稿子代理拿到的字数和可读性目标随文章变，不再一律 2,000 到 2,500 词。
- 用这次的亚麻例子推一遍：Role 是 cluster（站内已有男士亚麻总指南），范围 1,200 到 1,800 词；Reader Task 是「什么时候太冷、怎么叠穿」，两个需求，取中间约 1,500 词；`VOICE.md` 写的是 consumer、6 到 8 年级。结果和你手动改的「1,500 词、9 年级以内」一致，模拟跑也得到同样的值。
- 已知的遗留：Step 5 选模板时不看 Role，所以 pillar 文章可能选到 how-to-guide 而不是 pillar-page 模板；blog-write 选模板那一步还会读模板自带的字数。前者以后单独讨论，后者归 blog-write 计划文档（让 brief 的值优先）。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-1-topic-intake.md` | Delivery 一步加 Role 的三个值和起草规则 |
| `skills/blog-brief/templates/task-brief.md` | Delivery 表加 Role 行 |
| `skills/blog-brief/references/step-9-generate-brief.md` | Inputs 加 `VOICE.md`、两份参考文件和模板；Steps 写两行的定法；Check 加一条 |
| `skills/blog-brief/templates/brief-template.md` | Positioning 加 Role；Content Parameters 两行改占位符 |
| `tests/test_blog_brief_workflow.py` | Step 9 的行名加 Role |

### 4.6 分支顺序

Role 行要加进 `feat/blog-brief-positioning` 新建的 Delivery 表。两种做法：

1. 先推送 `feat/blog-brief-positioning`、开 PR、合并，再从最新的 `main` 开本分支（推荐）。一个分支一件事，PR 也好审。
2. 从 `feat/blog-brief-positioning` 上接着开本分支（堆叠分支）。不用等合并，但前一个 PR 改了，本分支要跟着变基。

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 自己定一张「读者任务 × 角色」的字数表 | 课程和 Google 都没有这样的表，仓库里已经有规划范围。新表只会多一套要维护的数字 |
| 按竞品排名页的平均字数定 | 要多抓页面或多算一步，而且照竞品长度写正是「为字数而写」 |
| 在 Step 1 就写死字数 | Step 1 还不知道读者任务（Step 2 才从搜索结果读出来），也不知道模板（Step 5） |
| 交给 blog-write 自己定 | brief 是给人审的计划，篇幅和难度应该在动笔前定好、能被看到 |
| Role 不进任务单，只在 Step 9 推断 | pillar 还是 cluster 是站点结构决定，只有人知道，步骤 01 的工具一栏是「人工 / 客户资料」 |

## 6. 验证

| 验证项 | 结果 |
|---|---|
| 仓库检查：`python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`（看 errors） | 通过。完整测试 1543 个通过、56 个跳过，两条新测试先失败后通过（Step 9 读 Role 行；模板里不再有写死的字数和 expert-accessible）。按检查结果改完措辞后，brief 相关的 75 个测试复跑通过。skill 校验通过；破折号违规只在被 git 忽略的 `docs/yudong/`；一致性检查只剩未提交的 blog-write 计划文档的 6 个旧错误 |
| 新旧对照（子代理）：改前改后的 Step 1、Step 9 和两份模板 | 做了。找出 4 处含义变化（其中「读者对不上任何一档时没有兜底」是意外丢失）、7 处两读、7 处重复或冲突、6 处要猜。按 4.2 节「实现中按检查结果做的调整」修了，没修的写进第 2 节 |
| 模拟跑（子代理）：只按新文件做 Step 9 三次，输入用 2026-10-26 新版实跑的真实 brief 产物，只改 Role 和 Reader | 做了，用的是按检查结果修改前的文件。三次 Check 全过，结果见 6.1 节。子代理指出的两处要猜的地方已按调整第 2、3 条改 |
| 真实跑 | 没做。本分支只改 Step 1 的一行和 Step 9，不调接口；模拟跑用的已经是真实 brief 产物 |
| 对照瑜东 | 符合。篇幅在开工时作为估计写下，对应 Ebestron 任务启动单的「交付约 2.8K 词」(p.108)；模板写明「规划估计」，Step 9 禁止把字数说成目标，对应「字数只是容纳完整回答的结果」(p.130)。按需求数取低、中、高端是本 skill 自己的规则，课程没有，skill 文字里写明了 |
| 对照上游原版（`3544423`） | 增益：上游写死「2,000 到 2,500 词、Flesch 60-70 (expert-accessible)」，和测试场 `VOICE.md` 的 consumer 6 到 8 年级冲突。新版按角色、读者和读者任务推出，亚麻例子推出约 1,500 词、6 到 8 年级，和用户手动改的值一致。代价：Step 1 多一个草稿要确认；Step 9 多读三个文件。未验证：用推出来的值写成文章，读者体验是否更好 |

### 6.1 Step 9 模拟跑的结果

| 情况 | Word count | Reading level |
|---|---|---|
| cluster，有 `VOICE.md` | 约 1,500 词，1,200 到 1,800 取中间 | consumer，6 到 8 年级，来自 `VOICE.md` |
| pillar，B2B 读者，无 `VOICE.md` | 约 3,250 词，2,500 到 4,000 取中间 | professional，8 到 10 年级，来自读者画像 |
| standalone，无 `VOICE.md` | 约 2,250 词，how-to-guide 的 2,000 到 2,500 取中间 | consumer，6 到 8 年级，来自读者画像 |

三次都取中间，因为 Reader Task 有两个需求：什么时候太冷、怎么叠穿。

## 7. 提交拆分

```
docs(blog-brief): add design for length and reading level from the post role and reader
feat(blog-brief): set the length estimate and reading level from the role, reader, and VOICE.md
```
