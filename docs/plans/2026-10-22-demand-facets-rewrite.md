# 方案：Step 2.2 需求面重写（第二版）

- 日期：2026-10-22
- 状态：方案，第 7 节三项已定（2026-10-22，均按推荐）。实现分支 feat/blog-brief-demand-facets 已放弃，第一版的设计和 skill 改动没有合入 main。本方案留作下次开发的依据
- 依据：`docs/plans/2026-10-22-demand-facets-vs-yudong.md` 第 5 节
- 配套：`docs/plans/2026-10-22-keyword-expansion-rewrite.md`。按它的第 4 节，面少于 5 个时 Step 2.2 会调一次 Related Keywords，这是"不调接口"的唯一例外
## 1. 一句话

先从搜索结果里的问题证据列出"答案由哪几部分组成"，再把关键词挂上去当证据。关键词不再生成面。

## 2. 和第一版的区别

| | 第一版（已测试，不能用） | 第二版 |
|---|---|---|
| 面从哪来 | 330 行关键词逐行归组 | AI Overview 小节标题、PAA、相关搜索、结果标题 |
| 一个面是什么 | 一个修饰词的一个取值（黑色裤） | 答案的一个部分（裤子颜色），取值列在面里 |
| 关键词的作用 | 每行必须进一个面 | 挂在面下当证据，用来选代表词、补漏掉的面 |
| 饱和检查 | 生成规则：330 行全部归面 | 验收：读前 50 行，挂不上的要么开新面，要么标"别的页面" |
| 复述焦点词的词 | 自成一面（F1） | 归焦点词，不占面 |
| 排序 | 代表词搜索量 | 先看有几类证据，再看搜索量 |
| 代表词 | 只从关键词池取 | 两张表里挂上的词，取搜索量最高的 |
| 业务背景 | 没提 | 不用，产物里写明"未用业务背景"（见第 7 节决定 2） |

## 3. 为什么从问题证据出发

- 瑜东课程第 115 页：从"我要覆盖哪些词"，转向"读者需要解决哪些问题"；每个面要有"一个明确问题和回答责任"。
- Google 官方说 AI Mode 用 query fan-out（把一个问题拆成几个子话题分别搜索）。AI Overview 的小节标题就是 Google 自己拆出来的子话题。
- DataForSEO Live SERP 的 `ai_overview_element` 带 `title` 字段。亚麻裤这次的返回里有三个小节标题：Best Tops to Pair、Shoes & Footwear、Layers & Accessories。第一版看不到这条证据，"上衣"才会落选。

## 4. 改动清单

1. `skills/blog-brief/templates/keyword-research.md`：加一节 Question Evidence，放五类问题证据：四类来自 Step 1.5 的返回，第五类是自动补全（见扩词方案）。PAA 和相关搜索全部照抄，不管它们在不在关键词池里。现在的 Other Sources 会删掉池里已有的词，所以看不出哪些词出现在相关搜索里。
2. `skills/blog-brief/SKILL.md` Step 2：加一条，从 Step 1.5 的返回把问题证据抄进上面那一节。不新调接口。
3. `skills/blog-brief/SKILL.md` Step 2.2：按第 5 节重写。
4. 在 `skills/blog-brief/templates/` 下新建 demand-facets.md，结构见第 6 节。
5. `skills/blog-brief/templates/brief-template.md`：Target Keywords 加一行 Demand facets，链接需求面文件。每个 H2 块加一行 Facets，写这一节覆盖的面 ID。
6. `skills/blog-brief/SKILL.md` Step 5 加一条 Content Outline 规则，原文如下（第一版已经和你确认过）：

   ```markdown
   - **Content Outline**: cover each kept Step 2.2 facet in at least one H2.
     One H2 can cover more than one facet. The facet order does not set the
     H2 order. Write the facet IDs in each H2.
   ```

7. 设计文档：实现时以本方案和扩词方案为准，不另写。
8. 第一版的测试产物没有保留在仓库里。亚麻裤真实测试的原始文件在 `/Users/Kai/个人项目/claude-seo-playground/briefs/`，主要数字记在对比文档第 2 节。

## 5. Step 2.2 草稿（英文）

```markdown
### Step 2.2: Demand Facets

A demand facet is one part of the reader task. Step 5 gives each kept
facet at least one H2. In this step, you fill
`${CLAUDE_SKILL_DIR}/templates/demand-facets.md`. Read the Step 2 file
`briefs/[slug]-keyword-research.md`. Do not call an API, except in item 8.

1. List each item of the Question Evidence section.
2. Merge the items into facets. If two items differ only in one value,
   put them in one facet. For example, black and white linen pants differ
   only in the color. List the values in the facet.
3. If an item asks about another task, put it in the Other Facets table.
   Give the reason "other page".
4. Read the first 50 rows of the Keyword Pool and all rows of Other
   Sources. If a row restates the focus keyword, attach it to the focus
   keyword. If a row answers a facet, attach it to that facet. If a row
   names a new part of the reader task, add a facet for it. If a row fits
   no facet, mark it "other page".
5. For each facet, use the attached keyword with the highest volume as
   the representative keyword. If volumes are equal, use the row that
   comes first in the file. Copy its volume, KD, and intent. Do not add
   the volumes of the attached keywords. If a facet has no attached
   keyword, write `-`.
6. Count the evidence types of each facet. There are six types: the five
   parts of Question Evidence, and the attached keyword rows. Sort the
   facets by this count, from high to low. If counts are equal, sort by
   the volume of the representative keyword. Put a facet with `-` after
   the facets with a volume. If volumes are also equal, keep the order of
   the file.
7. Keep the first 9 facets. Put the others in the Other Facets table with
   the reason "lower rank".
8. If you keep fewer than 5 facets, call
   `POST /v3/dataforseo_labs/google/related_keywords/live` for the focus
   keyword with `depth: 2`. Read `core_keyword` from
   `keyword_data.keyword_properties`. Add the keywords to the Keyword
   Pool with the rules of Step 2, items 5 to 8 and 10. Record the call in
   the Data Scope table of the Step 2 file. Save that file again. Then do
   items 4 to 7 again. Do this item only one time.
9. If you keep fewer than 3 facets after item 8, stop. Tell the user that
   this keyword is possibly too narrow for one post. Ask the user to write
   anyway, try another keyword, or end.
10. Save the filled template as `briefs/[slug]-demand-facets.md`.
```

本节已按 simple-english skill 改写（2026-10-22）。"reader task" 的定义在 Step 2 开头。

## 6. 新模板的结构

| 节 | 内容 |
|---|---|
| 表头 | 焦点词、来源文件、日期、"No new API calls"、"No business context was used" |
| Focus Keyword | 复述焦点词的行号 |
| Kept Facets | ID、读者问题、取值、证据（例如 `AIO: Best Tops to Pair`、`related: tops to wear with linen pants`）、证据类数、代表词、搜索量、KD、意图、挂上的行号 |
| Other Facets | ID、读者问题、证据、不保留的理由 |
| Keyword Check | 前 50 个池行：挂上几行、开了几个新面、几行标"别的页面" |

## 7. 三项决定

已定：问题证据抄进关键词文件；这次不加业务背景；饱和检查读前 50 行。下面是当时的选项和理由。

1. 问题证据放在哪。推荐：Step 2 抄进关键词文件，Step 2.2 只读文件。另一种做法是 Step 2.2 直接读 Step 1.5 的返回，但这要依赖对话上下文，而且你的规则是跨步骤复用要由你决定。
2. 业务背景要不要这次加。推荐：这次不加，产物写明"未用业务背景"，业务背景留给以后单独一个分支。原因是一个分支只做一个功能，而 4d7beed 加过一次又撤销了。
3. 关键词检查读多少行。推荐：前 50 行。关键词池按搜索量排序，第一版两次测试里，长尾行大多只是重复的修饰词组合。另一种做法是读全部行，覆盖更全，但输出会很长。

## 8. 亚麻裤按第二版会是什么样（手工推演，不是测试结果）

问题证据（来自已存的 Step 1.5 返回）：

- AI Overview 小节：Best Tops to Pair、Shoes & Footwear、Layers & Accessories
- PAA：What is the rule for wearing linen?、Are linen pants in style in 2026?、What to wear with wide leg pants over 50?、What color goes best with linen pants?
- 相关搜索：what to wear with linen pants men、what to wear with linen pants women's、tops to wear with linen pants、what top to wear with wide leg linen trousers、how to style wide leg linen pants plus size、how to wear wide leg linen pants over 60、what shoes to wear with wide leg linen pants、linen pants women
- 结果标题：女性穿搭、阔腿裤 5 套搭配、InStyle 的 10 款上衣等 7 条

预计的面：上衣、鞋、外套和配饰、裤子颜色、男士和女士、裤型（阔腿等）、年龄和体型、穿搭规则。"Are linen pants in style in 2026?" 进 Other Facets，理由是"别的页面"。上衣有 AI Overview、相关搜索、结果标题、关键词 4 类证据，会排在前面。

## 9. 测试计划

1. 跑项目四项检查。
2. 和扩词一起，在 playground 真实重跑亚麻裤，和第一版对比。做法见扩词方案第 9 节。
3. 情侣装那次被闸门拦下，不是真实会写的词，这次不重跑。

## 出处

- 瑜东课程第 115 页：本地文件 `/Users/Kai/个人项目/瑜东SEO/sources/瑜东谷歌SEO线下课-结构化.md`
- Google 对 query fan-out 的说明，经第三方转引（AI Mode 发布文和 I/O 2025 文章；2025 年 12 月写进 Search Central 文档）：https://www.aleydasolis.com/en/ai-search/google-query-fan-out/
- DataForSEO 解析 AI Overview 的说明：https://dataforseo.com/help-center/parse-google-ai-overviews-ai-mode
- `ai_overview_element.title` 字段：亚麻裤真实测试的 Live SERP 返回（playground 会话的已存工具结果），本次用脚本读出
