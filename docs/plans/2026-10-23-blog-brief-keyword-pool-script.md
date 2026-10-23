# 开发文档：blog-brief Step 3 的机械操作改成脚本

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已确认，实现中（用户 2026-10-23 定：脚本直接调接口；就在当前分支继续） |
| 分支 | feat/blog-brief-a06-gap-list（接在 b882c7d 之后） |
| 依据 | essentials `skill-dev-rules.md` 第 8 条「机械活用脚本，判断活用模型」；`docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节末尾「a05 里去重、分组、排序适合改成脚本」；瑜东第 00 课「工具提供数据与执行，模型负责理解与判断」（p.150） |
| 改动范围 | 新建 `skills/blog-brief/scripts/keyword_pool.py` 和 `tests/test_keyword_pool.py`；改 `references/step-3-demand-facets.md`、`templates/keyword-research.md`、`templates/demand-facets.md`、`SKILL.md` 步骤表一行、`CLAUDE.md` 目录树 |

## 1. 为什么改

Step 3 有 17 条，其中 7 条是每次结果都应该一样的机械操作：去重、按 `core_keyword` 分组、按搜索量排序、选代表词、数证据类型、按证据和搜索量排序、取前 9 个。模型手工做这些既费字又容易错。

真实跑的证据（2026-10-22 linen pants）：两次 Keyword Suggestions 返回 65 万和 105 万字符，模型靠 Claude Code 把超长返回落盘才解析得了；445 个词分 280 组，全靠模型在上下文里做。这一步花了 0.09 美元接口费，上下文消耗远大于此。

## 2. 改完的样子

模型只做判断：种子怎么缩、剔除词归哪一类、证据合并成面、关键词行挂到哪个面、业务边界、保留理由。脚本做剩下的。

| 操作 | 现在 | 改后 |
|---|---|---|
| 调 Keyword Suggestions、Overview、Related Keywords | 模型通过 MCP 调，返回进上下文 | 见第 3.1 节 |
| 去重、分组、排序、选主关键词、峰值月 | 模型手工 | 脚本 |
| Keyword Pool、Other Sources、Not in Overview 三张表 | 模型手写 | 脚本生成 |
| 剔除跑题词 | 模型判断 | 模型判断，只写行号和类别，脚本据此更新表 |
| 面的证据类型计数、排序、取前 9 | 模型手工 | 脚本，输入是模型写的面清单 |
| Data Scope 的调用记录和费用 | 模型从返回里抄 | 脚本写 |

Step 3 预计从 17 条降到 10 条左右。

## 3. 两件要用户定的事

### 3.1 脚本怎么拿到接口数据

| 方案 | 做法 | 好处 | 坏处 |
|---|---|---|---|
| A 脚本直接调 DataForSEO 接口（推荐） | 脚本用 `urllib` 调 REST 接口，凭据从环境变量 `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` 读，和 MCP 用同一对 | 上百万字符的返回完全不进模型上下文；结果可重复；`blog-google/scripts/` 已有同样做法的先例；不加第三方依赖 | 运行环境要有这两个环境变量（`docs/MCP-INTEGRATION.md` 已建议放 `~/.config/dataforseo.env`）；Step 3 的规则从「通过 MCP 调」改成「跑脚本」 |
| B 脚本解析模型存下的 MCP 返回 | 模型仍通过 MCP 调，把返回存成文件，脚本读文件 | 不碰凭据 | 返回不超上限时不会自动落盘，模型要自己把几十万字符写进文件，上下文照样被吃掉；两条路径要写两套说明 |

### 3.2 什么时候做

| 方案 | 做法 |
|---|---|
| A 先收尾当前分支（推荐） | 当前分支已有 10 次提交，先真实跑、开 PR、合并；脚本从 main 开新分支。脚本有测试，混进当前 PR 会让它更难审 |
| B 叠在当前分支上 | 新分支从 feat/blog-brief-a06-gap-list 开出，等它合并后再 rebase |
| C 就在当前分支上继续 | 第 11 次提交起加脚本 |

## 4. 脚本的接口（按 3.1 的 A 写，选 B 再改）

`python3 skills/blog-brief/scripts/keyword_pool.py <子命令> [参数]`，stdlib only，输出 JSON 到标准输出，同时写文件。

| 子命令 | 输入 | 做什么 | 输出 |
|---|---|---|---|
| `pool` | `--focus`、`--seed`（1 到 3 个）、`--location`、`--language`、`--evidence FILE`（模型写的小 JSON：PAA 问题、相关搜索） | 每个种子调一次 Suggestions（limit 300）；去重、分组、排序；不在池里的相关搜索调一次 Overview | `briefs/[slug]-keyword-pool.json`（全部行和字段）和 `briefs/[slug]-keyword-pool.md`（Keyword Pool、Other Sources、Not in Overview 三张表加 Data Scope 调用行） |
| `remove` | `--pool FILE`、`--removed FILE`（模型写的 JSON：行号、类别、理由） | 把剔除的行移到 Removed Keywords | 更新两个文件 |
| `related` | `--pool FILE`、`--focus` | 调一次 Related Keywords（depth 2），并入池 | 更新两个文件 |
| `rank-facets` | `--facets FILE`（模型写的 JSON：每个面的问题、证据编号、挂的行号、业务判断）、`--pool FILE` | 代表词、证据类型计数、排序、取前 9，少于 5 个返回提示 | `briefs/[slug]-demand-facets.md` 的 Kept Facets 和 Other Facets 表 |

模型写的三个小 JSON 都只有几十行，上下文代价可忽略。

## 5. 产物文件的变化

- `keyword-research.md` 拆成两个文件：模型写的 Question Evidence、Seeds、Removed Keywords 留在 `keyword-research.md`；脚本写的三张表放 `keyword-pool.md`。两边互相链接。
- `demand-facets.md` 的表由脚本写，模型负责表外的说明和理由句。

## 6. 测试

- `tests/test_keyword_pool.py`：用录下来的两份真实返回（linen pants 的 Suggestions 和 Overview，脱敏后存进 `tests/fixtures/`）测分组、排序、平局、空值；接口调用用 monkeypatch 替换，不联网。
- 真实跑：`can you wear linen in winter`，看池的行数和上次模型手工的结果是否一致、上下文消耗降多少。

## 7. 实现记录（2026-10-23）

- 按 TDD 做：先写 15 条测试看它们失败（模块不存在），再写脚本让它们通过；CLI 的端到端测试是代码之后写的，只算覆盖。
- 夹具 `tests/fixtures/keyword_pool_suggestions.json` 是按官方文档的字段结构手写的样例，不是录下的真实返回；真实返回的字段名在实现前用 WebFetch 从 docs.dataforseo.com 核过（Suggestions、Overview、Related Keywords 三页）。
- 和第 4 节的差别：Overview 在剔除之前调（`pool` 一次做完），因为脚本只跑一次；相关搜索最多几条，多付的钱可忽略。凭据同时接受 `DATAFORSEO_LOGIN` 和仓库文档里的 `DATAFORSEO_USERNAME`。代表词也可以来自 Other Sources 里有搜索量的相关搜索，和原规则一致。
- Step 3 从 17 条变 12 条；三张池表和两张面表由脚本写，模型只写三个小 JSON（证据、剔除、面）。

## 8. 不做

- Step 2 的 SERP 调用仍走 MCP，返回小，且 Step 3 复用它。
- 不改剔除、归面、业务边界这些判断规则。
- 不接 Ahrefs，不做站内覆盖。

## 出处

- essentials：`/Users/Kai/个人项目/essentials/skill-dev-rules.md` 第 8 条
- 真实跑记录：`claude-seo-playground/briefs/what-to-wear-with-linen-pants-a06/what-to-wear-with-linen-pants-a06-test-notes.md` 第 2 节调用 4、5
- DataForSEO 凭据配置：`docs/MCP-INTEGRATION.md`
