# 开发文档：任务单收同站页面清单，大纲按清单安排内链

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-24 |
| 状态 | 计划中。等 `feat/blog-brief-a10-outline` 合并后，从 `main` 开分支。2026-10-26 补记：#24 给任务单加了 Delivery 表，#25 加了 Role 行，Step 1 和 Step 8 都改过。动手前要按新的任务单模板改写本计划，cluster 文章链回 pillar 也可以放进来。2026-10-27 补记：Existing Pages 表（URL、Covers、Type）和 Step 1 的撞题检查由分支 feat/upgrade-step-1-topic-intake 做了，见 2026-10-27-blog-brief-step-1-yudong-intake.md；本计划只剩 Step 8、Step 9 的内链部分，动手前删掉第 2 节「不做」表里的撞题一行和 4.2 第 1 条 |
| 分支 | feat/blog-brief-internal-link-pages（暂定） |
| 依据 | 第 01 课资料盘点单「已有网站资料：产品网址清单、同站博客清单，用于选内链和避免重复」（p.110）；第 05 课第二版「确定表格、案例、内链的位置」（p.125）；第 07 课自然内链「连接支柱页和相关内容」、条数「没有通用标准」（p.132-133） |
| 来源 | `docs/reviews/2026-10-24-blog-brief-narrow-constraints.md` 的 A1 |

## 1. 目标

用户给了同站页面清单时，简报的大纲在需要的 H2 里写出要链到清单上哪个页面、为什么；清单上没有合适页面时，写清需要一篇讲什么的页面。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| Link FROM（反向内链：老页面加链接指向新文章）。要改的是用户网站上的老页面，课程 A 阶段也没讲 | 照旧写 `missing`，以后要做再单独开分支 |
| 自动读站点 sitemap.xml 拿页面列表。要改 Step 1「不打开网站」的规则，还要多一次抓取和失败处理 | 不做。2026-10-24 用户选了「用户给清单」 |
| 检查清单上的网址能不能打开 | 不做。`blog-write` 第 6.5 阶段会把每条内链换成真实存在的页面，换不了就删掉 |
| 用清单判断「站内是否已经写过这个题」（第 01 课的「避免重复」） | 以后再定。这次只用清单安排内链 |
| 评审文档里的 A2、A3、B1、B2、D | 各自单独开分支 |

## 3. 原因

### 3.1 现在的问题

现在从 Step 1 到 Step 9，内链只认任务单的 Page this post supports 这一个页面。

1. 改大纲前，内链全靠猜。Coofandy 亚麻例子的 10 条内链写着 `URL to confirm` 和 `not checked: may not exist`（a10 开发文档 3.1 第 6 条）。
2. a10 为了不再猜网址，规定内链只连支撑页，其余写 `missing`。见 `step-8-outline.md` 第 73-74 行、`step-9-generate-brief.md` 第 26 行，`brief-template.md` 第 76 行更是把 `Other pages: missing` 写死了。
3. 结果是：用户就算手上有同站博客清单，简报也只能有 1 条内链。一篇讲冬天穿亚麻的文章，没法链到同站讲亚麻洗护或叠穿的文章。

### 3.2 问题从哪一步进来

问题出在 Step 1：任务单没有地方收同站页面清单。瑜东的资料盘点单有这一项（p.110），我们的任务单只有 Brand、Domain、Sells、Page this post supports 这些格子。后面的步骤没有输入，只能写 `missing`。a10 开发文档第 2 节已经把这件事记成「以后改 Step 1 时再定」。

## 4. 方案

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 用户的话 | Step 1 从里面抄同站页面：网址、讲什么、页面类型。用户没给就写 `missing` |
| `briefs/[slug]-task-brief.md` 的新表 Existing Pages | Step 8 从里面选内链 |
| `briefs/[slug]-outline.md` 第二版每个 H2 的 Components 行 | Step 9 从里面汇总 Link TO |

### 4.2 处理步骤

1. Step 1 任务单加一张表 Existing Pages，三列：URL、Covers（讲什么，用用户的话）、Type（product、category、post，或别的类型，例如 tool）。规则沿用 Step 1：只抄用户给的，不打开网站，不推断。
2. Step 8 第二版的 Components 行，内链写成两种之一：
   - `internal link: [URL], [读者为什么在这里需要它]`。URL 只能是 Existing Pages 里的网址或 Page this post supports。
   - `internal link: missing, a page about [X]`。读者在这里确实需要继续了解，但清单上没有合适页面。
3. Step 8 的规则从「Link only to the Page this post supports」改成：只链到任务单里出现过的网址；不猜网址。内链放在读者需要继续了解的地方（第 07 课），不设条数。
4. Step 9 的 Link TO 按第二版的顺序列出每一条内链，原样抄 Components 里的写法。Link FROM 照旧写 `missing`。

### 4.3 输出

| 文件 | 变化 |
|---|---|
| `briefs/[slug]-task-brief.md` | 多一张 Existing Pages 表（URL、Covers、Type），没给时一行 `missing` |
| `briefs/[slug]-outline.md` | 第二版 Components 里的内链用上面两种写法 |
| `briefs/[slug]-brief.md` | Internal Link Architecture 的 Link TO 是多条，不再写死 `Other pages: missing` |

### 4.4 下游怎么变

- `blog-write` 不用改。它本来就把内链写成 `[INTERNAL-LINK: anchor text → target description]` 占位，再在第 6.5 阶段换成真实页面。简报里 `missing, a page about [X]` 那句话正好当它的 target description。
- 用户什么清单都没给时，简报和现在一样只有支撑页，只是多了几条带需求描述的 `missing`。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/templates/task-brief.md` | 加 Existing Pages 表 |
| `skills/blog-brief/references/step-1-topic-intake.md` | Steps 加一项「已有页面」；Check 加一条 |
| `skills/blog-brief/references/step-8-outline.md` | 第 73-74 行内链规则、Components 两种写法、第 90-91 行 Check |
| `skills/blog-brief/templates/outline.md` | 第 52 行 Components 的占位说明加上内链的两种写法 |
| `skills/blog-brief/references/step-9-generate-brief.md` | 输入加大纲 Components；第 26 行规则和第 42 行 Check |
| `skills/blog-brief/templates/brief-template.md` | Link TO 改成按第二版列出多条，删 `Other pages: missing` |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 自动读 sitemap.xml | 要改 Step 1「不打开网站」，多一次抓取和失败处理；sitemap 只有网址，没有「讲什么」。用户 2026-10-24 没选 |
| 只用用户清单，没有清单就整段 `missing` | 读者需要继续了解的地方就丢了，`blog-write` 拿不到 target description。用户 2026-10-24 没选 |
| 内链只在 Step 9 汇总成一张表，大纲里不写 | 第 05 课要第二版「确定内链的位置」（p.125），位置只能写在 H2 里 |
| 顺手做 Link FROM | 一分支一功能。用户 2026-10-24 选这次不做 |

## 6. 验证

| 验证项 | 打算怎么验 |
|---|---|
| 仓库检查 | `python3 -m pytest tests/`、`python3 scripts/lint_prose.py`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/consistency_check.py`（看 errors） |
| 整篇重读 | 改过的 6 个文件每一句问：谁需要、删了坏什么、模板是否已写；报告删了什么 |
| 模拟跑（子代理） | 只按新文件做 Step 1、8、9，两种情况：用户给了 3 个同站页面；用户什么都没给。报告每一处不得不猜的地方 |
| 真实跑（子代理，在 playground） | 亚麻例子补一份同站页面清单，重跑 Step 8、9：内链网址是否都在任务单里；`missing` 是否都有需求描述；有没有再猜网址 |

## 7. 提交拆分

1. `docs(blog-brief): add design for internal links from an existing-pages list`
2. `feat(blog-brief): collect existing pages in Step 1 and place internal links in the outline`
