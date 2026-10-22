# 测试记录：blog-brief Step 1.5 和 Step 2（matching outfits for couples）

日期：2026-10-21。市场：`location_code` 2840，`language_code` "en"。

被测文件（未改动）：

- `/Users/Kai/个人项目/github-skills/claude-blog-v2/skills/blog-brief/SKILL.md`
- `/Users/Kai/个人项目/github-skills/claude-blog-v2/skills/blog-brief/templates/keyword-research.md`

Step 1：焦点词 "matching outfits for couples"。没有 BRAND.md，没有业务背景。受众按话题推断为"想穿情侣装的情侣"。

输出文件：`briefs/matching-outfits-for-couples-keyword-research.md`。

## 1. API 调用

共 8 次调用：Step 1.5 一次，Step 2 七次。工具都是 `mcp__dataforseo__api_request`，没有失败，没有重试。

| # | 步骤 | 方法和路径 | 请求体 | `noAiMode` | 返回条数 | `total_count` | 费用（美元） |
|---|------|-----------|--------|-----------|---------|---------------|-------------|
| 1 | 1.5 | `POST /v3/serp/google/organic/live/advanced` | `{"keyword": "matching outfits for couples", "depth": 10, "location_code": 2840, "language_code": "en"}` | 默认（false） | 12 个 SERP 元素：1 AI Overview、8 organic、1 images、1 PAA（4 个问题）、1 related searches（8 个） | 无此字段 | 响应里没有（AI 模式去掉了 `cost`） |
| 2 | 2.1 | `POST /v3/serp/google/organic/live/advanced` | 同上 | true | `items_count` 11：1 AI Overview、8 organic、1 images、1 related searches（8 个），没有 PAA | 无此字段（`se_results_count` 162） | 0.002 |
| 3 | 2.3 | `POST /v3/dataforseo_labs/google/keyword_suggestions/live` | `{"keyword": "matching outfits for couples", "location_code": 2840, "language_code": "en", "limit": 300}` | true | 300 | 312 | 0.048 |
| 4 | 2.3 | 同上 | `keyword` 改为 "matching couple outfits"，其余同上 | true | 300 | 409 | 0.048 |
| 5 | 2.3 | 同上 | `keyword` 改为 "his and hers matching outfits"，其余同上 | true | 23 | 23 | 0.01476 |
| 6 | 2.5 | `POST /v3/dataforseo_labs/google/related_keywords/live` | `{"keyword": "matching outfits for couples", "location_code": 2840, "language_code": "en", "depth": 2}` | true | 27（含 depth 0 的种子词本身） | 27 | 0.01524 |
| 7 | 2.6 | `POST /v3/serp/google/autocomplete/live/advanced` | `{"keyword": "matching outfits for couples", "location_code": 2840, "language_code": "en", "client": "gws-wiz-serp"}` | true | 10（第 1 条是焦点词本身） | 无此字段 | 0.002 |
| 8 | 2.11 | `POST /v3/dataforseo_labs/google/keyword_overview/live` | `keywords` 共 547 个（546 个关键词池拼写 + 1 个 Autocomplete 词），`location_code` 2840，`language_code` "en" | true | 546 | 无此字段 | 0.07752 |

响应里能看到的费用合计 0.20752 美元。第 1 次调用的费用没有显示。

大响应的体积：Suggestions 每次约 1.15 MB，Overview 约 8.1 MB。它们都超过了工具的输出上限，被存成文件，我用 Python 读完整个 JSON 再处理。

## 2. Step 1.5 闸门结果

闸门停止：`blog` 没有多于其他标签。

| # | 域名 | 标题 | 标签 |
|---|------|------|------|
| 1 | kennyflowers.com | Matching Couples Outfits & Swimwear \| His & Hers Swim | category |
| 2 | dresslily.com | Matching Couple Outfits | category |
| 3 | pinterest.com（`/trouse101/couples-outfit-choices/`） | 290 Couple's Outfit choices ideas in 2026 | image board |
| 4 | amazon.com（`/couples-matching-outfits/s?k=...`） | Couples Matching Outfits | category |
| 5 | pinterest.com（`/ideas/color-matching-couple-outfits/`） | Color Matching Couple Outfits | image board |
| 6 | diyanu.com（`/blogs/fashion/his-and-hers-matching-outfits-for-every-occasion`） | His and Hers Matching Outfits for Every Occasion | blog |
| 7 | my-couple-goal.com（`/collections/couple-clothes`） | Matching Couple Outfits | category |
| 8 | pinterest.com（`/ideas/matching-couple-travel-outfits/`） | Matching Couple Travel Outfits | image board |

计数如下：

- category 4。例：`https://www.kennyflowers.com/collections/matching-couples-outfits`
- image board 3。例：`https://www.pinterest.com/trouse101/couples-outfit-choices/`
- blog 1。例：diyanu.com 那篇。

按 skill，这里要问用户"照写 / 换词 / 结束"。这是测试，所以没有问，直接继续 Step 2。

对照：Step 2 第 2 次调用拿到的 organic 结果用同样规则标注，是 category 4、blog 3（diyanu.com、seventeen.com、otaa.com）、image board 1。结论相同，都是停止，但计数不同。

## 3. 同义种子

| 种子 | 来源 | Suggestions 结果 |
|------|------|------------------|
| matching outfits for couples | 焦点词 | 300 / 312 |
| matching couple outfits | 第 2 次调用的 organic 第 8 位：seventeen.com，标题以 "25 Matching Couple Outfits" 开头，URL `/fashion/style-advice/g27526501/matching-couple-outfits/` | 300 / 409 |
| his and hers matching outfits | 第 2 次调用的 organic 第 5 位：diyanu.com，标题 "His and Hers Matching Outfits for Every Occasion"，URL `/blogs/fashion/his-and-hers-matching-outfits-for-every-occasion` | 23 / 23 |

没有选的候选有三个：

- shinesty.com 的 "Couples Matching Suits and Dresses"。它只限西装和裙子，范围更窄。
- otaa.com 的 "Matching Attire for Couples"。它只限婚礼。
- shein.com 的 "Couple Matching looks"。它是店铺页。

两个种子的效果：

- "matching couple outfits" 带来 297 个新词，和种子 1 只重复 1 个。原因是 Suggestions 按词形匹配，"couple" 和 "couples" 被当成不同的词。
- 这个种子在 Overview 里和焦点词在同一个 `core_keyword` 组，搜索量都是 14800。它确实是"同一个东西的另一种说法"。
- "his and hers matching outfits" 只返回 23 个，全部是新词。

## 4. 短种子

没有做短种子。焦点词的 `total_count` 是 312，不低于 50，所以 Step 2.4 不触发。

## 5. 关键词池

| 项目 | 数值 |
|------|------|
| 原始条数（Suggestions 300+300+23，Related 27） | 650 |
| 忽略大小写去重后 | 630（重复 20 个） |
| 按 `core_keyword` 分组（剔除前） | 318 组 |
| 剔除的拼写 | 84 个，整组被删 48 组 |
| 剔除后 | 546 个拼写，270 组 |
| 只有 1 个拼写的组（剔除前） | 200 组 |
| `core_keyword` 字符串本身不在池里的组（剔除后） | 38 组 |
| 最大的组 | `core_keyword` "matching couples wedding outfits"，15 个拼写，主关键词 "couples matching outfits for wedding"（210，7 个拼写并列 210） |
| 只来自 Related 的词 | 8 个，其中 5 个被剔除 |

去重只合并了大小写相同的拼写。Labs 返回的都是小写，所以去重只发生在不同调用之间。

Overview 之后主关键词变化的组数，按两种比较口径：

- 和 `core_keyword` 字符串比：42 组变了。其中 38 组是因为 `core_keyword` 字符串不是池里的拼写，主关键词只能是别的拼写。真正因为变体搜索量更高而变化的有 4 组：
  - "formal matching outfits for couples"（210）→ "matching outfits for couples formal"（480）
  - "matching plus size couple outfits"（20）→ "plus size matching outfits for couples"（40）
  - "matching his and hers nike outfits"（10）→ "his and hers matching nike outfits"（30）
  - "couple matching outfits for party"（10）→ "couples matching outfits for party"（20）
- 和 Suggestions/Related 自带的搜索量比：0 组。546 个词的 Overview 搜索量、KD、`main_intent`、`foreign_intent` 和 Labs 返回的值完全相同。只有 `monthly_searches` 不同：Labs 给 12 个月，Overview 给 17 到 105 个月。

并列：270 组里有 58 组，最高搜索量由 2 个以上拼写并列。例：焦点词组的 8 个拼写都是 14800。

## 6. 剔除的类别

按 skill 的顺序判断，每个词用第一个符合的类别。

| 类别 | 数量 | 关键词 |
|------|------|--------|
| other audience | 5 | matching nike outfits for family, matching nike outfits for father and son, nike two piece set for woman, date night outfits for ladies, nike matching set hoodie and sweatpants |
| other task | 42 | matching outfits for couples roblox, matching roblox outfits for couples, roblox matching outfits for couples, matching couple outfits roblox, roblox matching couple outfits, roblox matching outfits couple, matching couple roblox outfits, matching outfits for couples roblox codes, cute matching outfits for couples roblox, cute couple matching outfits roblox, couple matching outfits codes, matching outfits for couples berry avenue, matching couple outfits berry avenue, gacha club matching outfits for couples, gacha club couple matching outfits, gacha life matching outfits for couples, gacha life matching couple outfits, imvu matching couple outfits, matching couple outfits imvu, matching gta 5 couple outfits, matching couple outfits gta, matching bitmoji outfits for couples, bitmoji matching outfits for couples, matching couple bitmoji outfits, best matching bitmoji outfits for couples, cute matching bitmoji outfits for couples, cute matching couple bitmoji outfits, matching bitmoji outfits for couples country, matching snapchat outfits for couples, matching snapchat #outfits for couples, matching outfits on snapchat for couples, matching outfits for couples on snapchat, snapchat matching outfits for couples, matching outfits for couples snapchat, couple matching outfits snapchat, matching outfits for couples on snap, matching snap outfits for couples, instagram captions for couples matching outfits, matching outfits for couples quotes, matching couple outfits quotes, matching couple outfits meme, old couple matching outfits meme |
| store or platform navigation | 37 | 店铺：amazon matching outfits for couples, matching outfits for couples amazon, amazon matching couple outfits, matching couple outfits amazon, matching tropical outfits for couples amazon, matching outfits for couples shein, shein matching outfits for couples, shein matching couple outfits, shein couple matching outfits, matching couple outfits on shein, matching couple outfits shein, matching beach outfits for couples shein, matching tropical outfits for couples shein, matching couple outfits vacation shein, his and hers matching outfits shein, asos matching couple outfits, matching outfits for couples fashion nova, fashion nova matching couple outfits, fashion nova couple matching outfits, matching couple outfits fashion nova, rosegal matching outfits for couples, patpat matching outfits for couples。平台：matching outfits for couples pinterest, matching couple outfits pinterest, couple matching outfits pinterest, instagram matching couple outfits, matching couple outfits instagram, instagram cute matching outfits for couples, instagram matching african outfits for couples, korean couple matching outfits instagram, japanese couple matching outfits instagram, old japanese couple matching outfits instagram, cute couple matching outfits tumblr, dope matching outfits for couples tumblr, matching couple outfits tumblr, matching couple outfits polyvore, couple matching outfits tiktok |
| business conflict | 0 | 没有业务背景，所以没有词 |

skill 说"不确定就保留"。我拿不准而保留的词如下：

- nike matching outfits
- matching christmas outfits for couples and dog
- couples matching african outfits for family
- anime couple matching outfits
- matching emoji outfits for couples
- cringe matching couple outfits
- ugly matching couple outfits
- near me、where to buy、for sale、stores 这类没有指名店铺的购买词

保留的产品品牌：nike、adidas、jordan、champion、gucci、louis vuitton、burberry、tommy hilfiger、true religion、gymshark、hello kitty、disney。

## 7. null 和 0

统计对象是发给 Overview 的 547 个词。

| 情况 | 数量 |
|------|------|
| Overview 没有返回这个词 | 1（matching outfits for couples plus size，来自 Autocomplete） |
| 搜索量 `null` | 1（就是上面这个词） |
| 搜索量 `0` | 11 |
| KD `null` | 90（Overview 返回了但 KD 是 null 的 89 个，加上没返回的 1 个） |
| KD `0` | 352，其中 351 个搜索量大于 0。焦点词本身搜索量 14800，KD 也是 0 |
| `main_intent` 为 `null` | 1（没返回的那个词） |

## 8. skill 或模板不清楚、矛盾或需要我猜的地方

1. Step 1.5 没有要求 `noAiMode: true`，Step 2 要求了。我按字面让 Step 1.5 用默认 AI 模式。结果 Step 1.5 的响应里没有 `cost`、`items_count`、`se_results_count`，只能估算费用。
2. Step 2 说"不使用其他步骤的数据"，所以同一个关键词的 Live SERP 要调用两次。两次只隔几十秒，结果却不一样。Step 1.5 有 4 个 PAA，Step 2 一个都没有。8 个 organic 结果里只有 diyanu.com 和 amazon.com 两个域名重复。所以本次关键词研究的 PAA 是 0，Step 1.5 看到的 4 个 PAA 问题被丢弃了。
3. 种子数量"1 or 2"：skill 没有说什么时候选 1 个、什么时候选 2 个。我选了 2 个。
4. "Each one names the same thing for the same audience"：skill 自己的例子 "his and hers matching outfits" 只覆盖异性情侣，比 "couples" 范围窄。我按例子照用。"couple" 和 "couples" 只差一个词形，算不算"另一种说法"也要我判断。
5. `limit: 300` 截断了结果。种子 1 少拿 12 个（312 − 300），种子 2 少拿 109 个（409 − 300）。skill 没有说要不要用 `offset` 翻页。Suggestions 按搜索量从高到低排序，所以被截掉的是搜索量最低的词。种子 1 第 300 条的搜索量已经是 0，种子 2 是 10。
6. Related Keywords 的结果里包含 depth 0 的种子词本身。skill 没有说要不要保留它。它和焦点词同一个拼写，去重后没有影响。
7. 分组规则只写了"没有 `core_keyword` 的词，加上指向它的词，组成一组"。没有说 `core_keyword` 字符串不在池里时怎么办。本次有 38 组是这种情况。我按 `core_keyword` 字符串分组，但没有把这个字符串当作拼写发给 Overview，因为它不是"pool spelling"。
8. 剔除规则作用在"两张表"上，但关键词池的一行是一个组。skill 没有说剔除按拼写还是按整组。我按拼写剔除。本次没有一个组被剔除了一部分，所以结果没有差别。
9. 店铺和品牌的边界：SHEIN 和 Fashion Nova 是卖自有品牌的零售网站，既像店铺又像品牌。我按店铺剔除。Google 的 related searches 里也有 "Matching outfits For Couples shein"。
10. "platform navigation" 的边界：Instagram、Pinterest、Tumblr、TikTok 这类词，可能是想去那个平台，也可能是想看那个平台上的穿搭灵感。我按平台导航剔除。
11. 游戏和头像里的情侣装（Roblox、Bitmoji、Snapchat 等）我归为 other task，memes、quotes、captions 也归为 other task。skill 没有给 other task 的例子，这些都是我的判断。
12. "business conflict" 在没有业务背景时怎么处理，skill 没有说。我写了 0 个，并在原因里说明。
13. 国家词（canada、australia、kenya、nigeria、india、south africa）不属于四类中的任何一类，所以保留。skill 没有"其他市场"这一类。
14. Step 2.11 要发"every Autocomplete and related search word"。但 Step 2.9 已经把池里有的词从其他来源表里删掉了。8 个 related searches 和 9 个 Autocomplete 词都在池里，它们作为池拼写已经发出，所以 Other Sources 只有 1 个词。这里没有矛盾，但要读两遍才确定。
15. Overview 的数据和 Suggestions/Related 自带的数据完全相同（搜索量、KD、两个意图字段，546 个词全部一致）。在本次测试里，Overview 是最贵的一次调用（0.07752 美元），只多给了更长的 `monthly_searches`。
16. 主关键词并列：58 组的最高搜索量有 2 个以上拼写并列，因为 Google 给相近拼写同一个数。skill 没有给并列规则。我的规则是：如果 `core_keyword` 拼写在并列里就选它，否则选 Labs 返回顺序里的第一个。
17. 模板的组行写一个 Search volume、KD、Intent，但没有说是主关键词的值还是全组合计。我用主关键词的值。合计会重复计算，因为相近拼写共用同一个数。
18. Peak month：Overview 在 `noAiMode: true` 下返回最多 105 个月，最早到 2018 年。按字面"monthly_searches 里最高的月份"，焦点词的峰值是 2022 年 1 月（60500，8 个月并列）。最近 12 个月的峰值是 18100，2026 年 6 到 8 月和 2025 年 10 月并列。所以按字面得到的是历史峰值，不是季节性。270 行里有 134 行峰值并列。模板格式 `[month: n]` 没有年份，我加了年份，并标出并列月份数。
19. "Not in Overview" 一节写"Overview returned no data"。我只列了没有返回的 1 个词，没有列 KD 为 null 的 89 个词，因为它们有搜索量。这一节要不要包括部分为 null 的词，模板没有说清楚。
20. Step 2.1 要求拿 organic 标题和 URL，但模板里没有放它们的位置。它们只用来选种子。
21. Source 列：一个组可能来自多个来源（例如 suggestions (seed 1)、related、suggestions (seed 2)）。模板只给了 "[suggestions (seed n) / related]" 的单值格式。我用逗号连接多个来源。
22. AI Overview 的引用里有 "Google"（Google Shopping 商品链接），它不算真正的发布者。我把它写成 "Google (Shopping product listings)"。
23. Step 1.5 的 Pinterest ideas 页在 DataForSEO 里带 `is_video: true`。skill 说按 URL 和标题标注，所以我标成 image board，没有标 video。
24. SKILL.md 开头要求在加载项目上下文之前先读 `orchestration-details.md`。本次任务明确只跑 Step 1、1.5、2，而且没有 BRAND.md，所以我没有读。

## 9. 数据观察（不是 skill 文本问题）

- 焦点词的 `main_intent` 是 informational，但 SERP 上大多是店铺分类页。意图字段和 SERP 实际情况不一致。
- 焦点词的 `search_volume_trend` 是 −18%（月、季、年都是）。它的年搜索量从 2021 年的约 60500 降到现在的 14800。
- Related Keywords 的 depth 2 结果偏离主题：只来自 Related 的 8 个词里有 5 个被剔除（Nike 单人套装、家庭装、父子装）。
