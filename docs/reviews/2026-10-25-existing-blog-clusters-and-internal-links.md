# 评估：输入现有博客列表，给出集群划分和内链方案

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 问题 | 已有网站和博客时，能不能输入一份从站点地图扒下来的博客列表，得到集群划分和内链调整方案？值不值得做，现有 skill 能不能凑出来，要做放在哪个 skill |
| 读过的文件 | `skills/blog-cluster/SKILL.md` 和它的 3 份参考、`skills/blog-audit/SKILL.md`、`skills/blog-cannibalization/SKILL.md`、`skills/blog-google/SKILL.md`、`skills/blog/references/internal-linking.md`、docs/plans 下的 2026-10-24-blog-brief-internal-link-pages.md（未提交）、瑜东课程第 01、05、07、09、11 课 |

## 1. 结论

1. 值得做，但不急。它解决的是真实问题：老站的文章越写越多，彼此不链接，或者几篇抢同一个词。但它不在瑜东课程里（课程讲的是一篇文章怎么做），也不在路线二上。建议路线二最后一步 `feat/blog-write-use-brief` 做完后再开。
2. 现有 skill 能凑出大约一半：拿到每篇文章排什么词、找出抢词的文章、找出没人链接的孤立页，都有现成的。缺的是中间那一段：按共享的词把文章分成集群，选出每个集群的支柱页，再对照现有链接列出「哪篇加一条链接到哪篇」。
3. 要做的话，放进 `blog-cluster`，加一个子命令（暂名 `/blog cluster plan --from site <列表>`）。它已经有集群结构、链接矩阵、关系图和「已发布文章的改链清单」这几样，只差把输入从种子词换成现有文章。不建议新建 skill，也不建议塞进 `blog-audit`。
4. 动手前先手工凑一次：拿 Coofandy 的博客列表，用现有 skill 一步步做，看产出的方案有没有用、哪一步最费事，再决定写不写成功能。

## 2. 现有 skill 能做到哪一步

| 需要的一步 | 现有 skill | 能不能直接用 |
|---|---|---|
| 拿到博客列表 | 用户从站点地图扒 | 能。`blog-cannibalization` API 模式第 1 步就是「从用户或 sitemap 收集已发布网址」 |
| 知道每篇文章讲什么、排什么词 | `/blog google gsc`：Search Console 按「查询词 + 页面」导出，默认 28 天、1000 行，免费 | 能，前提是用户有这个站的 Search Console 权限 |
| 同上（没有 Search Console 时） | `/blog cannibalization --api`：DataForSEO Ranked Keywords，每个网址一次调用，付费 | 能，但只在 cannibalization 的流程里用，结果不落盘给别的 skill |
| 找出几篇抢同一个词 | `/blog cannibalization` | 能，只出报告，给合并或区分的建议 |
| 按共享的词把文章分成集群，选支柱页 | 无 | 不能。`blog-cluster` 的分组只接受种子词扩出来的关键词，不接受现有文章 |
| 画出现有的内链关系，找孤立页 | `/blog audit` 第 4 步：建链接图，找零入链的孤立页和零出链的死胡同，每个孤立页推荐 2 到 3 篇该链向它的文章 | 部分能。它读的是本地文章文件，不是网址列表；推荐只看话题相近，不看集群 |
| 列出「哪篇加一条链接到哪篇」，不直接改线上文章 | `blog-cluster` 执行阶段的 `cluster-link-patches.md`：文件、锚文本、要改的那句话、目标文件 | 格式现成，但只用在新写的集群里 |
| 改链的节奏 | `internal-linking.md`：老文章加链接每周最多 3 到 5 篇，不要一次全改 | 能，直接引用 |

所以缺口很明确：「按词分集群、选支柱页」和「对照现有链接出改链清单」这两段没有，其余都有。

## 3. 两个数据源问题（和 blog-cluster 现有的问题相同）

`blog-cluster` 现在扩词和分组都只用 WebSearch，这对新功能也是坑：

- WebSearch 没有搜索量、难度、意图，也不是 Google 按市场和语言给出的前 10 条自然结果。拿它数「两个词的前 10 条结果重合几条」，数出来的不可靠。
- 现有文章有更好的依据：这个网址实际在 Google 排了哪些词。两篇文章共享的排名词多，就该在同一个集群；共享同一个主词，就是在抢排名。这些数据来自 Search Console（免费、最准，只有自己的站有）或 DataForSEO Ranked Keywords（付费，不需要站点权限）。
- DataForSEO Labs 多数接口按「每次 0.01 美元加每条结果 0.0001 美元」计费。Ranked Keywords 的单价没查到明确页面，100 篇文章大约 1 到 2 美元，是推算，要以账号后台为准。

`blog-cluster` 扩词改用 DataForSEO，是另一件事，单独一个分支。

## 4. 放在哪个 skill

| 方案 | 好处 | 坏处 |
|---|---|---|
| `blog-cluster` 加 `plan --from site`（推荐） | 集群结构、`cluster-plan.json`、关系图、链接矩阵、改链清单格式都现成；已经有 `plan --from strategy` 这种「换一种输入」的先例 | SKILL.md 已有 394 行，接近 500 行上限，要先像 blog-brief 一样拆步骤文件 |
| `blog-audit` 加一步 | 它已经建链接图、找孤立页 | 它是全站体检，读本地文件；加上网址列表、拉排名词、分集群，职责会变成两件事 |
| 新建一个 skill | 职责单一 | 「如无必要，勿增实体」；它要的东西八成在 `blog-cluster` 里，会重复一份 |

## 5. 和别的计划的关系

- docs/plans 下的 2026-10-24-blog-brief-internal-link-pages.md（还没做）让用户在写单篇简报时给一份同站页面清单，大纲按清单安排内链。它管「新文章链向谁」，本功能管「老文章之间怎么链」。两者可以共用同一份清单格式（URL、讲什么、类型）。
- 瑜东第 01 课说，已经运营的网站要结合站内覆盖情况、支柱页和锚文本清单来判断，避免重复建设（p.107）；第 07 课说内链放在读者确实需要继续了解的位置，条数没有通用标准（p.132-133）。这两条适用于本功能，但课程没有讲老站整体改内链的做法，本功能的步骤要自己定，并在开发文档里写明。
- Google 的链接规范：每个重要页面至少要有站内另一个页面链向它；锚文本要能说明目标页讲什么，不用「点这里」；链接放在对读者有帮助的地方。

## 6. 动手前要用户回答的问题

1. 网站有 Search Console 权限吗？有就用免费的查询词数据，没有才用 DataForSEO。
2. 博客大约多少篇？几十篇可以一次做完；几百篇要分批，也要先抽样验证。
3. 产出只要「改链清单」交给人去改，还是要直接改本地的文章文件？建议只出清单，因为线上文章由 CMS 管，本地未必有源文件。

## 出处

- Google Search Central, Link best practices for Google: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- DataForSEO 帮助中心，Labs 接口计费说明: https://dataforseo.com/help-center/how-to-run-serp-analysis-for-seo-with-dataforseo-labs-api
- 同类做法参考（用 Claude Code 读站点地图、分集群、找孤立页）: https://www.tripledart.com/blog/internal-linking-using-claude-code
