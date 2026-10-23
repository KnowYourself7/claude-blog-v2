# 开发文档：blog-brief 步骤文件统一成六段格式

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-22 |
| 状态 | 已确认，实现中 |
| 分支 | feat/blog-brief-a06-gap-list（接在任务单和业务筛选之后） |
| 依据 | 瑜东第 00 课：「每一步都要有明确输入、产物和验收」（p.106），`docs/yudong-blog-workflow-小白讲解/00-导读-一篇博客为什么要走20步.md`；质量门要能回答「哪一步有问题、为什么、怎么修」（p.29） |
| 改动范围 | `skills/blog-brief/references/` 下 7 个步骤文件全部重写成同一格式；模板不动；SKILL.md 不动 |

## 1. 为什么改

七个步骤文件是分几次、按不同要求改出来的，格式各不相同：三个有「先读哪些文件」，四个没有；三个有规则段，四个没有；产物藏在输入段的「存为某文件」里；没有一个文件有验收。用户 2026-10-22 指出步骤文件应该有固定格式：目标、输入、处理步骤、产物、规则、自我检查。这正是瑜东「输入、产物、验收」的原则，加上目标和规则。

验收是最缺的一段。瑜东的质量门要在每一步结束时回答「这一步做完了没有」，现在全靠模型自觉。

## 2. 格式

每个步骤文件六段，顺序固定，标题用英文四级标题。模板继续承担填表规则，步骤文件不复述模板正文。

| 段 | 标题 | 写什么 | 不写什么 |
|---|---|---|---|
| 目标 | `#### Goal` | 一句话：这一步把什么变成什么 | 背景、理由 |
| 输入 | `#### Inputs` | 要先读的文件，每个一行：路径加「拿它做什么」。要读的模板也在这里 | 模板里已有的填表规则 |
| 规则 | `#### Rules` | 必须和禁止，每条一两句。接口、失败处理、不许编的东西放这里 | 和模板重复的话 |
| 步骤 | `#### Steps` | 编号，每条以动词开头，写明填到模板的哪一段。判断规则（怎么分类、怎么定去留）放在用到它的那一条里 | 模板已经说明的填表方式 |
| 产物 | `#### Outputs` | 存哪个文件，每个一行。停下问用户时文件里写什么 | 无 |
| 验收 | `#### Check` | 三到五条是否题，做完一步先自答，答不上就回去修。写成「每个保留的面都有一句问题和保留理由」这种可以逐条核对的句子 | 感受式的话（「质量好」） |

句子按 simple-english：步骤句不超过 20 个词，说明句不超过 25 个词，不用分号和破折号。引用别的步骤用 SKILL.md 的编号（Step 2、Step 3），不用瑜东编号。

## 3. 七个文件各段的内容

| 步骤 | Goal | Inputs | Outputs | Check 要查什么 |
|---|---|---|---|---|
| 1 Topic Intake | 把用户的话变成任务单 | 任务单模板 | task-brief | 每格有值或 missing；没有推断的品牌事实；市场有值 |
| 2 SERP Intent Gate | 判断这个词该不该写博客 | 搜索意图模板、任务单 | search-intent | 每条结果有 Label 和 On topic；占比有算式；读者任务一句话；停下时 User choice 为 pending |
| 3 Keywords to Demand Facets | 把关键词变成需求面 | 两个模板、搜索意图、任务单 | keyword-research、demand-facets | 保留的面 3 到 9 个；每个面有问题、证据、理由；null 没写成 0；前 50 行都有归属 |
| 4 Template Recommendation | 选一个内容模板 | 模板选择指南、搜索意图、关键词文件 | 无文件，结论进 Step 7 | 选择理由是标题计数；只选了一个 |
| 5 Competitor Gap List | 把竞品拆成差距清单 | 两个模板、搜索意图、需求面 | competitor-gaps、competitor-[n] | 每个竞品一个文件；失败页不在 Gap List；每条差距有类型和面；差异一句 |
| 6 Statistics Research | 找文章要用的数字 | 无文件 | 无文件，结论进 Step 7 | 每个数字有出处、网址、日期；核不了的已丢掉 |
| 7 Generate the Brief | 把研究变成简报 | 简报模板、搜索意图、需求面、差距清单 | brief | 每个面至少一个 H2；差距只来自差距清单文件；没有无依据的 first-hand 声明 |

Step 8 保存简报留在 SKILL.md 里，只有两句，不单独成文件。

## 4. 不改的内容

- 规则本身不变。这次只换格式和去重，含义有变化要单独说明并记在本文档。
- Step 4 和 Step 6 是上游原文，这次只套格式，不按瑜东重做；Step 6 要等路线图第 6 个分支的证据表。
- 上游测试钉死的句子原样保留在同一行：Step 7 的 "only when the user supplies supporting methodology"。

## 5. 验证

1. 仓库检查：pytest、validate_skills、lint_prose、consistency_check。
2. 子代理对照每个文件的新旧两版，列出含义变化和歧义句；含义变化必须为零或在本文档说明。2026-10-22 已跑：七个文件规则无丢失，唯一的含义变化是 Step 2 的市场代码改从任务单取（有意为之，Step 1 写市场）。据此改了六处：Step 1 的步骤补写 `given`，和验收对齐；Step 2 把 SERP 调用从规则段挪回步骤第 1 条（原来没有一条说去调）、「Mark each item on topic」改成「as on topic or off topic」、停下时的验收改成看文件里的页面类型而不是看对话；Step 4 的验收从「理由是标题计数」改成「附上决定它的计数」，删掉查不了的「模板文件已读」；Step 6 的「Mark」改成「Note … for the Visual Element Plan」，说明记到哪里；Step 7 的验收写明是 Competitive Gaps 的三个编号项。两处验收仍要看对话而不是产物（Step 1 的品牌事实来源、Step 7 的 first-hand 证据），保留，因为它们查的就是用户给没给。
3. 真实跑在 playground：`can you wear linen in winter` 加 Coofandy 背景，看每步的 Check 是否被执行、产物是否齐全。

## 6. 提交拆分

1. `docs(blog-brief): define the six-section format for step files`
2. `refactor(blog-brief): rewrite the seven step files in the six-section format`

## 出处

- 瑜东 00 课：`docs/yudong-blog-workflow-小白讲解/00-导读-一篇博客为什么要走20步.md`
- 写法规范：simple-english skill；writing-skills skill 的 token 效率和「模板承担填表规则」原则
