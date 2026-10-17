# 方案评估：blog-brief 用 DataForSEO Live SERP 判定搜索意图

- 日期：2026-10-17
- 状态：待确认（未写代码）
- 涉及：`skills/blog-brief/SKILL.md` Step 1 / Step 2

## 1. 需求原文

Step 1 的 search intent 改为调用 DataForSEO Live SERP，取 Top 10，统计博客页占比；
博客页占比最多才继续，否则停止并提示"搜索意图不是博客"。

## 2. 必要性判断：需要做

| 问题 | 现状 | 结论 |
|---|---|---|
| 意图从哪来 | Step 1 让用户填或"从上下文推断"，Step 2 用 WebSearch 顺带"看一眼" | 没有证据，全靠猜 |
| WebSearch 能替代吗 | 自带 WebSearch 不是 Google 真实排名，也拿不到固定的 Top 10 | 不能 |
| 不做的代价 | 关键词首页全是商品页时，照样写完整篇简报和文章，排名机会很低 | 浪费最大的一种返工 |
| 成本 | Live 模式每次 $0.002（Top 10），一篇简报只调一次 | 可忽略 |
| 行业依据 | Ahrefs 的"搜索意图 3C"第一条就是看首页排名页面的主流内容类型（博客、商品页、分类页、视频） | 是标准做法 |
| 已有经验 | 你在 `claude-blog-kai` 里做过同样的 Step 2a，含计数脚本和测试 | 可复用，风险低 |

## 3. 定下来的方案：不用脚本，只改 SKILL.md

Top 10 最多 10 行，模型数得清。真正的风险不是算错，而是模型"放水"让关键词过关。
所以不写脚本，改为要求把分类表和计数**写进简报**，判定过程人能一眼核对。

规则：

1. **位置**：Step 1 不再让用户填意图；新增 **Step 1.5 SERP 意图闸门**，在 Step 2 之前。
2. **调用**：用 DataForSEO MCP 调一次 `POST /v3/serp/google/organic/live/advanced`
   （`depth: 10`，默认美国 / 英语）。失败重试一次，仍失败就停止并说明原因，不退回 WebSearch 猜。
3. **分类**：每条自然排名结果按 URL 和标题标一个类型：`blog`、`product`、`category`、
   或其他具体类型（`video`、`forum` 等）。不打开页面。
4. **判定**：`blog` 的数量**严格多于**其他任一单一类型才继续；并列也停。
5. **停下时**：列出各类型数量和每类一个示例 URL，让用户三选一：坚持写 / 换关键词重查 / 结束。
6. **留痕**：分类表、计数、结论写进简报的 Search Intent 部分。

## 4. 改动清单（确认后再做）

- `skills/blog-brief/SKILL.md`：Step 1 去掉意图输入；新增 Step 1.5（约 20 行）；Step 2 第 6 条改为引用 1.5 的结论
- `skills/blog-brief/templates/brief-template.md`：Search Intent 部分加分类表和计数
- `docs/FORK-DEVLOG.md`：合并后记一条
- 分支：`claude/brief-skill-step1-optimize-f1ff43` 改名为 `feat/blog-brief-serp-intent-gate`

不加：计数脚本、测试、单独的参考文件。旧项目 Step 2 的其余部分（关键词池、需求分面、
竞品卡片）也不搬，超出本次范围。

## 5. 以后什么情况再加脚本

如果实际用下来发现模型数错或放水，再把计数移到脚本里。先用简单版验证需求。

## 出处

- DataForSEO Google Organic SERP 定价（Live $0.002/次，Standard $0.0006/次）：https://dataforseo.com/pricing/serp/google-organic-serp-api
- DataForSEO Labs Search Intent 只给关键词级意图（informational 等），不分页面类型，所以不适合本需求：https://docs.dataforseo.com/v3/dataforseo_labs/google/search_intent/live/
- Ahrefs 搜索意图 3C：https://ahrefs.com/blog/search-intent/
- 旧实现（参考，未搬脚本）：`/Users/Kai/个人项目/github-skills/claude-blog-kai/skills/blog-brief/`（SKILL.md Step 2a、`scripts/count_serp_types.py`）
