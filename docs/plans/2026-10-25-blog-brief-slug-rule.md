# 开发文档：Step 1 定下 slug 的做法

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-25 |
| 状态 | 已提交，未开 PR |
| 分支 | feat/blog-brief-slug-rule |
| 依据 | 仓库 `skills/blog-cluster/SKILL.md` 的 slug 规则；Django `slugify`；POSIX 可移植文件名字符集；Google URL 结构建议 |

slug（白话：文件名开头那段代表主题的短名字，比如 `can-you-wear-linen-in-winter`）。

## 1. 目标

不管哪个模型跑 blog-brief，同一个焦点词都得到同一个 slug，后面每一步都能按 `briefs/[slug]-*.md` 找到前面的文件。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| SKILL.md 进度清单旁加一句「Step 1 定 slug」，并给 Step 1 那一行加 `Can stop`（焦点词全非英文时 Step 1 会停下问） | SKILL.md 这一段正被 feat/blog-brief-workflow-checklist 改写，同时改会冲突。两个分支谁后合并，谁补上 `Can stop` |
| `briefs/` 里已有同名文件时怎么办（覆盖还是另起名） | 以后再定。现在的步骤文件都没讲，不在这次范围 |
| 用户自己给 slug 时照用 | 这次没讨论，不加。以后有需要再定 |
| 去虚词（can、you、in）缩短 slug | 2026-10-25 用户选了「焦点词全保留」 |
| 写一个脚本生成 slug | 规则只有几句，模型照做即可。多一个脚本要多维护一份代码和测试 |

## 3. 原因

### 3.1 现在的问题

`skills/blog-brief/` 里 30 多处输出路径写成 `briefs/[slug]-*.md`，例如 `references/step-1-topic-intake.md` 第 31 行的 `briefs/[slug]-task-brief.md`。可是没有一个文件说 `[slug]` 怎么来。

2026-10-25 feat/blog-brief-workflow-checklist 分支做模拟跑：一个 Haiku 子代理只按 `skills/blog-brief/SKILL.md` 做，拿到主题 "can you wear linen in winter"，推不出 slug，只能猜。

问题从 Step 1 进来：Step 1 是第一个写文件的步骤，它不定 slug，后面每一步就各自去猜。2026-10-24 的真实跑碰巧写成 `can-you-wear-linen-in-winter`（`rerun-2026-10-24-gain-list-5/can-you-wear-linen-in-winter-brief.md`），但换一个模型或换一次运行，没有东西保证还是这个名字。

### 3.2 瑜东课程怎么说

无。第 01 课只列了原始文件名（`_blog_workflow_state.json` 等），并注明「课程没有专门讲这条命名规则」（`docs/yudong/01-开工前-任务单与先复用再补研究.md` 第 101 行）。所以这条规则是我们自己定的，依据见文件开头的表和第 4 节。

### 3.3 上游原版怎么说

上游 `git show 3544423:skills/blog-brief/SKILL.md` 第 289 行同样只写 `briefs/[slug]-brief.md`，没讲 slug 怎么来。原版只有一个输出文件，猜错也只影响一个文件名；我们现在有十几个文件互相引用，猜错会断链。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 任务单里的焦点词（Focus keyword） | slug 从它生成 |

### 4.2 处理步骤

1. 字母改成小写。带重音的字母换成不带重音的，例如 `é` 换成 `e`。
2. 删掉 a-z、0-9、空格、连字符以外的字符。撇号也删，`men's` 变成 `mens`；中文字符也删。
3. 连续的空格和连字符换成一个连字符，去掉开头和结尾的连字符。
4. 如果一个字母或数字都不剩（比如焦点词全是中文），停下来请用户给一个英文 slug。

例子：`can you wear linen in winter` 得到 `can-you-wear-linen-in-winter`。

这四步就是 Django `slugify` 的默认做法，只差一处：Django 保留下划线，我们删掉，和 `skills/blog-cluster/SKILL.md` 第 135 行「只有小写字母、数字、连字符」一致。只用 a-z、0-9 和连字符，也在 POSIX 可移植文件名字符集之内；连字符分词是 Google URL 建议的写法。

2026-10-25 用户定了三件事：用焦点词全保留；非英文先去重音，剩不下就问；slug 写进任务单。

### 4.3 输出

任务单 `briefs/[slug]-task-brief.md` 的 Topic 表多一行 Slug，值就是生成的 slug。

### 4.4 下游怎么变

后面的步骤不用改。它们的路径本来就写 `[slug]`，现在 slug 有了唯一来源：任务单的 Slug 行。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-1-topic-intake.md` | Steps 加第 2 条 Slug，写上面四步；Check 加一条 slug 只含 a-z、0-9 和单个连字符，并且和文件名一致 |
| `skills/blog-brief/templates/task-brief.md` | Topic 表在 Focus keyword 下加一行 `Slug` |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 去掉虚词，得到 `wear-linen-winter` | 更短，但哪些算虚词要再列一张表，模型容易删得不一样。用户没选 |
| 每次停下来问用户 | 最准，但每篇都多一次来回。用户没选 |
| 保留中文等原文字符（Django `allow_unicode=True`） | 少问一次，但非 ASCII 文件名在部分系统和命令行里容易出问题。用户没选 |
| 规则写在 SKILL.md | 一条规则只在一个地方写；Step 1 是第一个用 slug 的步骤，规则归它。SKILL.md 这段也正在别的分支改 |

## 6. 验证

| 验证项 | 结果 |
|---|---|
| `.venv/bin/python -m pytest tests/` | 1518 passed, 6 skipped |
| `scripts/validate_skills.py --root .` | 全部通过 |
| `scripts/consistency_check.py --root .` 的 errors | `[]`，warnings 0 |
| `scripts/lint_prose.py` | zero prose-hygiene violations |
| 模拟跑：Haiku 子代理只读 Step 1 文件和模板，给四个主题 | 四个都对：`can-you-wear-linen-in-winter`、`mens-linen-shirts-pants`（来自 "Men's Linen Shirts / Pants"）、`cafe-linen-2026-guide`（来自 "Café linen" 加两个连字符再加 "2026 guide"）、"亚麻冬天能穿吗" 停下来问用户。发现一处能两读：停下的条件原写 "no letter or digit stays"，中文也可以算 letter，和删字符那条打架。已改成 "If nothing stays"。`briefs/` 放在哪个目录它也要猜，那是 SKILL.md Step 10 的事，子代理按要求没读 SKILL.md，不算本次问题 |
| 对照瑜东 | 课程没讲命名规则（第 01 课第 101 行），不冲突。这条规则是我们自己加的 |
| 对照上游原版 | 增益：多文件之间不再因 slug 猜错断链。代价：Step 1 多一条步骤和一行表，每次多几十个 token。未做真实跑对照 |

## 7. 提交拆分

一个提交：

```
feat(blog-brief): define how Step 1 makes the slug
```
