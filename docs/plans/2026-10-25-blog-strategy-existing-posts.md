# 开发文档：blog-strategy 接受现有博客列表，输出一份 CSV 总表

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 方案已和用户逐段确认，等实施 |
| 分支 | feat/blog-strategy-existing-posts，从 `main` 的 bb0ee67 开 |
| 依据 | 瑜东第 01 课：已经运营的网站要结合站内覆盖情况、支柱页和锚文本清单来判断，避免重复建设（p.107）；资料盘点单的「同站博客清单，用于选内链和避免重复」（p.110）。Anthropic 官方 Prompting best practices：结构化的状态信息用 JSON，https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices 。本项目 CLAUDE.md：脚本要有 docstring、命令行接口和 JSON 输出 |
| 来源 | `docs/reviews/2026-10-25-existing-blog-clusters-and-internal-links.md`；2026-10-25 和用户的方案讨论 |

## 1. 目标

已经有几百篇博客的网站跑 `/blog strategy` 时，能把现有博客列表交给它；拿到的规划里，每篇已有文章都归到一个支柱或写明为什么不归，新文章只补已有文章没覆盖的问题，已有和新写的文章在一份 CSV 总表里，可以用 Excel 按支柱筛选。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 拿每篇已有文章的排名词（Search Console 或 DataForSEO Ranked Keywords），按数据归类 | 下一个分支。这一版只按标题归类，策略文档里写明 |
| 帮用户从站点地图提取列表，或抓取每篇网页的内容 | 不做。用户给 CSV |
| 判断哪篇该更新 | 不做。用户 2026-10-25 选「只显示日期不判断」。总表列出更新日期 |
| 合并、301 跳转、删除的方案 | 不做。只标「疑似重复」，交给 `/blog cannibalization` 用数据确认 |
| 已有文章之间加内链的改链清单 | 评估文档里的 `cluster --from site`，以后再定 |
| 把 blog-strategy 拆成步骤文件 | 以后单独做。它现在 385 行，这次加完约 430 行，在 500 行以内 |
| 按标题文字相似度自动分组 | 不做。标题相似不等于话题相同（「linen pants with sneakers」和「linen pants in winter」），分组由 Claude 判断 |
| `blog-cluster` 执行阶段、链接矩阵、质量门的其他改动 | 不做。只改 Strategy Import 一节 |

## 3. 原因

### 3.1 现在的问题

1. `/blog strategy` 的输入只有一个行业名（`argument-hint: "<niche>"`）。Step 1 第 3 个问题只问有没有已有博客，项目里有文件时扫一下（`skills/blog-strategy/SKILL.md` 第 51 行）。从 Step 2 到 Step 8，没有一步规定拿已有文章做什么。
2. Step 4 的集群建设表只列要写的文章，没有「已有」一栏。对一个有 200 多篇博客的站，规划出来的新文章可能和已有文章重复，也可能完全绕开已经写得最多的方向。
3. Step 8 只给了策略文档的格式，没写存到哪里。200 多篇的归类结果只留在对话里，用户没法核对，`/blog cluster --from strategy` 也只能在当前目录里找一个带表格的文件。
4. 把列表贴进对话可以，但 200 多行全靠 Claude 记：会漏行、会数错，漏了也没人发现。

### 3.2 依据

- 瑜东课程讲的是单篇文章，没有讲策略这一层。相关的只有第 01 课：已经运营的网站要结合站内覆盖情况和支柱页判断，避免重复建设（p.107）；同站博客清单用于选内链和避免重复（p.110）。本方案的步骤是我们自己定的，课程没有对应的卡片。
- 编号、检查、统计、生成表格这类每次结果都该一样的事交给脚本，判断留给 Claude。本项目先例：blog-brief 的 `keyword_pool.py`、`brief_state.py`。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 用户的行业名和 Step 1 的回答 | 和现在一样 |
| 用户给的 CSV，三列 `url`、`title`、`lastmod`（`lastmod` 可空，站点地图里的 ISO 日期原样即可） | `init` 读进来、编号。不给就当作没有已有文章 |
| `strategy/[site]-existing-posts.json` | `init` 写、`list` 和 `check` 读。只归脚本管 |
| `strategy/[site]-assignments.jsonl` | Claude 写，一行一篇：已有文章的归类，以及每篇新文章的规划 |

`[site]` 是站点 slug：有域名就用域名去掉 `www.` 和后缀，否则用品牌名；只用小写字母、数字和连字符。

### 4.2 处理步骤

新脚本 `skills/blog-strategy/scripts/existing_posts.py`，标准库实现，三个子命令。

1. Step 1：问完 6 个问题后，跑 `init --site [site]`，有 CSV 时加 `--posts [路径]`。
   - 必须有 `url`、`title` 两列，缺列报错并写明缺哪一列。
   - 网址不是 `http://` 或 `https://` 开头的行跳过；同一网址只留第一行。两种都列进输出的 `skipped`，写明原因。
   - 按网址排序后编号 E1、E2……，写出 `[site]-existing-posts.json`，打印总数、跳过数、没有日期的篇数。
   - 文件已存在时报错，防止覆盖做到一半的归类；要重来加 `--force`。
2. Step 4 开头，有已有文章时：跑 `list --site [site]`，每篇一行「编号、标题、日期」。Claude 按「回答读者什么问题」把标题分成若干组，每组一句话、几篇。这份分组只是草稿，不落盘。
3. Step 4 定支柱：在分组基础上，结合业务、读者、竞品定 3 到 5 个支柱。已有文章多的分组优先接成支柱；不在业务范围的分组不硬接。
4. Step 4 写 `assignments.jsonl`：
   - 每篇已有文章一行：`{"id": "E12", "pillar": "Linen Care", "role": "spoke", "action": "keep"}`。
     - `pillar`：支柱名，或 `none`。
     - `role`：`pillar`（这篇能当总览页）、`spoke`（细分文章），归 `none` 时写 `-`。
     - `action`：`keep`，或 `possible duplicate of E[n]`；归 `none` 时写原因（例如 outside business scope）。
   - 每篇新文章一行，编号 N1、N2……：`{"id": "N3", "pillar": "Linen Care", "role": "spoke", "title": "...", "template": "how-to-guide", "target_keyword": "...", "word_count": "1,500-2,500", "internal_links": "E7, N1"}`。
   - 新文章只写已有文章没覆盖的问题。每个支柱「8 到 12 篇细分文章」改成已有加新写一起算；已有的够多时，新写可以是 0 篇。
   - 某个支柱没有已有文章能当总览页时，新写一篇 `role` 为 `pillar` 的文章。
5. 跑 `check --site [site] --pillars "[支柱 1]" "[支柱 2]" ...`。检查：
   - 每个 E 编号有且只有一行；N 编号不重复。
   - `pillar` 在 `--pillars` 里，或是 `none`（只有 E 行可以是 `none`）。
   - `role` 只能是 `pillar`、`spoke`、`-`；每个支柱正好一个 `pillar`。
   - `possible duplicate of E[n]` 指向存在的、不是自己的编号；`none` 行写了原因。
   - N 行的 `title`、`template`、`target_keyword`、`word_count`、`internal_links` 都填了，`template` 是 12 个模板之一，`internal_links` 里的编号都存在。
   - 有错就打印 `{"errors": [...]}`，每条写明行号、编号和错在哪，退出码 1。Claude 改完再跑。连续两次没过就停下问用户：这是沿用阶段门的项目规则，课程没有。
6. `check` 全过：写出 `strategy/[site]-plan.csv`，并打印每个支柱的已有篇数、新写篇数、疑似重复篇数，以及 `none` 的篇数。
7. Step 8：策略文档存为 `strategy/[site]-strategy.md`。「Content Pillars & Cluster Architecture」一节不再贴表，改成「现有内容盘点」：抄 `check` 的统计，链到 `plan.csv`，说明归类只看标题。

没有 CSV 时也走第 1、4、5、6、7 步，只是没有 E 行。这样有没有已有文章，产出都是同一种 CSV。

### 4.3 输出

`strategy/[site]-plan.csv`，UTF-8 带 BOM（Excel 双击打开不乱码），一行一篇，列如下：

| 列 | E 行（已有） | N 行（新写） |
|---|---|---|
| `id` | E12 | N3 |
| `status` | `existing` | `new` |
| `pillar` | 支柱名或 `none` | 支柱名 |
| `role` | `pillar`、`spoke` 或 `-` | `pillar` 或 `spoke` |
| `title` | CSV 里的标题 | 规划的标题 |
| `url` | CSV 里的网址 | `-` |
| `lastmod` | CSV 里的日期，或 `-` | `-` |
| `template` | `-` | 12 个模板之一 |
| `target_keyword` | `-` | 目标关键词 |
| `word_count` | `-` | 例如 `1,500-2,500` |
| `internal_links` | `-` | 要链到的编号 |
| `action` | `keep`、`possible duplicate of E[n]`，或不归的原因 | `-` |

排序：按 `--pillars` 的顺序分组；组内 `pillar` 行在前，然后已有细分文章，最后新写细分文章；`none` 的行放在表尾。已有文章不知道的格子写 `-`，不编。

`strategy/[site]-strategy.md`：原来的策略文档，加「现有内容盘点」一节。

### 4.4 下游怎么变

`skills/blog-cluster/SKILL.md` 的 Strategy Import 一节（第 209 到 218 行）：

- 第 1 条改成找 `strategy/*-plan.csv`（或用户给的路径），写明列名。
- 第 2 条改成按 `pillar` 列分组；`status` 为 `existing` 的行不写，也不做 SERP 验证，只加进「已写好、可以链过去」的文章列表。
- 其余几条不变。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-strategy/scripts/existing_posts.py` | 新建：`init`、`list`、`check` |
| `skills/blog-strategy/SKILL.md` | 参数说明加 `--posts`；Step 1 第 3 个问题和 `init`；Step 4 分组、定支柱、写 jsonl、跑 `check`，删掉手写的 Cluster Build Plan 表格式；Step 8 存进 `strategy/`，表格一节换成「现有内容盘点」 |
| `skills/blog-cluster/SKILL.md` | Strategy Import 第 1、2 条 |
| `tests/test_existing_posts.py` | 新建 |
| `tests/` 下一个契约测试 | strategy 写的 CSV 列名和 cluster 认的列名一致 |
| `CLAUDE.md` | 脚本说明和目录树 |
| 本文件 | 第 6 节填实际结果 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 只改 SKILL.md 文字，Claude 自己读 CSV、归类、统计 | 200 多行会漏行、数错，漏了没人发现 |
| 工作表用 Markdown，Claude 直接往表里填 | 网页标题常带 `|`，会把格子拆错（阶段门审查时刚遇到过）；脚本要自己解析表格 |
| Claude 直接改 JSON | 手改 200 多条 JSON 容易写坏格式，整个文件读不出来。JSONL 一行一篇，错一行脚本能指出是哪一行 |
| 集群建设表只列支柱页和新写文章，已有文章另列一份清单 | 用户 2026-10-25 要一张表看全 |
| 每个支柱一张表，再加一份全部已有文章的清单 | 已有文章在两处各出现一次。用户 2026-10-25 定为一份策略文档加一张总表 |
| 总表用 Markdown | 200 多行、12 列，在编辑器里不好读，不能筛选排序。用户 2026-10-25 选 CSV |
| 放进 `blog-cluster`，加 `plan --from site` | strategy 管盘点和归类，cluster 管照计划执行。先有盘点，后面才谈得上改内链 |
| 已有行让 Claude 按标题猜一个目标关键词 | 猜的词没有数据撑着，会误导 cluster。用户 2026-10-25 选写 `-` |

## 6. 验证

| 验证项 | 打算怎么验 |
|---|---|
| 先看到失败 | 先写测试，脚本不存在时测试失败 |
| 脚本单元测试 | 缺列；重复网址和坏网址进 `skipped`；拒绝覆盖和 `--force`；`list` 的格式；`check` 每类错误各一个用例；连同标题里的逗号、引号、竖线写进 CSV 后能用 `csv` 模块原样读回；排序和 `status`；没有 CSV 时只有 N 行 |
| 契约测试 | strategy 的 CSV 列名出现在 cluster 的 Strategy Import 里 |
| 仓库检查 | `pytest`、`validate_skills.py`、`consistency_check.py`（看 errors）、`lint_prose.py` |
| 整篇重读 | 改过的每个文件从头读，每句问谁需要、删了坏什么、别处是否已写 |
| 模拟跑 | 子代理只读改后的 SKILL.md，给它一份 30 行的假 CSV，报告每一处不得不猜的地方 |
| 真实跑 | 用户提供一份真实站点地图导出的 CSV，在 playground 跑一次，看归类有没有用、`none` 和疑似重复合不合理、Excel 打开是否正常 |
| 独立审查 | 子代理只拿课程和代码审查 |
| 对照瑜东、对照上游（提交前评估） | 第 01 课 p.107、p.110；上游 `3544423` 的 blog-strategy 和 blog-cluster |

## 7. 提交拆分

```
docs(blog-strategy): add design for planning from an existing post list
feat(blog-strategy): accept an existing post list and write one plan CSV
```

第一个提交只有本文件。第二个提交是脚本、两个 SKILL.md、测试、CLAUDE.md 和本文件第 6 节的结果。
