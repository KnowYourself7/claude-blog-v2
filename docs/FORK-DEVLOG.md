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
| 004 | 2026-10-17 | CI 分层：PR 只跑快速检查，main 跑全量 | chore/tier-ci-pr-vs-main | chore | #4 | 每个 PR 都跑 31 个任务，包括 4 个 Python 版本、3 个系统的锁文件安装和 Windows 安装器，机器总用时约 33 分钟 | PR 上只剩 7 个任务，机器用时约 7 分钟；推到 main 或手动触发仍跑全量。等待时间仍约 6 分钟，瓶颈是 test (3.14) 本身 | 1. 查 GitHub 官方文档：任务级 if 跳过时算成功；工作流级 paths 过滤会让检查卡在 Pending<br>2. 量上次 PR 各任务耗时<br>3. 加 workflow_dispatch；test 矩阵用 fromJSON 按事件切换；4 个重任务加 if<br>4. 更新并补充 ci.yml 结构测试 | pytest 1502 通过 6 跳过；lint_prose、consistency_check、actionlint 通过 |
| 003 | 2026-10-17 | 删除上游作者私自加入的无关文件 | chore/remove-unrelated-files | chore | #3 | 仓库里混着上游作者的私人产物：审计自己网站的报告、内部审计记录、跨产品品牌源文件、赞助按钮，以及另一个"保留所有权利"授权的产品 Claude Blog Brain（791 个文件） | 仓库只剩插件本身，体积少 6 MB 多；不再替别人存放未授权给本 fork 的内容；CI 少两个 job | 1. 列出顶层全部文件，用 git grep 查每个候选被谁引用<br>2. 分三档交用户审核<br>3. 分三次提交删除：报告和审计文档、品牌和赞助、brain 连带 CI 测试和同步脚本<br>4. 把 /reports/ 加进 .gitignore | pytest 1499 通过 6 跳过；lint_prose、consistency_check、validate_skills、validate_public_release、check_secrets 通过 |
| 002 | 2026-10-17 | 新建二次开发日志 | docs/add-fork-devlog | docs | #2 | CHANGELOG 和提交信息只记"改了什么"，不记动机和做法 | 每次改动的原因、收益、步骤集中在一处，也能分清哪些是自己加的 | 1. 查 docs/ 命名和文档规范<br>2. 新建本文件并补录 001<br>3. 改成一行一条的表格 | lint_prose、consistency_check、validate_public_release 通过；pytest 1531 通过 |
| 001 | 2026-10-17 | 固定本地 Python 为 3.14 | chore/pin-python-314 | chore | #1 | `uv sync` 默认用 3.13.5，其 `html.parser` 处理未闭合标签极慢，一个测试超时 | 本地自动用 3.14，同一输入解析约 0.017 秒，测试恢复正常；CI 不受影响 | 1. 定位超时根因<br>2. 根目录加 `.python-version`（3.14）<br>3. 重建虚拟环境重跑测试 | 该测试在 3.14 下通过 |
