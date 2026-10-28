# 开发文档：Step 3 按「焦点词扩需求问题」重做

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-28 |
| 状态 | 已实现，检查已过，未提交 |
| 分支 | feat/upgrade-step-1-topic-intake（用户 2026-10-28 定：直接在这个分支上改，不另开） |
| 依据 | 瑜东步骤 05「关键词 → 需求面」（p.115 到 116）：扩展问题（自动补全、相关搜索、其他用户还问了）、合并需求（同义去重、按问题与任务聚类）、排优先级（需求 × 业务价值，选代表词不堆词）、补 AI 信号（生成式搜索量、回答引擎引用基线）；红线「AI 信号记录来源、地区、时间、查询条件，不与 Google 月量相加」「被 AI 引用 ≠ 带来流量或询盘」 |
| 用户决定 | 2026-10-28 给出五步：焦点词扩问题，不够 9 个再去修饰词扩种子词重跑；合并；排优先级；补 AI 信号。同日定：9 数的是第 1 步去重后的问题条数；脚本加 expand、volume、ai，删 pool、related、remove；AI 信号这次只做 AI 搜索量 |
| 来源 | `docs/reviews/2026-10-27-step-3-vs-yudong-a05.md`：现在的 Step 3 缺趋势和 AI 信号，种子词只往短往宽扩 |

## 1. 目标

跑 `/blog brief` 到 Step 3 时，需求面从「读者会怎么问」扩出来，而不是从 Labs 给的一堆关键词里挑；问题不够就自动放宽种子词再扩一轮；每个面带 Google 搜索量和 AI 搜索量两个数，分开看。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 趋势检查（`historical_keyword_data`） | 另一个分支。`keyword_overview` 已经返回 monthly_searches，脚本有 peak_month，先看够不够 |
| 站内已有覆盖检查 | Step 1 的 Existing Pages 表做了撞题；按面查覆盖等内链分支 |
| 回答引擎引用基线的完整版（按问题查谁被引用） | LLM Mentions 的请求字段官方概览页没写，先只做 AI 搜索量；引用基线列为第二个提交，字段核实后做 |
| 分面合计列 | 维持不相加。瑜东记的是合计，我们只记代表词的量，开发文档记成有意不同 |

## 3. 原因

现在的 Step 3 先用 Labs `keyword_suggestions` 给三个种子词各拉 300 个关键词，再让模型从前 50 行里挑面。问题有三个。一是起点是「词」不是「问题」：PAA 和自动补全只当证据，不当面的来源，而瑜东的第一个动作就是扩问题。二是种子词固定三个一轮，不够只补一次 `related_keywords`，没有「不够就放宽」的循环。三是没有 AI 信号。2026-10-27 的对照评审把后两条记为缺口。

## 4. 方案

### 4.1 接口（都经 `mcp__dataforseo__api_request` 或脚本的 REST 调用，市场代码来自任务单）

| 用途 | 接口 | 关键参数 | 返回 |
|---|---|---|---|
| 自动补全 | `serp/google/autocomplete/live/advanced` | `keyword`, `client: "gws-wiz-serp"`, `noAiMode: true` | 建议词，含问题 |
| PAA 和相关搜索 | `serp/google/organic/live/advanced` | `keyword`, `depth: 10`, `people_also_ask_click_depth: 2`（1 到 4，每点一层加一点费用） | `people_also_ask` 项（含 `seed_question`）、`related_searches` 项 |
| 相关关键词 | `dataforseo_labs/google/related_keywords/live` | `keyword`, `depth: 2`（最多 72 个；3 是 584）, `limit: 100` | 每个词的 `search_volume`、`keyword_difficulty`、`main_intent` |
| 搜索量、难度、意图 | `dataforseo_labs/google/keyword_overview/live` | `keywords`（一次最多 700） | 同上，缺值为 `null` |
| AI 搜索量 | `ai_optimization/ai_keyword_data/keywords_search_volume/live` | `keywords`（最多 1000）, `location_code`, `language_code` | `ai_search_volume`、`ai_monthly_searches`（12 个月）。官方说明：按 PAA 的统计推算 |
| 引用基线（第二个提交） | `ai_optimization/llm_mentions/top_mentioned_domains_lite/live` 等 | 待核实 | 谁在 AI 回答里被引用 |

### 4.2 处理步骤（Step 3 的 Actions）

1. 扩问题，沿焦点词：三个调用各一次（自动补全、带 PAA 点击深度的 SERP、相关关键词）。收成「需求问题」：PAA 问题、自动补全里的问题、相关搜索和相关关键词里加了新修饰词的条目。记每条的来源。不满 9 条去第 2 步，满了去第 3 步。
2. 扩种子词：去掉焦点词的修饰词得到更宽的种子词（没有修饰词就用同一读者任务的更短说法），对它再做第 1 步。最多一轮，防止费用失控。合并两轮的问题。
3. 合并需求：同义去重，按问题和任务聚成面；只差一个值的（黑亚麻裤、白亚麻裤）合成一个面并列出值；不属于本读者任务的进 Other Facets，理由 `other page`。
4. 排优先级：每个面的候选词一次 `keyword_overview` 拿量、难度、意图；代表词取面内搜索量最高的一个，不堆词；业务价值按任务单 Sells 和 Does not sell or claim 标 `in` / `out`，匹配产品线的低量面保留并写明。脚本 `rank-facets` 排序（证据类型数，再搜索量）。
5. 补 AI 信号：代表词一次 `keywords_search_volume`，每个面加 `AI search volume` 一列，表头写明来源、地区、语言、日期；和 Google 量分开两列，不相加。
6. 面少于 3 个就停下问（写也行、换词、结束）。填两个模板。

### 4.3 输出

| 文件 | 变化 |
|---|---|
| `briefs/[slug]-keyword-research.md` | Question Evidence 按来源分组（PAA、Autocomplete、Related searches、Related keywords），加「轮次」列；Seeds 表记两轮 |
| `briefs/[slug]-demand-facets.md` | Kept Facets 表加 AI search volume 列；表下一行写 AI 量的来源、地区、时间、查询条件 |
| 脚本工作文件 | `-questions.json` 和 `.md`（两轮问题、调用、费用）、`-facets.json`、`-facet-tables.md`。旧的 `-keyword-pool`、`-evidence.json`、`-removed.json` 不再产生 |

### 4.4 脚本 `skills/blog-brief/scripts/keyword_pool.py`

| 子命令 | 变化 |
|---|---|
| `expand` | 新。对一个种子词发三个调用（Autocomplete；organic SERP 带 `people_also_ask_click_depth 2`；Related Keywords depth 2），按小写、单空格、去末尾标点去重，同一条文本记多个来源，报告总数和 `short`（少于 `--min`，默认 9） |
| `volume` | 新。对没有量的行调 `keyword_overview`（每次最多 700 个），缺值 `null`，查不到的记进 No Overview Data |
| `ai` | 新。对保留面的代表词调 `keywords_search_volume`，写 AI search volume 列和「端点、市场、日期」一行 |
| `rank-facets` | 保留，排序键从「证据类型数」改成「来源数」（脚本从挂上的行自己数，不再由模型填 evidence_parts）。仍保留前 9 个；9 的上限没改，另议 |
| `pool`、`related`、`remove` | 删。Labs `keyword_suggestions` 的 300 词池不再是起点 |

### 4.5 下游

Step 4 到 Step 8 读 Kept Facets 的 ID、问题和代表词，列名不变，不受影响。Step 11 阶段门按 ID 查面，不受影响。

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 保留 `keyword_suggestions` 词池，问题扩展只当补充 | 两套起点并存，模型又要在 300 个词里挑。用户定的是从问题出发 |
| 模型直接调 MCP，不改脚本 | 去重、排序、计数回到手工，#17 之前的毛病（每次结果不同）会回来 |
| PAA 点击深度 4 | 费用翻倍，问题多半重复；先用 2，不够再放宽种子词 |
| AI 搜索量和 Google 量合成一列 | 瑜东红线：不相加，分开看 |

用户 2026-10-28 定下的三件事：9 数的是第 1 步去重后的问题条数；脚本按 4.4 扩并删旧子命令和它们的测试；AI 信号只做 AI 搜索量，引用基线另提交。

## 6. 验证

| 验证项 | 打算怎么验 |
|---|---|
| 仓库检查 | pytest 1541 passed、55 skipped；lint_prose 本分支文件 0 处；validate_skills 通过；consistency_check errors 为空 |
| 脚本 | `tests/test_keyword_pool.py` 重写，12 条，用固定响应走完 expand 两轮、volume、rank-facets、ai；`null` 不写成 0；全过 |
| 模拟跑（子代理，只读步骤文件、模板、脚本 help） | 报 9 处要猜、9 处三方不一致。已改：expand 命令写全必填参数和市场代码；facets.json 的字段名在步骤文件里写全；`volume` 提到合面之前，低量面保留的判断有数可看；不挂的行统一进 keyword-research 的 Removed Rows，`out` 面只指业务范围外；少于 3 个面的停下挪到 `ai` 之前，省一次付费调用，并写明「照写」和「换词」各去哪；action 7 写明先填哪份、SERP Features 从 search-intent 文件抄；模板说明 `-` 和 `null` 的区别、Sources 写来源名；脚本 help 补 `--out`、`--keep` 默认值 |
| 真实跑 | 没做。要在 playground 用 `can you wear linen in winter` 跑 Step 3，看两轮问题数、面数、五个调用的费用 |

## 7. 提交拆分

1. `docs(blog-brief): add design for Step 3 question expansion`
2. `feat(blog-brief): expand demand questions from the focus keyword and widen the seed when short`
3. `feat(blog-brief): add AI search volume to the demand facets`
