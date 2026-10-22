# 开发文档：blog-brief Step 2 一步完成关键词到需求面

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-22 |
| 状态 | 待实现 |
| 建议分支 | feat/blog-brief-step2-demand-facets |
| 依据 | 瑜东 A·05「从关键词到需求面」 |
| 改动范围 | `skills/blog-brief/SKILL.md` Step 2 和 Step 5，`skills/blog-brief/templates/` 下的三个模板 |

## 1. 为什么改

现在 main 上的 Step 2 只做到"找词"：扩词、去重、删掉明显无关的词，然后把整张词表存进 `briefs/[slug]-keyword-research.md`。skill 里写明了"Do not select keywords"，后面也没有哪一步把词表变成文章结构。Step 5 只从词表里抄焦点词的搜索量、KD 和意图。

瑜东 A·05 在同一步里完成"关键词到需求面"。需求面是读者任务的一个部分，每个面要有"一个明确问题和回答责任"（课程第 115 页），后面的大纲按需求面分节。扩词和归面放在一步里，是因为两者互相决定：归完面才知道够不够，不够就回头补词，再重新归。

我们已经试过一次把需求面拆成单独的 Step 2.2（分支 feat/blog-brief-demand-facets，已放弃）。教训有三条：

1. 要求关键词池每一行都进一个面，结果长尾修饰词决定了结构。亚麻裤（"what to wear with linen pants"）330 行分出 62 个面，保留的 9 个里有 3 个是裤子颜色。
2. 面应该从问题证据里来。那次的 AI Overview 有三个小节：Best Tops to Pair、Shoes & Footwear、Layers & Accessories。可是关键词文件没留这些标题，"上衣"就落选了。
3. 拆成两步以后，"面不够才补 Related Keywords"只能做成 Step 2.2 回头调接口的例外，问题证据也要专门抄进文件才能传给下一步。这两处别扭都是拆步造成的。

## 2. 改完的样子

Step 2 改名为 "Keywords to Demand Facets"，一步产出两个文件：

| 文件 | 作用 | 对应瑜东 |
|---|---|---|
| `briefs/[slug]-demand-facets.md` | 正式产物：保留的面、不保留的面、关键词检查 | `a05-需求面.md` |
| `briefs/[slug]-keyword-research.md` | 证据快照：问题证据、种子、关键词池、剔除类别 | `_snapshots/` |

完成标准：

1. 保留 9 个以内的面。每个面有一句读者问题、证据、代表词和保留理由。
2. 关键词池前 50 行和 Other Sources 的每一行，都挂到一个面上，或者标"other page"。这就是饱和检查：新词都有归属，就不用再扩。
3. 保留的面少于 5 个时，补一轮 Related Keywords。补完仍少于 3 个，就停下问用户。
4. 没有模型自己编的关键词，`null` 不写成 `0`，变体的搜索量不相加。

## 3. 瑜东 A·05 的做法

出处：瑜东 a05 阶段文件（动作 1 到 6 和验收），课程第 78、115、116 页，2026-09-21 的 a05 实跑日志。

| 动作 | 瑜东怎么做 |
|---|---|
| 1 多轮种子扩词 | 焦点词查一轮；再去掉修饰词、保留读者任务核心，缩成 1 到 2 个更短的种子，各查一轮；写明怎么缩、为什么。日志里有两种缩法：去修饰词，或换成同一处境的说法 |
| 1 不够才补 | 合并后独立读者问题少于 5 个，才用 Related Keywords（depth 2）补一轮；够了就停 |
| 1b 自动补全 | 可选；只取问句和新修饰词，给 FAQ 和变体用，不作搜索量依据 |
| 2 筛选 | 先看与客户业务和本文读者任务的相关性，再看搜索量；每个剔除的词类写一句理由 |
| 3 聚类 | 把留下的词和 PAA、相关搜索合在一起，按读者问题聚类；同一问题的不同说法归一面，不同任务即使词根相近也分开 |
| 4 写成问题 | 每个面写成一句完整的读者问题，选一个代表词，列出变体 |
| 5 补口径 | 给代表词和主要变体（最多 30 个）调一次 Keyword Overview |
| 6 定去留 | 通常 5 到 9 个面；低量但重要的面写明理由保留；站内已有覆盖的面只链接不展开 |
| 验收 | 少于 3 个面就停，建议并入别的主题或换词；至少两个种子；`null` 不写成 `0` |

另外，日志里遇到过粒度问题：光头、大块头算不算胡子的变体。产物的做法是把"胡子、光头、体型、长发"并成一面，也就是同一方面的不同取值归一面。

## 4. 现在和改后

| 环节 | 现在的 Step 2 | 改后 |
|---|---|---|
| 产物 | 一张词表，不做取舍 | 需求面文件加关键词快照 |
| 问题证据 | PAA 和相关搜索压平成关键词；池里有的就从 Other Sources 删掉；AI Overview 小节标题不留 | 单独一节 Question Evidence，五类照抄：AI Overview 小节标题、PAA、相关搜索、结果标题、自动补全 |
| 种子 | 焦点词，加 1 到 2 个从结果标题里找的同义说法；结果少于 50 个才缩短 | 照瑜东：种子 2 去掉修饰词（没有修饰词就不做），种子 3 是比焦点词短、说同一任务的说法；写明理由 |
| Related Keywords | 每次都调 | 保留的面少于 5 个才补一轮 |
| 自动补全 | 词进 Other Sources，再调 Overview 取搜索量 | 只把问句和带新修饰词的建议写进问题证据，不取搜索量 |
| 筛选 | 只删 4 类明显无关的词 | 先问"是否在问本文的读者任务"；剔除类别加"同一个词的另一种意思" |
| Overview | 给 Other Sources 的词调 | 只给不在池里的相关搜索调 |
| 归面 | 没有 | 先从问题证据列面，再把关键词挂上去 |
| 去留 | 没有 | 先看证据有几类，再看搜索量，最多保留 9 个 |
| 停止规则 | 没有 | 少于 5 个补词，少于 3 个停 |

## 5. 和瑜东不同的四处

1. 不照搬动作 5（给代表词再调一次 Overview）。第一次真实测试把 546 个词同时发给了 Overview，搜索量、KD、两个意图字段和 Suggestions 返回的完全一样（`/Users/Kai/个人项目/claude-seo-playground/briefs/matching-outfits-for-couples-test-notes.md` 第 5 节）。再调只多花钱。
2. 不用业务背景。瑜东筛选和去留都看客户业务，这次先不加，产物里写明"未用业务背景"。业务背景以后单独一个分支。
3. "读者问题少于 5 个"改成"保留的面少于 5 个"。读者问题就是面，归完面才数得出来。
4. 不做"站内已有覆盖"的检查。它需要站点数据，以后单独一个分支。

## 6. 新 Step 2 的顺序

1. 收集问题证据：沿用 Step 1.5 的 Live SERP 返回，再调一次自动补全。
2. 种子扩词：两到三个种子，各调一次 Keyword Suggestions。
3. 去重、按 `core_keyword` 分组、排序，得到关键词池。
4. 按读者任务筛选，两张表都筛。
5. 给不在池里的相关搜索调 Overview，补搜索量。
6. 存关键词快照。
7. 从问题证据列面，同一方面的不同取值归一面。
8. 读池子前 50 行和 Other Sources，把每行挂到面上，或开新面，或标"other page"。
9. 选代表词，按证据类数和搜索量排序，保留前 9 个。
10. 少于 5 个面：补一轮 Related Keywords，重做第 8、9 步。少于 3 个：停。
11. 存需求面文件。

## 7. Step 2 英文草稿

已按 simple-english skill 写，指令句不超过 20 个词，条件放在指令前面。

```markdown
### Step 2: Keywords to Demand Facets

Turn the keywords of the topic into demand facets. A demand facet is one
part of the reader task. The reader task is what the searcher of the
focus keyword wants to do or know. Step 5 gives each kept facet at least
one H2.

In this step, you fill two templates:
`${CLAUDE_SKILL_DIR}/templates/keyword-research.md` for the keyword
evidence, and `${CLAUDE_SKILL_DIR}/templates/demand-facets.md` for the
facets. Take the volume, KD, and intent only from the DataForSEO Labs
responses. Write `null` for a missing value, not `0`. Do not add the
volumes of two keywords.

Use the Step 1.5 Live SERP response again. Send the other calls with
`mcp__dataforseo__api_request`. Use `noAiMode: true`, `location_code: 2840`,
and `language_code: "en"`. If the user names another market, use the codes
of that market. If a call fails two times, stop. Tell the user the reason.
Do not use WebSearch.

#### Evidence and keywords

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
12. Save the filled keyword template as
    `briefs/[slug]-keyword-research.md`.

#### Facets

13. List each item of the Question Evidence section.
14. Merge the items into facets. If two items differ only in one value,
    put them in one facet. For example, black and white linen pants
    differ only in the color. List the values in the facet.
15. If an item asks about another task, put it in the Other Facets table.
    Give the reason "other page".
16. Read the first 50 rows of the Keyword Pool and all rows of Other
    Sources. If a row restates the focus keyword, attach it to the focus
    keyword. If a row answers a facet, attach it to that facet. If a row
    names a new part of the reader task, add a facet for it. If a row
    fits no facet, mark it "other page".
17. For each facet, use the attached keyword with the highest volume as
    the representative keyword. If volumes are equal, use the row that
    comes first in the keyword file. Copy its volume, KD, and intent. If
    a facet has no attached keyword, write `-`.
18. Count the evidence types of each facet. There are six types: the five
    parts of Question Evidence, and the attached keyword rows. Sort the
    facets by this count, from high to low. If counts are equal, sort by
    the volume of the representative keyword. Put a facet with `-` after
    the facets with a volume. If volumes are also equal, keep the order
    of the keyword file.
19. Keep the first 9 facets. Put the others in the Other Facets table
    with the reason "lower rank".
20. If you keep fewer than 5 facets, call
    `POST /v3/dataforseo_labs/google/related_keywords/live` for the focus
    keyword with `depth: 2`. Read `core_keyword` from
    `keyword_data.keyword_properties`. Add the keywords to the Keyword
    Pool with items 5 to 8 and 10. Record the call in the Data Scope
    table. Save the keyword file again. Then do items 16 to 19 again. Do
    this item only one time.
21. If you keep fewer than 3 facets after item 20, stop. Tell the user
    that this keyword is possibly too narrow for one post. Ask the user
    to write anyway, try another keyword, or end.
22. Save the filled facet template as `briefs/[slug]-demand-facets.md`.
```

## 8. 模板改动

### 8.1 关键词快照 `skills/blog-brief/templates/keyword-research.md`

| 节 | 改动 |
|---|---|
| Data Scope | 调用表改成：Live SERP（沿用 Step 1.5）、Google Autocomplete、每个种子的 Keyword Suggestions、Keyword Overview（或"未调用"）、Related Keywords（"未调用"，或"第 20 条补词"） |
| Question Evidence | 新加。五个小表或列表：AI Overview 小节标题、PAA、相关搜索、结果标题（带 Step 1.5 标签）、自动补全 |
| Seeds | 加"怎么缩、为什么"一列；去掉"结果少于 50 个才缩短"的说明 |
| Keyword Pool | 不变 |
| Other Sources | 只放不在池里的 PAA 和相关搜索；来源列去掉 autocomplete |
| Removed Keywords | 类别加 other meaning of the same word |
| Not in Overview、SERP Features | 不变 |

### 8.2 需求面模板 demand-facets.md（新建，放在 `skills/blog-brief/templates/` 下）

| 节 | 内容 |
|---|---|
| 表头 | 焦点词、日期、关键词快照文件名、"No business context was used" |
| Focus Keyword | 复述焦点词的行号 |
| Kept Facets | ID、读者问题、取值、证据（例如 `AIO: Best Tops to Pair`）、证据类数、代表词、搜索量、KD、意图、挂上的行号、保留理由 |
| Other Facets | ID、读者问题、证据、不保留的理由（other page 或 lower rank） |
| Keyword Check | 池子前 50 行：挂上几行、开了几个新面、几行标 other page；Other Sources：挂上几行，共几行；是否补过 Related |

### 8.3 简报模板 `skills/blog-brief/templates/brief-template.md`

- Target Keywords 加一行 Demand facets，链接需求面文件。
- 每个 H2 块加一行 Facets，写这一节覆盖的面 ID。

## 9. SKILL.md 其他地方

1. Step 5 加一条规则（原文已和你确认过）：

   ```markdown
   - **Content Outline**: cover each kept Step 2 facet in at least one H2.
     One H2 can cover more than one facet. The facet order does not set the
     H2 order. Write the facet IDs in each H2.
   ```

2. Step 5 的 Target Keywords 规则不变，仍从关键词快照抄焦点词的数据。
3. Step 2.5 不变。它用的"Step 2 keywords"仍在关键词快照里。
4. 开头的 description 不变。

改完 SKILL.md 约 260 行，约 3,800 个 token，在 500 行、5,000 个 token 的上限内。

## 10. 不做

- 业务背景，以及按业务定去留。
- 每个面的 SERP 重合度检查（判断"要不要单独成页"）。
- 站内撞题检查。
- 可赢性结论。
- 让 Step 3 竞品分析、Step 4 统计数据按需求面来做（瑜东 A·06、A·07 的做法）。
- 发布后要在 GSC 追踪的目标词。
- 脚本和新测试。

## 11. 提交拆分

这是一个功能，但改动分两块，建议分开提交，任何一个都能单独撤回：

1. `docs(blog-brief): add design for Step 2 keywords to demand facets`：本文档。
2. `feat(blog-brief): turn Step 2 into keywords to demand facets`：SKILL.md Step 2、关键词快照模板、新的需求面模板。
3. `feat(blog-brief): cover demand facets in the brief outline`：Step 5 的 Content Outline 规则和简报模板。
4. 合并后：`docs/FORK-DEVLOG.md` 补 007（PR #7，目前漏记）和本分支的条目。

测试产物不放进本仓库，不单独提交（见第 12 节第 4 条）。

## 12. 测试计划

1. 跑 `python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`。
2. 在 claude-seo-playground 新开会话，用真实数据跑 Step 1 到 Step 2：
   - "what to wear with linen pants"：和第一次的 62 个面对比。预计保留上衣、鞋、外套和配饰、裤子颜色等面，颜色合成一面。
   - "2k dispensing problems"（瑜东课堂案例）：词窄，用来测"少于 5 个面补 Related"这条路径。也可以和瑜东的 9 个需求分面对照。
   - 按上次的单价估算，每个词约 0.1 美元。
3. 逐条核对第 2 节的完成标准，用脚本数关键词检查的行数，不靠眼数。
4. 测试产物和笔记留在 playground 的 `briefs/` 目录（`/Users/Kai/个人项目/claude-seo-playground/briefs/`），不放进本仓库。PR 描述里写明测试结论和这个位置。

## 出处

- 瑜东 a05 阶段文件：`/Users/Kai/个人项目/瑜东SEO/.claude/skills/yudong-blog-workflow/stages/a05-demand-facets.md`
- 瑜东 a05 实跑日志（两种缩法、粒度问题、概览也不保证 KD）：`/Users/Kai/个人项目/瑜东SEO/log/yudong-blog-workflow/2026-09-21-a05-多种子与概览补口径.md`
- 瑜东课程第 78、115、116 页：`/Users/Kai/个人项目/瑜东SEO/sources/瑜东谷歌SEO线下课-结构化.md`
- 第一次需求面测试（62 个面、AI Overview 小节标题）：`/Users/Kai/个人项目/claude-seo-playground/briefs/what-to-wear-with-linen-pants-test-notes.md`
- Overview 与 Suggestions 数值相同（不在仓库里）：`/Users/Kai/个人项目/claude-seo-playground/briefs/matching-outfits-for-couples-test-notes.md`
- DataForSEO 解析 AI Overview：https://dataforseo.com/help-center/parse-google-ai-overviews-ai-mode
- Google 的 query fan-out（把一个问题拆成子话题分别搜索），经第三方转引：https://www.aleydasolis.com/en/ai-search/google-query-fan-out/
