# 开发文档：blog-strategy 接受现有博客列表，输出一份 CSV 总表

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 已实施，等用户审核后合并 |
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
| `blog-cluster` 链接矩阵、质量门、执行流程的其他改动 | 不做。只改读入 CSV 和跳过已有文章所需的几处，见 4.4 |

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
   - 网址不是 `http://` 或 `https://` 开头的行跳过；标题为空的行跳过（归类只看标题，没有标题没法归）；同一网址只留第一行。三种都列进输出的 `skipped`，写明原因和 CSV 里的行号。标题为空这条是实施时加的。
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
- 第 2 条改成：一个支柱就是一份集群计划（`cluster-plan.json` 只能有一个支柱），CSV 里有多个支柱时先问用户规划哪个；`role` 为 `pillar` 的行是支柱页；`status` 为 `existing` 的行不写，也不验证关键词，只加进「已写好、可以链过去」的文章列表。原来「每个支柱一张表」时也是一次只能规划一个支柱，只是没写明；这条是实施时补的。
- 自检时发现：`cluster-plan.json` 原来没有字段表示「已写好」，支柱页是已有文章时，执行阶段可能把它重写。所以 schema 下面补一句：来自已有行的支柱或文章带 `"status": "existing"` 和 `url`；执行阶段 Step 2 开头补一句：跳过这些文章，把它们连同网址加进集群上下文里「已写好」的列表。
- Commands 表和 Cross-references 表里还写着「读 Cluster Build Plan 表格」的两处，改成读 plan CSV。
- 其余不变。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-strategy/scripts/existing_posts.py` | 新建：`init`、`list`、`check` |
| `skills/blog-strategy/SKILL.md` | 参数说明加 `--posts`；Step 1 第 3 个问题和 `init`；Step 4 分组、定支柱、写 jsonl、跑 `check`，删掉手写的 Cluster Build Plan 表格式；Step 8 存进 `strategy/`，表格一节换成「现有内容盘点」 |
| `skills/blog-cluster/SKILL.md` | Strategy Import 第 1、2 条；Commands 表和 Cross-references 表各一处；schema 下一句；执行阶段 Step 2 开头一句 |
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

### 6.1 结果

| 验证项 | 结果 |
|---|---|
| 先看到失败 | 先写 `tests/test_existing_posts.py`，脚本不存在时收集就报错。写完脚本 28 项通过，只剩契约测试失败，改完 cluster 的 Strategy Import 后 29 项全过 |
| 脚本单元测试 | 自检后共 40 个用例（18 个测试函数，其中两个参数化，分别是 18 个和 6 个用例；自检前是 29 个，之前写成「参数化逐个算是 46 个」，是数错了）：空行之后的行号、非 UTF-8 的报错、看起来填了其实不对的值（null、数组、小写编号、没有编号的链接、链到自己、`-` 当原因）、支柱名前后空格、失败时删掉旧总表、cluster 跳过已有文章；编号和 `skipped` 的三种原因；Excel 存的带 BOM、列名大写的 CSV；缺列；拒绝覆盖和 `--force`；坏的站点 slug；`list` 的格式；总表的顺序、`status`、BOM、`-`，以及标题里的逗号、引号、竖线写进 CSV 后原样读回；没有 CSV 时只有 N 行；`check` 18 类错误各一个用例，出错时不生成总表；不是 JSON 的行报出行号；模板名来自 `skills/blog/templates/` |
| 契约测试 | `test_blog_cluster_reads_the_plan_csv_columns`：总表的 12 个列名都出现在 cluster 的 Strategy Import 一节里 |
| 仓库检查 | 自检修改后 `pytest tests/` 1579 通过、56 跳过（第一次提交时 1568 通过）。跳过的比上一个分支多 50 个，全是渲染测试，原因是本机没装匹配的 Chromium，和本分支无关（这些测试不碰 strategy 和 cluster）。改模拟跑反馈后复跑相关 79 项全过。`validate_skills.py` 通过；`consistency_check.py` errors 为空；`lint_prose.py` 本分支文件 0 处 |
| 整篇重读 | strategy：删掉 Plan Files 第 2 条「在 Step 4 写判断、跑 check」，和 Step 4 的 Assignments 一节重复；盘点一节「sorted by title」用词不对，改成 assigned。脚本：读 lastmod 那行和写 CSV 的临时缓冲改成直白写法 |
| 模拟跑（子代理，Haiku，只读 SKILL.md，在 scratchpad 真跑脚本） | 30 行假列表（亚麻男装站，放了重复网址、相对路径、空标题、女装、床品、促销页）：`init` 收 27 篇、跳过 3 行；子代理定 3 个支柱，新写 3 篇，`check` 第一次就通过；3 篇归 `none`（促销、床品、女装）。它提 7 处疑问，改了 4 处：「8 到 12 篇」和「够了就不新写」像冲突，改成「是目标不是配额」；写明 `strategy/` 在项目根目录；写明 E 编号按网址排序；跳过原因写出重复时保留哪一行，相对路径的原因改成「不是以 http:// 或 https:// 开头」。没改：分组本来就不落盘；文档语言跟模板走英文；`check` 的报错文字由单元测试覆盖 |
| 对照开发文档自检（子代理，独立，只给开发文档和代码） | 第 4 节各条和第 2 节的边界都核过。挑出 2 处必须改、3 组建议改、5 处可不改，核实后全部属实。改了：CSV 里有空行时跳过行的行号错位，改用 `reader.line_num`（必须改）；`cluster-plan.json` 没有字段表示已写好，支柱页是已有文章时执行阶段可能重写，补 schema 一句和执行阶段一句（必须改）；cluster 另两处还写读表格；`check` 放过 null、数组、小写编号、没有编号的链接、链到自己、`-` 当原因；测试数写错。可不改里改了三处便宜的：非 UTF-8 时给看得懂的报错、支柱名去前后空格、`check` 失败时删掉旧总表。没改：网址去尾斜杠和 http/https 当同一篇、`.co.uk` 这类域名的 slug，规则见仁见智，等真实跑遇到再定 |
| 真实跑 | 没做。要用户提供一份真实站点地图导出的 CSV |
| 对照瑜东（提交前评估） | 见 6.2 |
| 对照上游原版（提交前评估） | 见 6.3 |

### 6.2 对照瑜东

| 课程要求 | 现在 | 结论 |
|---|---|---|
| 已经运营的网站要结合站内覆盖情况、支柱页判断，避免重复建设（第 01 课 p.107） | 先看已有文章怎么分组再定支柱；能当总览页的已有文章标 `pillar`；新文章只补没覆盖的问题 | 符合 |
| 同站博客清单用于选内链和避免重复（p.110） | 新文章的 `internal_links` 可以写已有文章编号；cluster 把已有文章当链接目标；两篇回答同一问题标疑似重复 | 符合 |
| 锚文本清单（p.107） | 不做 | 不符合。CSV 里没有锚文本，以后接排名数据时再定 |

课程没有策略这一层的卡片，下面这些是我们自己定的：CSV 三列的格式、E 和 N 编号、`keep` 和 `possible duplicate` 两种动作、`none` 要写原因、连续两次 `check` 没过就停（沿用阶段门的项目规则）。

### 6.3 对照上游原版

上游 `3544423` 的 blog-strategy 和 blog-cluster，fork 之后到 `main` 一行没改过。原版 strategy 只收行业名，Step 1 问一句有没有已有博客，之后没有一步用它；集群建设表手写在对话里，不落盘。

| | 内容 |
|---|---|
| 增益 | 有几百篇博客的站，规划会接住已有文章，不再从零规划；每篇已有文章都有归属或不归的原因，漏行由脚本挡住；策略文档和总表落盘到 `strategy/`，总表可以在 Excel 里按支柱筛选；cluster 不会重写已有文章，还能链过去 |
| 代价 | strategy 多 47 行（385 到 432）；每次多跑 2 到 4 次脚本；200 多篇时，Claude 要写 200 多行 JSONL，比原来手写一张表多花 token；不给 CSV 的老用法也要写 JSONL、跑 `check`，比原来多一步 |
| 证据 | 单元测试和一次模拟跑。归类只看标题，在真实站点上有没有用未验证 |

## 7. 提交拆分

```
docs(blog-strategy): add design for planning from an existing post list
feat(blog-strategy): accept an existing post list and write one plan CSV
```

第一个提交只有本文件。第二个提交是脚本、两个 SKILL.md、测试、CLAUDE.md 和本文件第 6 节的结果。
