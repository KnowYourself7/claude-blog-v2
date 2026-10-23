# 开发文档：blog-brief Step 1.5 按瑜东 A·03 补读者任务、跑题排查和页面建议

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-22 |
| 状态 | 已确认，实现中 |
| 分支 | feat/blog-brief-a03-search-intent（从 main 的 2ce4cd1 开出） |
| 依据 | 瑜东 A·03「搜索意图与页面分流」，`docs/yudong-blog-workflow-小白讲解/02-选题-搜索意图与竞争机会.md`（p.48、p.111 到 112） |
| 改动范围 | `skills/blog-brief/references/step-2-serp-intent-gate.md`、新建 `skills/blog-brief/templates/search-intent.md`、`templates/brief-template.md` 的 Search Intent 段、`references/a05-demand-facets.md` 两处引用、`SKILL.md` 步骤表一行、`CLAUDE.md` 目录树一行 |

## 1. 为什么改

现在的 Step 1.5 只做一件事：调一次 Live SERP，给前 10 条标 blog / product / category / 其他，blog 严格多于其他任一类才继续（PR #5 的简化版）。对照瑜东 02 课，缺的是判定前后的三样东西：

1. **读者任务没写下来。** Step 2 第 10 条按"是否在问读者任务"筛词，第 3、16 条也以它为准，可是没有任何一步把读者任务写成一句话，模型只能临场猜。瑜东把它放在搜索意图单的第一行（p.112："读者的问题：点胶发黏、双色、堵管怎么办？主要在找原因与处理步骤"）。
2. **跑题结果没排查。** 瑜东要求查"意图污染"：工业词的结果里混进消费品、本地服务、品牌导航（p.111）。现在只标页面类型，不看页面讲的是不是这个读者的事。
3. **停下时不说该换什么页面。** 瑜东有一张路由表（p.48）：找型号去产品页，比较系列去分类页，计算去工具页。现在停下只列计数。

另外，判定本身也要换：现在用"严格多数"，瑜东用"博客占比低于 30% 触发意图冲突检查"（p.111，瑜东说明这是内部规则，不是 Google 标准）。用户 2026-10-22 决定换成 30% 线。

## 2. 改完的样子

Step 1.5 产出自己的文件 `briefs/[slug]-search-intent.md`，和 Step 2 的两个产物同一模式，对应瑜东的"搜索意图单"。文件五段对应 p.112 的五行：

| 瑜东搜索意图单（p.112） | 产物里的段落 |
|---|---|
| 读者的问题 | Reader Task，一句 "The searcher wants to ..." |
| 搜索结果类型 | Results 表（Rank、URL、Title、Label、On topic）+ Counts（含 `blog n/10` 算式） |
| 可比页面 | Results 表里标 `blog` 的行 |
| 页面选择 | Decision 的 "Page type that fits the SERP" |
| 不做的推断 | SERP Features 下的固定句：没出现的特征不是需求小或竞争弱的证据 |

简报的 Search Intent 段只留读者任务、计数、判定，分类表链接到这个文件。

## 3. 新 Step 1.5 的顺序

1. 调用不变：一次 Live SERP，`depth: 10`，`noAiMode: true`，失败两次停，不退回 WebSearch。
2. 标签：`blog`、`product`、`category`、`tool`（计算器、换算器），或其他具体类型。只看 URL 和标题，不打开页面。
3. On topic 列：`yes`，或四选一 `consumer`、`local`、`brand`、`other meaning`，取第一个适用的。
4. 计数，写 `blog n/自然结果条数`。
5. 读者任务一句话，从 `blog` 标题和 PAA 归纳。
6. 记 AI Overview、精选摘要有无，加固定句。
7. 三条停止条件任一成立就停：博客占比低于 30%；`tool` ≥ `blog`；跑题 ≥ 5 条。
8. 停下时列计数和示例 URL，按多数标签给建议页面类型，用户三选一，不代选。
9. 存文件；Step 5 把读者任务、计数、判定抄进简报。

## 4. 和瑜东及旧版不同的地方

| 项 | 怎么处理 | 理由 |
|---|---|---|
| 判定规则 | 从"严格多数"改为"低于 30%"，另加 `tool` ≥ `blog` 和跑题 ≥ 5 条 | 用户决定采用瑜东的线。**行为变化**：3 篇博客 7 个产品页，以前停，现在继续。两条附加条件来自 p.111 的"需要换页面"信号（用户要立即使用计算器、在找本地商家）和原型 a03 的停止条件 |
| `local` 放哪 | 规划原定加 `local` 标签；实现时放进 On topic 列，不作标签 | 本地商家既是页面类型也是污染，两边都算会重复计数。放进跑题列，它计入"跑题 ≥ 5 条" |
| 查余额 | 不做 | 属于 A·02，路线图已暂缓；Step 2 也不查 |
| 主计算器判断 | 不做 | 本仓库不产出计算器；`tool` 多就停下 |
| 打开页面判断类型 | 不做 | 沿用 PR #5 的决定，成本和注入风险都低 |
| 博客占比的分母 | 用自然结果条数，不固定 10 | depth 10 时自然结果可能少于 10 条 |

## 5. 验证

1. 仓库检查：`python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`。
2. 子代理跑 3 个模拟 SERP，方法同 PR #5。2026-10-22 已跑，结果：
   - A `2k dispensing problems`（模拟里 blog 2、category 4、product 2、forum 1、video 1）：blog 2/10 = 20%，停，建议分类页。
   - B `2k dispensing gun`（blog 2、category 8）：20%，停，建议分类页。
   - C `epoxy mix ratio by weight`（blog 3、tool 5）：正好 30% 不触发第一条，tool 5 ≥ blog 3 触发第二条，停，建议工具页。
   子代理列了 13 处不清楚的地方，据此补了 4 句：店铺搜索页算 `category`；`brand` 改成"只服务搜该品牌名的页面"；占比同时写百分数；混合 SERP 取最多的标签、并列写两个，等用户回答期间写 `pending`。其余（forum 和 video 不计入任何停止条件、`[slug]` 怎么取）沿用 Step 2 和 PR #5 的现状，不在本分支处理。
3. 真实跑在 `claude-seo-playground`（DataForSEO MCP 只在那里）：`2k dispensing problems` 预期继续，看读者任务是否一句话、On topic 列是否全填、产物文件是否生成；`2k dispensing gun` 预期停下。每次一个 Live SERP 调用 $0.002。顺带核对一件事：`noAiMode: true` 是 PR #7 为避开 40101 错误加的，真实跑时看返回里还有没有 AI Overview；没有的话，第 6 条和 Step 2 第 1 条抄 AI Overview 小节标题的做法要另开分支处理。

## 6. 提交拆分

1. `docs(blog-brief): add design for the Step 1.5 search intent file`
2. `feat(blog-brief): write the reader task and off-topic check in Step 1.5`

## 出处

- 瑜东 02 课：`docs/yudong-blog-workflow-小白讲解/02-选题-搜索意图与竞争机会.md`
- 原型 a03 阶段文件（停止条件、验收）：`/Users/Kai/个人项目/瑜东SEO/.claude/skills/yudong-blog-workflow/stages/a03-search-intent.md`
- 现行闸门方案：`docs/plans/2026-10-17-blog-brief-serp-intent-gate.md`
- 路线图与 A·04 暂缓：`docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节；`docs/plans/2026-10-20-yudong-20-step-gap-analysis.md` P7

> 文件改名说明：步骤文件在 2026-10-22 按 SKILL.md 重排编号（见 `docs/plans/2026-10-22-blog-brief-step-file-format.md`），本文档里的路径已改为新名，正文中的旧步骤号和 a0N 名称保留为历史记录。
