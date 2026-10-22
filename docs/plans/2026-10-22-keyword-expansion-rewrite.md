# 方案：Step 2 扩词按瑜东 A·05 重写

- 日期：2026-10-22
- 状态：方案，第 7 节两项已定（2026-10-22，均按推荐）。实现分支 feat/blog-brief-demand-facets 已放弃，skill 未改。本方案留作下次开发的依据
- 依据：瑜东 a05 阶段文件动作 1、1b、2、5，课程第 115 页，2026-09-21 a05 实跑日志
- 配套：`docs/plans/2026-10-22-demand-facets-rewrite.md`（Step 2.2 第二版）

## 1. 一句话

种子词改成瑜东的"焦点词加缩短的种子"；Related Keywords 改成"读者问题不够才补"；自动补全只取问句和新修饰词；筛选先问"是否回答本文的读者任务"。

## 2. 逐项对照

| 环节 | 瑜东 a05 | 现在的 Step 2 | 改成 |
|---|---|---|---|
| 种子 | 焦点词一轮，再去掉修饰词、保留读者任务核心，缩成 1 到 2 个更短的种子，各查一轮；写明怎么缩、为什么（动作 1） | 焦点词，加 1 到 2 个从结果标题里找的同义说法；焦点词结果少于 50 个才缩短 | 照瑜东的两种缩法：种子 2 去掉修饰词，焦点词没有修饰词就不做；种子 3 换成比焦点词短、说同一任务的说法；写明理由 |
| Related Keywords | 合并后独立读者问题少于 5 个才补一轮，depth 2；够了就停（动作 1） | 每次都调，depth 2 | 照瑜东：Step 2.2 保留的面少于 5 个时补一轮，见第 4 节 |
| 自动补全 | 可选；只取问句和新修饰词，给 FAQ 和变体用；不作搜索量依据（动作 1b） | 每次都调；词进 Other Sources，再调 Overview 取搜索量 | 照瑜东：调一次，只把问句和新修饰词写进 Question Evidence，不取搜索量 |
| 筛选 | 先看与客户业务和本文读者任务的相关性，再看搜索量；每个剔除的词类写一句理由（动作 2） | 只删 4 类明显无关的词，拿不准就留，不按搜索量或意图删 | 先问"是否回答本文的读者任务"；剔除词类加瑜东的"无关同名"；业务一项这次不用（你已定） |
| Overview | 聚类后给代表词和主要变体（最多 30 个）补一次，统一 KD 和意图（动作 5） | 只给 Other Sources 的词调 | 只给关键词池里没有的相关搜索调。不照搬动作 5，理由见第 3 节 |

## 3. 两处不照搬，以及理由

1. 不照搬动作 5（给代表词再调一次 Overview）。瑜东这样做，是因为他的实跑里 Suggestions 和 Related "不稳定返回 KD"。我们第一次真实测试把 546 个词同时发给了 Overview，搜索量、KD、两个意图字段和 Suggestions、Related 返回的完全一样。再调一次只多花钱，数值不会变。
2. 不照搬第 78 页"保留约 60 到 100 个词"。那一页是建站阶段的全站关键词筛选，不是单篇文章的 A·05。

## 4. Related Keywords 为什么放到 Step 2.2 触发

瑜东的判断条件是"合并后独立读者问题少于 5 个"。读者问题要到 Step 2.2 归完面才数得出来。所以 Step 2.2 加一条：保留的面少于 5 个时，调一次 Related Keywords，把新词加进关键词文件，再从挂词那一步重做一遍。重做后仍少于 3 个，才停下问你。

代价是 Step 2.2 会在这种情况下调一次接口，和"Step 2.2 不调接口"的原设计不同。见第 7 节决定 1。

## 5. Step 2 草稿（英文）

```markdown
### Step 2: Keyword Research

Find the keywords for the reader task. The reader task is what the
searcher of the focus keyword wants to do or know. Remove only the
keywords that do not ask about the reader task. Do not select keywords.
Step 2.2 does that.

In this step, you fill `${CLAUDE_SKILL_DIR}/templates/keyword-research.md`.
Take the volume, KD, and intent only from the DataForSEO Labs responses.
Write `null` for a missing value, not `0`.

Use the Step 1.5 Live SERP response again. Send the other calls with
`mcp__dataforseo__api_request`. Use `noAiMode: true`, `location_code: 2840`,
and `language_code: "en"`. If the user names another market, use the codes
of that market. If a call fails two times, stop. Tell the user the reason.
Do not use WebSearch.

1. Question evidence is the text that shows what readers ask. Copy four
   parts of it from the Step 1.5 response into the Question Evidence
   section: the AI Overview section titles (`ai_overview_element.title`),
   the PAA questions, the related searches, and the organic titles. Add
   the Step 1.5 label to each organic title.
2. Call `POST /v3/serp/google/autocomplete/live/advanced` one time for
   the focus keyword, with `client: "gws-wiz-serp"`. A modifier is a word
   that narrows the reader task, for example a color or an audience. Add
   these suggestions to the question evidence, as its fifth part: the
   questions, and the suggestions that add a modifier. Do not use the
   suggestions for volume.
3. Make two or three seeds. A seed is a keyword that you send to Keyword
   Suggestions. Seed 1 is the focus keyword. For seed 2, remove the
   modifiers from the focus keyword. If the focus keyword has no
   modifier, do not make seed 2. For seed 3, write another phrase for the
   same reader task. It must be shorter than the focus keyword. In the
   Seeds section, write how and why you made each seed.
4. Call `POST /v3/dataforseo_labs/google/keyword_suggestions/live` one
   time for each seed, with `limit: 300`.
5. Remove exact duplicates from the results. Ignore letter case.
6. Group the keywords by `core_keyword`, from `keyword_properties`. A
   keyword without `core_keyword` forms one group with the keywords that
   point to it. Each group is one row of the Keyword Pool.
7. In each row, the main keyword is the spelling with the highest volume.
   If volumes are equal, use the `core_keyword` spelling. If that spelling
   is not in the row, use the first spelling in the call order: seed 1,
   seed 2, seed 3.
8. Sort the rows of the Keyword Pool from the highest volume to the
   lowest. If volumes are equal, keep the call order.
9. Put the PAA questions and the related searches that are not in the
   Keyword Pool into the Other Sources table.
10. From both tables, remove the keywords that do not ask about the
    reader task. The classes are other audience, other task, other
    meaning of the same word, store or platform navigation, and business
    conflict. Give each removed keyword the first class that applies, in
    this sequence. A product brand, for example nike, is not a store. If
    you are not sure, keep the keyword. Do not remove a keyword for its
    volume or intent. Give one reason for each class.
11. Call `POST /v3/dataforseo_labs/google/keyword_overview/live` for the
    related searches in the Other Sources table. If no related search
    stays in the table, do not call it.
12. Save the filled template as `briefs/[slug]-keyword-research.md`.
```

Step 2.2 加的 Related 补词规则在需求面方案第 5 节第 8 条，只写在那一处，这里不重复。

本节已按 simple-english skill 改写（2026-10-22）。

## 6. 亚麻裤按新种子会怎样（推演，不是测试结果）

- 种子 1：what to wear with linen pants。
- 种子 2：不做。草稿把修饰词定义为"缩小读者任务的词"，比如颜色、人群。"what to wear with linen pants" 里没有这样的词，每个词都属于任务本身。
- 种子 3：linen pants outfit。比焦点词短，说的是同一个任务。上次测试里它带回了 3600 的 "linen pants outfit"，比焦点词的 1900 还高。
- Related Keywords：不调。上次光是三个种子就有 300 多个词，面数应当够 5 个。
- 自动补全：上次返回的是 "women casual"、"women summer"，按新规则只作为新修饰词写进问题证据。

## 7. 两项决定

已定：Related Keywords 在 Step 2.2 面少于 5 个时才补；不照搬动作 5。下面是当时的选项和理由。

1. Related Keywords 怎么补。推荐：Step 2.2 面少于 5 个时补一轮（第 4 节），最贴近瑜东"不够才补"。另两种做法是每次都调（现状），或者完全去掉。
2. 动作 5 的 Overview 要不要照搬。推荐：不照搬，理由见第 3 节第 1 条。

## 8. 范围提醒

加上这份方案，这个分支会改 Step 2、Step 2.2 和两个模板。上一次 DataForSEO 分支就是因为一次改太多被放弃的。建议分两个提交：一个只改扩词，一个只改需求面，任何一个都能单独撤回。

## 9. 测试计划

1. 跑项目四项检查。
2. 在 playground 真实重跑亚麻裤的 Step 1 到 Step 2.2，和第一版对比。按上次的单价估算，约 0.1 美元。第 6 节推演的两个种子上次都调过，但实跑时模型选的种子 3 可能不同，所以仍要真实跑一次。

## 出处

- 瑜东 a05 阶段文件：`/Users/Kai/个人项目/瑜东SEO/.claude/skills/yudong-blog-workflow/stages/a05-demand-facets.md`
- 瑜东 a05 实跑日志（两种缩法、长种子让 Suggestions 结果很少、概览也不保证 KD）：`/Users/Kai/个人项目/瑜东SEO/log/yudong-blog-workflow/2026-09-21-a05-多种子与概览补口径.md`
- 瑜东课程第 78、115 页：`/Users/Kai/个人项目/瑜东SEO/sources/瑜东谷歌SEO线下课-结构化.md`
- Overview 与 Suggestions 数值相同：`eval/blog-brief-keyword-research/2026-10-21-matching-outfits-for-couples/matching-outfits-for-couples-test-notes.md` 第 5 节
- 亚麻裤第一次真实测试（不在仓库里）：`/Users/Kai/个人项目/claude-seo-playground/briefs/what-to-wear-with-linen-pants-test-notes.md`
