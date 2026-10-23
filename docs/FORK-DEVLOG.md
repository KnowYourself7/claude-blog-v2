# 二次开发日志

记录本 fork 相对上游 [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) 的每次改动。
`CHANGELOG.md` 是上游写给使用者的版本说明，这里只记自己的开发经过。

## 填写规则

- 一行一条，新条目加在表格最上面。
- 分支类型用提交规范里的前缀：feat、fix、docs、chore、refactor、test。
- 单元格里不能写竖线；多个步骤用 `<br>` 换行。
- 分支名不加反引号：`scripts/consistency_check.py` 会把反引号里以 docs/ 开头的文字当成文件路径检查。
- 不用破折号（U+2014、U+2013，中文破折号也算），`scripts/lint_prose.py` 会报错。

空白行模板（复制到表头下面）：

```markdown
| 003 | YYYY-MM-DD | 修改事项 | type/short-name | type | #N | 遇到的问题 | 改完好在哪 | 1. 第一步<br>2. 第二步 | 跑了什么命令，结果 |
```

## 日志

| 编号 | 日期 | 修改事项 | 分支名 | 分支类型 | PR | 开发原因 | 带来的提升 | 开发步骤 | 验证 |
|------|------|----------|--------|----------|----|----------|------------|----------|------|
| 010 | 2026-10-23 | blog-brief 简报模板 H2 数量对齐 Step 2 的 9 个面上限 | fix/blog-brief-h2-facet-count | fix | #12 | Step 2 最多保留 9 个需求面，Step 5 要求每个保留面至少占一个 H2，可 skills/blog-brief/templates/brief-template.md 写死 6-8 个；008 那次真实跑已经分出 9 个面，两条规则不可能同时满足，模型只能违反其中一条，同一选题重复跑会产出不一致的大纲；6-8 是 005 从旧模板搬过来时带进来的通用值，blog-outline 里有一份一模一样的复制品，它没有需求面概念，说明这个数字不是为 blog-brief 定的 | 改成 8-10，让段落预算服从读者需求，不再砍掉花钱调 DataForSEO 换来的真实切面；方向与 tests/test_release_safeguards.py 既有决议一致，那个文件专门在防止项目重新出现写死的数量配额；blog-brief 内已无 6-8 残留，blog-outline 的 6-8 保持不变 | 1. 用 DEVLOG 008 的真实跑记录确认冲突已经发生<br>2. 查 consistency_check、lint_prose、validate_skills 和 tests，确认没有断言盯住这两个数字<br>3. 在收紧上游和放开下游之间选放开下游，理由是收紧等于加强硬配额<br>4. 改 brief-template.md 两处，同步加本行日志 | lint_prose、validate_skills、consistency_check 通过，240 处引用已验证；pytest 交 CI 分层跑，本地缺 Python 3.14 与 uv |
| 009 | 2026-10-22 | blog-brief 每一步拆成单独文件 | refactor/blog-brief-step-files | refactor | #10 | 要按瑜东阶段 A 一步一步重做 blog-brief，可所有步骤都在一个 261 行的 SKILL.md 里；每步都会变长，会超过 500 行上限，也做不到一个分支只换一步 | SKILL.md 降到 68 行，只留共享规则、步骤顺序表和 Step 6；Step 1 到 Step 5 原样搬进 references 文件夹下 7 个文件，文件名用瑜东步骤号；以后每个分支只换一个文件 | 1. 对比瑜东原型的结构，定下"拆成文件，不拆成 skill"<br>2. 查 Agent Skills 规范和 Claude Code 文档：目录用 references，路径变量只在 SKILL.md 里替换<br>3. 写开发文档和后续 8 个分支的路线图<br>4. 用脚本原样搬移，步骤文件改用相对路径<br>5. 同步改测试路径、CLAUDE.md 目录树和三个模板注释 | 逐行 diff 只差路径前缀；pytest 1502 通过 6 跳过；validate_skills、lint_prose、consistency_check 通过；在 playground 用 "2k dispensing problems" 真实跑完整 brief，按顺序读步骤文件，产物结构和旧产物一致，花费 0.057 美元 |
| 008 | 2026-10-22 | blog-brief Step 2 一步完成关键词到需求面 | feat/blog-brief-step2-demand-facets | feat | #9 | 原来的 Step 2 只产出一张不做取舍的词表（亚麻裤 330 行），后面没有哪一步把它变成文章结构；拆成单独 Step 2.2 的尝试分出 62 个面，已放弃 | 按瑜东 A·05 一步完成：先收集五类问题证据，再缩种子扩词、按读者任务筛选，然后从问题证据列需求面并挂上关键词；最多保留 9 个面，少于 5 个补一轮 Related Keywords，少于 3 个停下问用户；Step 5 让每个保留的面至少有一个 H2 | 1. 对照瑜东 a05 阶段文件和实跑日志写开发文档<br>2. 删除被取代的三份拆步方案<br>3. 改 Step 2 和关键词模板，新增需求面模板<br>4. 改 Step 5 和简报模板<br>5. 用两个焦点词真实跑 | pytest 1502 通过 6 跳过；validate_skills、lint_prose、consistency_check、validate_public_release 通过；"what to wear with linen pants" 分出 9 个面，花费 0.094 美元；"2k dispensing problems" 关键词库没有数据，按规则停下，花费 0.044 美元 |
| 007 | 2026-10-22 | blog-brief Step 2 改用 DataForSEO 做关键词调研 | feat/blog-brief-keyword-research | feat | #7 | WebSearch 拿不到搜索量、KD 和意图，次关键词全靠猜；第一版方案一个分支改了太多处、文字啰嗦，整体放弃后重做 | Step 2 用 Keyword Suggestions、Related Keywords 和 Autocomplete 扩词，PAA 和相关搜索沿用 Step 1.5 的 SERP；同一搜索的不同写法按 core_keyword 合并，只剔除 4 类跑题词并写理由；结果存进新的关键词调研模板 | 1. 两次真实数据测试后修订设计<br>2. 改 Step 2，新增关键词调研模板<br>3. Step 1.5 的 SERP 调用加 noAiMode<br>4. 按 simple-english 精简 Step 2 文字<br>5. 用 "matching outfits for couples" 真实跑 3 次 | pytest 1502 通过 6 跳过；validate_skills、lint_prose、consistency_check、validate_public_release 通过；第 3 次真实测试之后又改了 4 处规则，没有再用真实数据重跑 |
| 006 | 2026-10-17 | blog-brief 加 SERP 意图闸门 | feat/blog-brief-serp-intent-gate | feat | #5 | 意图靠用户填或模型猜，关键词首页全是商品页时照样写完整篇简报 | 写简报前先用 DataForSEO Live SERP 看 Top 10，博客页严格最多才继续，否则停下让用户选：坚持写、换词、结束；判定表写进简报便于核对 | 1. 判断必要性并查定价和 Ahrefs 搜索意图 3C<br>2. 方案从脚本版简化为只改 SKILL.md<br>3. 加 Step 1.5，Step 1 去掉意图输入<br>4. 简报模板 Search Intent 加分类表和计数<br>5. 按 writing-skills 精简 Step 1.5（263 词降到 142 词），用子代理跑 3 个模拟 SERP 验证判定 | pytest 1502 通过 6 跳过；validate_skills、lint_prose、consistency_check 通过；子代理 3 个场景全部判对 |
| 005 | 2026-10-17 | 简报模板移出 blog-brief 的 SKILL.md | refactor/blog-brief-template | refactor | 无（本地合并，随 #5 推送） | SKILL.md 已 290 行，后续加功能容易逼近 500 行上限 | SKILL.md 降到 142 行，模板按需读取，后续有约 350 行余量 | 1. 查官方 Skill 最佳实践<br>2. 模板抽到 templates/brief-template.md<br>3. SKILL.md 留引用和填写规则 | pytest 1531 通过；validate_skills、lint_prose、consistency_check 通过 |
| 004 | 2026-10-17 | CI 分层：PR 只跑快速检查，main 跑全量 | chore/tier-ci-pr-vs-main | chore | #4 | 每个 PR 都跑 31 个任务，包括 4 个 Python 版本、3 个系统的锁文件安装和 Windows 安装器，机器总用时约 33 分钟 | PR 上只剩 7 个任务，机器用时约 7 分钟；推到 main 或手动触发仍跑全量。等待时间仍约 6 分钟，瓶颈是 test (3.14) 本身 | 1. 查 GitHub 官方文档：任务级 if 跳过时算成功；工作流级 paths 过滤会让检查卡在 Pending<br>2. 量上次 PR 各任务耗时<br>3. 加 workflow_dispatch；test 矩阵用 fromJSON 按事件切换；4 个重任务加 if<br>4. 更新并补充 ci.yml 结构测试 | pytest 1502 通过 6 跳过；lint_prose、consistency_check、actionlint 通过 |
| 003 | 2026-10-17 | 删除上游作者私自加入的无关文件 | chore/remove-unrelated-files | chore | #3 | 仓库里混着上游作者的私人产物：审计自己网站的报告、内部审计记录、跨产品品牌源文件、赞助按钮，以及另一个"保留所有权利"授权的产品 Claude Blog Brain（791 个文件） | 仓库只剩插件本身，体积少 6 MB 多；不再替别人存放未授权给本 fork 的内容；CI 少两个 job | 1. 列出顶层全部文件，用 git grep 查每个候选被谁引用<br>2. 分三档交用户审核<br>3. 分三次提交删除：报告和审计文档、品牌和赞助、brain 连带 CI 测试和同步脚本<br>4. 把 /reports/ 加进 .gitignore | pytest 1499 通过 6 跳过；lint_prose、consistency_check、validate_skills、validate_public_release、check_secrets 通过 |
| 002 | 2026-10-17 | 新建二次开发日志 | docs/add-fork-devlog | docs | #2 | CHANGELOG 和提交信息只记"改了什么"，不记动机和做法 | 每次改动的原因、收益、步骤集中在一处，也能分清哪些是自己加的 | 1. 查 docs/ 命名和文档规范<br>2. 新建本文件并补录 001<br>3. 改成一行一条的表格 | lint_prose、consistency_check、validate_public_release 通过；pytest 1531 通过 |
| 001 | 2026-10-17 | 固定本地 Python 为 3.14 | chore/pin-python-314 | chore | #1 | `uv sync` 默认用 3.13.5，其 `html.parser` 处理未闭合标签极慢，一个测试超时 | 本地自动用 3.14，同一输入解析约 0.017 秒，测试恢复正常；CI 不受影响 | 1. 定位超时根因<br>2. 根目录加 `.python-version`（3.14）<br>3. 重建虚拟环境重跑测试 | 该测试在 3.14 下通过 |
