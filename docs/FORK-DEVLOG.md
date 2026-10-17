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
| 002 | 2026-10-17 | 新建二次开发日志 | docs/add-fork-devlog | docs | #2 | CHANGELOG 和提交信息只记"改了什么"，不记动机和做法 | 每次改动的原因、收益、步骤集中在一处，也能分清哪些是自己加的 | 1. 查 docs/ 命名和文档规范<br>2. 新建本文件并补录 001<br>3. 改成一行一条的表格 | lint_prose、consistency_check、validate_public_release 通过；pytest 1531 通过 |
| 001 | 2026-10-17 | 固定本地 Python 为 3.14 | chore/pin-python-314 | chore | #1 | `uv sync` 默认用 3.13.5，其 `html.parser` 处理未闭合标签极慢，一个测试超时 | 本地自动用 3.14，同一输入解析约 0.017 秒，测试恢复正常；CI 不受影响 | 1. 定位超时根因<br>2. 根目录加 `.python-version`（3.14）<br>3. 重建虚拟环境重跑测试 | 该测试在 3.14 下通过 |
