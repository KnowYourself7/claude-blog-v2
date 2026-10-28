# 写作工作流现状，以及让它更合 SEO 的改法

- 日期：2026-10-27。
- 范围：从 `/blog brief` 到交付的整条流程，按 main 上的现状（9921bd6）。
- 实例：冬季亚麻那次实跑，见 `docs/reviews/2026-10-27-linen-winter-article-review.md`。
- 依据：Google Search Central 的官方文档（2026-10-27 读过，网址在第 4 节），以及 `docs/yudong/` 的课程。
- 只读评估，没有改 skill 文件。

## 1. 现在的工作流

整条流程分三段，用两个命令跑。

| 段 | 命令和步骤 | 做什么 | 产物 |
|---|---|---|---|
| 简报 | `/blog brief` Step 1 | 任务单：读者、品牌、支撑页、定位、交付物 | task-brief.md |
| | Step 2 | 查实时搜索结果，判断这个词该不该写博客 | search-intent.md |
| | Step 3 | 关键词池归成读者需求面 | keyword-research.md、demand-facets.md |
| | Step 4 | 抓排名前 5 的博客，找缺口，写「我们的不同」 | competitor-gaps.md |
| | Step 5 | 选文章模板 | 记在状态文件里 |
| | Step 6 | 证据计划：每个要说的点找来源 | evidence-plan.md |
| | Step 7 | 信息增益：把缺口做成读者能用的工具 | information-gain.md |
| | Step 8 | 大纲两版 | outline.md |
| | Step 9、10 | 定字数和难度，生成简报 | brief.md |
| | Step 11 | A→B 阶段门：方向和证据清楚才往下走 | 无 |
| 写作 | `/blog write` Phase 0 到 6 | 读简报，再选一次模板、再查一次资料、再出一次大纲，然后写正文、做图表、自查 | S.md |
| 交付 | Phase 6.5 交付合同 | 渲染 HTML 和 PDF；审稿 agent 打 100 分制，90 分以上、零个 P0 才放行；5 道闸门查格式、截图、链接；最多返工 3 轮 | S.html、S.pdf、review.md、preflight-report.json |

SEO 相关的命令还有几个，但都不在这条流程里，要手动另跑：`/blog seo-check`、`/blog cannibalization`、`/blog schema`、`/blog geo`、`/blog google`、`/blog decay`。

## 2. SEO 已经做了的

| 环节 | 做法 |
|---|---|
| 搜索意图 | Step 2 用实时搜索结果判断这个词该不该写成博客 |
| 关键词 | Step 3 用 DataForSEO 关键词池，按读者需求归组，不按词堆 |
| 竞争 | Step 4 抓竞品全文找缺口，Step 7 做成信息增益 |
| 页面元素 | 写作阶段出标题、meta 描述、H2 层级、FAQ、图表 |
| 审稿 | 审稿 agent 的 SEO 一项占 25 分，AI 引用准备占 15 分 |
| 技术 | 渲染器生成 JSON-LD（给搜索引擎看的结构化数据）、canonical、OG 标签；Gate 5 查每个链接能不能打开 |

## 3. 改法，按收益排序

每一条都来自亚麻那次的实际问题。

| # | 改什么 | 亚麻那次的问题 | 依据 | 改在哪里 |
|---|---|---|---|---|
| 1 | 开工前查站内撞题，定「新建还是更新旧文」 | 站内已有同题旧文，新文会和它抢同一个搜索词 | 瑜东第 01 课 p.107（站内已有文章是否覆盖过）；第 02 课 p.113（新建还是更新旧文）。Google 没有「关键词蚕食」这个官方说法 | brief Step 1 和任务单模板。现有的 `/blog cannibalization` 只分析本地文章文件，不能直接读网址清单 |
| 2 | 建内链体系：链出到 pillar、同站相关文章、集合页；也要列出哪些旧页面要加链接指回新文 | 只链了 1 个集合页，没链 pillar；指回新文的链接（Link FROM）写的是 missing | Google：每个重要页面至少要有一个站内页面链向它；锚文本要能说明目标页；链接数量没有理想值 | brief Step 1 收同站页面清单，Step 8 安排位置。已有计划 `docs/plans/2026-10-24-blog-brief-internal-link-pages.md`，但它把 Link FROM 列为不做，需要重新考虑 |
| 3 | 标题规则改成「重要词放前面」，不按 40-60 字符扣分 | 为了缩到 60 字符以内，删掉了区分词 "Men's" | Google：标题没有长度上限，搜索结果按设备宽度截断；标题要描述清楚、简洁、不堆词 | 上游评分规则 `skills/blog/references/quality-scoring.md` 第 137 行，把超长当成 High 级问题 |
| 4 | 向品牌要一手资料，配实拍图或产品图 | 一手资料一栏是 none supplied；首图是文字卡 | Google 有用内容自查题：是否提供原创的信息或分析；是否体现亲自用过产品得来的经验。Google 图片指南：高质量照片，放在相关文字附近 | brief Step 1 或 Step 7 主动询问；写作阶段配图 |
| 5 | 作者是编辑团队时，schema 用 Organization | 作者被标成 Person，审稿三次都扣分 | Google Article 结构化数据：人用 Person，组织用 Organization | `scripts/blog_render.py` 第 497 行把类型写死成 Person |
| 6 | 补语义覆盖检查（瑜东 A·09 语义基准） | 没有词表可对，写完不知道漏了哪些相关概念 | 瑜东第 05 课 | brief 新加一步，写作阶段对照。量大，排后面 |
| 7 | 发布后复测排名和点击 | 流程到交付就结束了 | 瑜东第 10、11 课 | 已有 `/blog google`、`/blog decay`，先手动用，暂时不接进流程 |

还有一项不改代码：本机装上 patchright 要的浏览器，让 Gate 2、3、5 能跑。不装的话，链接检查每次都会跳过。

### 不建议做的

- 给字数定目标。Google 把「按特定字数写」列为以搜索引擎为先的信号，并说明自己没有偏好的字数。现在的 Step 9 只给估计值，方向对。
- 往标题、锚文本里硬塞关键词。上面两份 Google 文档都明确反对。

## 4. Google 官方文档

| 文档 | 网址 | 用在第几条 |
|---|---|---|
| 标题链接 | https://developers.google.com/search/docs/appearance/title-link | 3 |
| 有用的内容 | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | 4、不建议做的 |
| 链接最佳做法 | https://developers.google.com/search/docs/crawling-indexing/links-crawlable | 2 |
| Article 结构化数据 | https://developers.google.com/search/docs/appearance/structured-data/article | 5 |
| Google 图片 | https://developers.google.com/search/docs/appearance/google-images | 4 |
