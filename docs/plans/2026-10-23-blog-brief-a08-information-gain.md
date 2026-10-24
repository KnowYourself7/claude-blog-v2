# 开发文档：blog-brief 加一步「信息增量」

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已合并（#14）。Step 7 的表格和简报的增量段由 `docs/plans/2026-10-23-blog-brief-a08-gain-list-fix.md` 修正 |
| 分支 | feat/blog-brief-a08-information-gain |
| 依据 | 瑜东第 04 课 A·08「规划信息增量」（p.121-122）；第 05 课 A·10 大纲的输入（p.125） |

## 1. 目标

简报的大纲里只出现写给读者的话，不出现对竞品页面的评价。

## 2. 不做什么

- 不改大纲每一节的字段（Cover 这些）。这是下一个分支。
- 不加大纲 v1、自审、v2。这是路线图第 7 个分支。
- 不让 Step 6 统计数字落盘成文件。这是路线图第 6 个分支剩下的一半。
- 不改 blog-write 和 blog-reviewer。
- 不改 Step 4 竞品差距清单。

## 3. 原因

现在的问题：Coofandy 那篇亚麻衬衫文章，正文里出现了给别的网站打分的话。例如正文第 35 行：「the sites that say "pack it away" are right about that one case」。

这句话是这样来的：

1. Step 4 差距清单 G4 记下：四家说亚麻能调温，没来源，第五家说相反。这是研究笔记，主语是竞品页面。
2. 原 Step 7 生成简报时，直接读差距清单，把笔记写进了大纲 Cover 行：「the fifth-ranked page's "no" is right for that case」。
3. blog-write 按大纲逐节展开，笔记就成了正文。

瑜东的做法中间多一步。他的大纲不读差距清单，读的是「信息增量」。信息增量就是读者看完这篇，比看完现有搜索结果多得到的东西。竞品信息先翻译成信息增量，主语就从竞品换成了读者。

第 04 课还有一条规则：「缺少证据就缩小结论」。原简报里的温度分段没有来源，结果正文写了「这是经验法则，不是实验数据」这种免责句。正确做法是在写大纲之前就收窄说法。

## 4. 方案

在 Step 6 统计数字之后，加一步新的 Step 7「信息增量」。原 Step 7 生成简报改为 Step 8，原 Step 8 保存改为 Step 9。

### 4.1 新 Step 7 的输入

| 输入 | 拿它做什么 |
|---|---|
| `briefs/[slug]-competitor-gaps.md` | 差距清单、本篇差异、格式优势：要翻译的原料 |
| `briefs/[slug]-task-brief.md` | 「不卖、不能说」那一行：哪些增量不能写 |
| Step 6 保留的统计数字（不落盘，在上下文里） | 每条增量的证据 |
| `templates/information-gain.md` | 要填的表 |

### 4.2 新 Step 7 的处理步骤

1. 从「本篇差异」写一句主增量：看完这篇，读者能做什么。
2. 每条差距写成一行增量。两条差距指向同一个增量，就合成一行。
3. 格式优势不是 none，就再写一行。
4. 每行填证据：哪条统计数字支持它。没有统计数字，就写 `none` 和收窄后的说法。
5. 第一方证据：只写用户提供的方法、证据和结果。没有就写 `none supplied`。

规则（都来自第 04 课）：写得更长、抓更多页、换个说法，都不算增量；别人的研究不能写成用户自己的；给方法起个名字，不等于证明它有效；没有证据就收窄说法，不能保留说法再加免责。

### 4.3 新 Step 7 的输出

`briefs/[slug]-information-gain.md`，一张表：

| 列 | 写什么 | 进不进大纲 |
|---|---|---|
| The ranking pages give | 排名页面现在给了读者什么 | 不进，只留在这个文件里 |
| This post adds | 看完这篇，读者能多理解、多判断或多完成什么 | 进 |
| Evidence | 支持它的统计数字，或 none 加收窄说法 | 进 |

### 4.4 下游怎么变

- Step 8 生成简报：输入里的差距清单换成信息增量文件。大纲只取 This post adds 和 Evidence 两列。
- 简报模板：删掉 Competitive Gaps to Exploit 段；Information Gain Opportunities 段改成列出各条增量。
- SKILL.md：DISCOURSE.md 的主题改为在 Step 7 进入增量文件，不再直接加进简报。否则会和 Step 8「只用增量文件里的增量」冲突。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/references/step-7-information-gain.md` | 新建 |
| `skills/blog-brief/templates/information-gain.md` | 新建 |
| `skills/blog-brief/references/step-8-generate-brief.md` | 由原 Step 7 改名，输入和规则改成读增量文件 |
| `skills/blog-brief/templates/brief-template.md` | 删一段，改一段 |
| `skills/blog-brief/SKILL.md` | 步骤表加一行，DISCOURSE.md 那句改指向 |
| Step 2、5、6 三个步骤文件 | 「Step 7」改成「Step 8」 |
| `tests/test_release_safeguards.py` | 文件路径改成 step-8 |
| `CLAUDE.md` | 目录树里的数量改成 8 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 只改简报模板的 Cover 一行，写明「写给读者」 | 只堵住一行。差距清单还是 Step 8 的输入，竞品信息还能从别的行漏进大纲 |
| 新步骤放在 Step 4 之后 | 瑜东是先证据（A·07）后增量（A·08），增量要用到证据；而且要改名三个步骤文件，放在 Step 6 之后只改名一个 |

## 6. 验证

| 验证 | 结果 |
|---|---|
| pytest | 1518 通过，6 跳过 |
| validate_skills、consistency_check | 通过，errors 为空 |
| lint_prose | 新文件没有违规；剩下 43 处在被 `.gitignore` 忽略的瑜东讲解目录里，CI 看不到 |
| 真实跑：亚麻衬衫已有产物上只跑 Step 7 和 Step 8，输出在 Coofandy 工作区的 `rerun-2026-10-23-information-gain/` | G4 翻译成「读者能明白亚麻透气，暖和来自外面那几层」；大纲里搜不到竞品页面、排名或差距；温度分界标成【需确认】，没写具体度数 |

真实跑发现、留给下个分支的问题：大纲 Cover 行里仍有写给写手的话，例如「because no kept statistic sets them」。

## 7. 提交拆分

1. `docs(blog-brief): add design for the information gain step`
2. `feat(blog-brief): translate competitor gaps into reader gains before the brief`
