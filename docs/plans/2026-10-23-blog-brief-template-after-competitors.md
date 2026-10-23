# 开发文档：模板选择挂到竞品拆解之后，按页面结构判断

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-23 |
| 状态 | 已确认，实现中（用户定：挂到竞品拆解之后） |
| 分支 | feat/blog-brief-a06-gap-list（接在 cd1a347 之后） |
| 依据 | 瑜东 A·03「页面类型由实时搜索结果决定」（第 02 课 p.111）；用户 2026-10-23：选模板要看 SERP，不能因为需求面是问句就选 faq |
| 改动范围 | 步骤 4 和 5 对调：`step-4-competitor-gaps.md`、`step-5-template-recommendation.md`（改名加重写）；SKILL.md 步骤表两行加 Step 7 一行；两个竞品模板注释里的步骤号 |

## 1. 为什么改

Coofandy 真实跑（2026-10-23）选了 faq-knowledge，理由是五个博客标题里 2 个问句最多，加上「保留的面都是问句」。两处都不成立：标题是问句不等于页面是问答式参考页，五个竞品实际都是分节讲叠穿、单品、场合的指南；需求面按规则就写成问句，不能当格式信号。faq-knowledge 模板自己也写着少于 10 个问题不该用。

根子是原 Step 4 排在竞品拆解之前，手里只有标题和关键词，只能数标题里的词。能看出页面格式的是竞品详情文件的 Structure 表。

## 2. 改完的样子

顺序变成：1 任务单、2 SERP 闸门、3 需求面、4 竞品差距清单、5 模板选择、6 统计数字、7 简报、8 保存。模板选择的输入是各竞品详情文件的 Structure 段；规则：按页面结构判形状（编号条目 listicle、步骤 how-to-guide、五个以上问句标题 faq-knowledge、并排比较 comparison、其他取选择指南最近的一行），标题问句不算 faq；取最多竞品共有的形状，平局取排名最高的那页；不按需求面、不按我们的关键词判。

用户看过第一版后要求简化：不要形状判定表，核心流程就是读搜索意图文件理解任务、读竞品文件看对手格式、再从 12 个模板里选一个。第二版 Step 5 按这三步写，一条规则：从排名页面选，不从需求面或标题词选。

## 3. 验证

仓库检查；真实跑时看 Coofandy 这个题会不会改选 how-to-guide。

## 4. 提交拆分

1. `docs(blog-brief): add design for template selection after the competitor step`
2. `refactor(blog-brief): choose the template from competitor page structure after Step 4`
