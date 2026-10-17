# 二次开发日志

本文件记录这个 fork（[KnowYourself7/claude-blog-v2](https://github.com/KnowYourself7/claude-blog-v2)）
在上游 [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) 基础上做的每一次改动。

## 和其他记录的分工

| 记录 | 写给谁 | 写什么 |
|------|--------|--------|
| `CHANGELOG.md` | 使用者 | 每个版本改了什么（上游维护，Keep a Changelog 格式） |
| git 提交信息 | 看代码历史的人 | 单次提交改了什么、为什么 |
| 本文件 | 自己 | 一个功能从动机到落地的完整经过，跨多个提交 |

## 记录规则

- 新条目写在最上面（倒序），和 `CHANGELOG.md` 一致。
- 每个功能分支合并前补一条；分支名、PR 号写全，方便回查。
- 编号连续递增，不复用。
- 分支名不加反引号：`scripts/consistency_check.py` 会把反引号里以 docs/ 开头的文字当成文件路径检查。
- 禁止使用破折号（U+2014、U+2013）和两侧带空格的双连字符，`scripts/lint_prose.py` 会检查。中文破折号也属于 U+2014，可改用冒号、逗号或括号。

## 条目模板

```markdown
## NNN. 标题（YYYY-MM-DD）

- 分支：type/short-name
- PR：#N
- 类型：feat / fix / docs / chore / refactor / test

### 开发原因

遇到了什么问题，或想要什么能力。

### 带来的提升

改完之后具体好在哪里，能量化就量化。

### 开发步骤

1. 第一步
2. 第二步

### 验证

跑了哪些命令，结果如何。
```

## 002. 新建二次开发日志（2026-10-17）

- 分支：docs/add-fork-devlog
- PR：待创建
- 类型：docs

### 开发原因

`CHANGELOG.md` 和提交信息只记录"改了什么"，不记录一个功能的完整动机和做法。
时间一长，自己会忘记当初为什么这样改。

### 带来的提升

每次二次开发都有一处固定位置回顾原因、收益和步骤；和上游同步时，
也能快速分清哪些改动是自己加的。

### 开发步骤

1. 查看 `docs/` 现有命名（全大写文件名）和 `.github/CONTRIBUTING.md` 的文档规范。
2. 确认 `scripts/lint_prose.py` 会扫描 `docs/`，不能出现破折号。
3. 新建分支 docs/add-fork-devlog，添加本文件，并补录第 001 条。
4. `scripts/consistency_check.py` 把反引号里的分支名误判为缺失路径，改成纯文本后通过。

### 验证

`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`、
`python3 scripts/validate_public_release.py` 通过。

## 001. 固定本地 Python 版本为 3.14（2026-10-17）

- 分支：chore/pin-python-314
- PR：#1
- 类型：chore

### 开发原因

不指定版本时，`uv sync` 会选用 CPython 3.13.5。它自带的 `html.parser`
处理大量未闭合标签时耗时呈平方增长，导致
`tests/test_preflight_wave3.py::test_document_audit_is_linear_on_hostile_markup`
跑几分钟后超出 5 秒限制而失败。

### 带来的提升

本地建环境自动使用 3.14，同一输入解析耗时降到约 0.017 秒，测试恢复正常。
CI 不受影响，它用 pip 按版本矩阵安装。

### 开发步骤

1. 定位超时测试，确认根因是 Python 3.13.5 的 `html.parser`。
2. 在仓库根目录添加 `.python-version`，内容为 `3.14`。
3. 用 3.14 重建虚拟环境并重跑测试。

### 验证

`python3 -m pytest tests/` 中该测试在 3.14 下通过。
