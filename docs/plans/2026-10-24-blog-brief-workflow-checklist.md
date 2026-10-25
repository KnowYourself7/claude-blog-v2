# 开发文档：SKILL.md 的步骤表改成可勾选清单

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-24 |
| 状态 | 已实现 |
| 分支 | feat/blog-brief-workflow-checklist，从合并 A·10 之后的 main 开 |
| 依据 | Anthropic《Skill authoring best practices》「Use workflows for complex tasks」：复杂流程给一份清单，让 Claude 复制到回复里，做完一步勾一步。https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices ；`essentials/skill-dev-rules.md` 第 8 条「每步产物要能检查」 |

## 1. 目标

Claude 打开 blog-brief 的 SKILL.md，就能看到每一步读哪个步骤文件、产出哪个文件、用到前面哪几步的产出、会不会停下来问用户；开工时把清单抄进回复，一步的 Check 全部通过才勾掉，再做下一步。

## 2. 不做什么

| 不做的事 | 去向 |
|---|---|
| 给每一步写检查脚本，像「运行脚本，不通过不得进入下一步」那样。现在多数 Check 要判断（比如「理由写出了排名页的格式」），脚本查不了 | 以后再定。能用脚本查的（文件在不在、某一节有没有）以后可以单独加 |
| 把停下的阈值（博客占比低于 30%、保留面少于 3 个）抄进 SKILL.md | 不做。阈值只写在步骤文件里，清单只标「Can stop」 |
| 让 Step 5 模板推荐写成文件。现在它不写文件，结果靠对话记住，带到 Step 9 | 以后再定。这次只在清单和 Step 9 的 Inputs 里写明这条依赖 |
| 改步骤文件的六段格式，或改任何一步的做法 | 不改 |
| 学粘贴示例建 `work/` 目录 | 不做。产出照旧放 `briefs/` |

## 3. 原因

### 3.1 现在的问题

现在 [SKILL.md](../../skills/blog-brief/SKILL.md) 的 Workflow 是一张三列表：步骤、步骤文件、这一步还要读的其他文件。总流程已经在 SKILL.md 里，但有三处不够：

1. 没写每一步产出什么文件。Step 3 的第 3 列写的是「the Step 1 and Step 2 output files」。Claude 开工前看 SKILL.md，看不出这是 `briefs/[slug]-task-brief.md` 和 `briefs/[slug]-search-intent.md`，也看不出整个流程会留下哪些文件；要做到那一步、回头读前面的步骤文件才知道。
2. 表格不能勾。九步走下来，没有地方记做到哪一步、哪一步的 Check 过了没有。也没有一句话说「Check 没过不能做下一步」。
3. 哪几步会停下问用户（Step 2 意图分流、Step 3 保留面太少），只写在步骤文件里。

### 3.2 表格已经和步骤文件对不上

第 3 列和每个步骤文件的 Inputs 段写的是同一件事，两处分开改，已经有三处不一致：

| 步骤 | SKILL.md 第 3 列 | 步骤文件 Inputs |
|---|---|---|
| Step 2 | 只有 `templates/search-intent.md` | 还读 `briefs/[slug]-task-brief.md` 的市场代码（Step 1 的产出） |
| Step 5 | 没有 Step 2 | 读 `briefs/[slug]-search-intent.md` 的读者任务 |
| Step 9 | 没有 Step 5 | 也没有 Step 5。可是简报的 Template 段要填 Step 5 选的模板 |

问题从这里进来：同一份依赖写了两遍，没有测试把两处对起来。

## 4. 方案

把表格换成清单。清单只写步骤文件名、用到哪几步、产出文件和会不会停下；要读的模板和脚本只写在步骤文件的 Inputs 段，不再在 SKILL.md 重复。加一个测试，把清单和步骤文件对起来。

### 4.1 输入

| 输入 | 拿它做什么 |
|---|---|
| 每个步骤文件的 Outputs 段 | 清单每行的 Output |
| 每个步骤文件的 Inputs 段里 `briefs/[slug]-…` 的文件 | 清单每行的 Uses：这个文件是哪一步产出的 |
| Step 2、Step 3 步骤文件里「stop … Ask the user」的地方 | 清单里标 Can stop |
| Step 5 的 Outputs「No file … go into the Template section of the brief in Step 9」 | Step 9 的 Uses 加 Step 5 |

### 4.2 处理步骤

1. 先写测试 `tests/test_blog_brief_workflow.py`，在旧表上跑，看到它失败。测试查三件事：
   - 清单里每个 Step N 都有步骤文件，文件第一行的「### Step N: 名字」和清单一致。
   - 清单每行的 Output 文件，都写在那个步骤文件的 Outputs 段里。
   - 步骤文件 Inputs 段里每个 `briefs/[slug]-…` 文件，产出它的那一步都在这一行的 Uses 里。
2. 改 SKILL.md 的 Workflow 段，见 4.3。Step 10 的说明段保留，清单里加一行指向它。
3. Step 9 步骤文件的 Inputs 加一行：Step 5 选的模板和理由，填 Template 段。
4. 改 `CLAUDE.md` 的 blog-brief 目录说明。
5. 跑测试和仓库检查，整篇重读 SKILL.md。

### 4.3 输出

SKILL.md 的 Workflow 段改成这样（英文按 simple-english 写；清单放进代码块，Claude 照原样复制）：

````markdown
## Workflow

Copy this progress list into your reply. Do the steps in this order.
Before you start a step, read its step file completely. Do not read a
step file before you start that step. When every item in the `Check`
section of a step is true, mark the step as done. Do not start the
next step before that.

Step files are in `${CLAUDE_SKILL_DIR}/references/`. Paths in the step
files are relative to `${CLAUDE_SKILL_DIR}`. Output files are in
`briefs/` and start with `[slug]-`. "Uses" names the steps whose output
the step reads. "Can stop" means that the step can stop and ask the
user a question. If it stops, wait for the answer.

```
Brief Progress:
- [ ] Step 1: Topic Intake. Read step-1-topic-intake.md. Output: task-brief.md.
- [ ] Step 2: SERP Intent Gate. Read step-2-serp-intent-gate.md. Uses Step 1. Output: search-intent.md. Can stop.
- [ ] Step 3: Keywords to Demand Facets. Read step-3-demand-facets.md. Uses Step 1, Step 2. Output: keyword-research.md, demand-facets.md, and the work files that the step file lists. Can stop.
- [ ] Step 4: Competitor Gap List. Read step-4-competitor-gaps.md. Uses Step 2, Step 3. Output: competitor-gaps.md, competitor-[n].md.
- [ ] Step 5: Template Recommendation. Read step-5-template-recommendation.md. Uses Step 2, Step 4. Output: no file. Keep the template and the reason for Step 9.
- [ ] Step 6: Evidence Plan. Read step-6-evidence-plan.md. Uses Step 3, Step 4. Output: evidence-plan.md.
- [ ] Step 7: Information Gain. Read step-7-information-gain.md. Uses Step 1, Step 4, Step 6. Output: information-gain.md.
- [ ] Step 8: Outline. Read step-8-outline.md. Uses Step 1, Step 2, Step 3, Step 6, Step 7. Output: outline.md.
- [ ] Step 9: Generate the Brief. Read step-9-generate-brief.md. Uses Step 1, Step 2, Step 5, Step 6, Step 7, Step 8. Output: the filled brief, no file.
- [ ] Step 10: Save the Brief. Read the Step 10 section below. Uses Step 9. Output: brief.md.
```
````

Uses 列按 4.1 从步骤文件的 Inputs 推出来，和现在表格的第 3 列比，改了三处：Step 2 加 Step 1，Step 5 加 Step 2，Step 9 加 Step 5。

### 4.4 下游怎么变

- 每次跑 `/blog brief`，回复里会先出现这份清单，做完一步勾一步。真实跑时可以直接看出跳了哪一步。
- 以后改任何步骤文件的 Inputs 或 Outputs，忘了改清单，测试会失败。
- `essentials/skill-file-format.md` 第四节写着「步骤顺序表每行三列」，要改成清单的写法。这个文件在仓库外，不进这个分支的提交，跟这次改动同一天改。

### 4.5 改动文件

| 文件 | 改什么 |
|---|---|
| `skills/blog-brief/SKILL.md` | Workflow 表换成清单 |
| `skills/blog-brief/references/step-9-generate-brief.md` | Inputs 加 Step 5 的模板和理由 |
| `tests/test_blog_brief_workflow.py` | 新建，见 4.2 第 1 步 |
| `CLAUDE.md` | blog-brief 的 `SKILL.md` 说明从「Step order table」改成「Step checklist」 |
| `/Users/Kai/个人项目/essentials/skill-file-format.md`（仓库外） | 第四节改成清单的写法，修订记录加一条 |

## 5. 考虑过、没选的方案

| 方案 | 为什么没选 |
|---|---|
| 保留表格，加一列「产出」 | 表格不能勾，解决不了「做到哪一步」。四列表在 Markdown 原文里也很难读 |
| 表格保留，下面再加一份只有步骤名的清单（官方示例的写法） | 步骤名写两遍，两处都要改 |
| 清单每行把模板、脚本也列全，和现在的第 3 列一样 | 每行太长，复制进回复很乱；又和步骤文件的 Inputs 重复，3.2 的不一致就是这样来的 |
| 不加测试，靠改的时候小心 | 3.2 说明小心不够，三处已经不一致 |

## 6. 验证

| 验证项 | 结果 |
|---|---|
| 先看到失败 | 旧表上跑：2 项失败（找不到清单），3 项跳过。换成清单后 29 项全过。再故意删掉 Step 2 和 Step 9 的一个 Uses，对应 2 项失败，说明测试能抓到不一致 |
| 仓库检查 | pytest 1547 项通过、6 项跳过；`validate_skills.py` 通过；`consistency_check.py` 的 errors 为空；`lint_prose.py` 报 43 处，全在被 gitignore 的 `docs/yudong/`，和本分支无关 |
| 整篇重读 | 改了两处：一行折行过长；Step 3 的「and the script files」改成「the work files that the step file lists」。旧表的第 3 列整列删掉，模板和脚本只留在步骤文件的 Inputs 段。simple-english hook 还报 9 处，都在本分支没改的老段落（第 18 到 40 行、Step 10 段），不在本次范围 |
| 模拟跑（子代理，Haiku，只读 SKILL.md） | 清单部分没有要猜的地方：每步读什么、产出什么、要等哪几步都答对，也答对了 Step 9 的模板来自 Step 5。它提的疑问有两类。设计如此：看不到 Check 的内容、work files 没列名，这两样都在步骤文件里。本分支之前就有：`[slug]` 在整个 skill 里没有定义；第 23 行 `orchestration-details.md` 和清单谁先做没写；第 19 到 21 行的覆盖路径和 sibling roots 没说清。这些不在本次范围 |
| 真实跑 | 没有做。下次在 claude-seo-playground 真实跑 blog-brief 时顺带看：清单有没有抄进回复，有没有在 Check 没过时就开始下一步 |

## 7. 提交拆分

1. `docs(blog-brief): add design for the workflow checklist`
2. `feat(blog-brief): track the brief workflow with a checklist in SKILL.md`
