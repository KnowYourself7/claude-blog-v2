# 开发文档：blog-brief 每一步拆成单独文件

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-22 |
| 状态 | 待确认 |
| 分支 | refactor/blog-brief-step-files（从 main 的 aa50215 开出） |
| 依据 | 路线二第一段：先搭架子，再一步一步换成瑜东阶段 A 的做法 |
| 改动范围 | `skills/blog-brief/SKILL.md`、新建 `skills/blog-brief/references/` 下 7 个文件、`tests/test_release_safeguards.py` 一行路径、`CLAUDE.md` 目录树 |

## 1. 为什么改

blog-brief 现在有 261 行，所有步骤都写在一个 `SKILL.md` 里。接下来每一步都要换成瑜东的做法，而且每一步都会变长，比如瑜东 a10 光是大纲自审就有五项。如果全部塞进一个文件，会超过仓库规定的 500 行上限，也做不到一个分支只换一步。

这个分支只搬家，不改内容。这样以后跑出来的结果有变化，就能确定是哪个分支的内容改动造成的，不会和搬家混在一起。Google 的代码评审规范也建议，把重构（只改结构、不改行为）和功能改动分开提交。

## 2. 改完的样子

```
skills/blog-brief/
  SKILL.md                                  总控：读入规则、步骤顺序表、Step 6
  references/
    a01-topic-intake.md                     现在的 Step 1
    a03-serp-intent-gate.md                 现在的 Step 1.5
    a05-demand-facets.md                    现在的 Step 2
    template-recommendation.md              现在的 Step 2.5
    a06-competitive-analysis.md             现在的 Step 3
    a07-statistics-research.md              现在的 Step 4
    a10-generate-brief.md                   现在的 Step 5
  templates/                                不动
    brief-template.md
    demand-facets.md
    keyword-research.md
```

`SKILL.md` 里各段的去向：

| 现在的段落 | 去向 |
|---|---|
| frontmatter、路径说明、Reference documents | 留在 SKILL.md，不改 |
| Auto-loaded inputs、Cross-reference | 留在 SKILL.md，不改。测试要求 "Auto-loaded Project-Root Context" 和 "Niche / single-source themes" 在 SKILL.md 里 |
| Step 1 到 Step 5 | 各搬进一个文件，标题和正文不改 |
| Step 6: Save the Brief | 留在 SKILL.md。它只有三行，讲的是存到哪里，属于总控 |
| 新增 | Workflow 段改成读入规则加步骤顺序表，草稿见第 5 节 |
| 行数 | SKILL.md 从 261 行降到 90 行左右；最长的 `a05-demand-facets.md` 约 103 行，低于新参考文件 200 行的要求 |

## 3. 文件放哪里、叫什么

放在 `references/`。这是 Agent Skills 规范约定的目录名，用来放"Claude 用到时才读"的说明文件。本仓库的其他子 skill 也用这个名字，比如 blog-cluster、blog-google。原型用的是 `stages/`，但本仓库没有这个约定，所以不沿用。

文件名用瑜东的阶段号，和原型 `stages/` 是同一套编号。这样每个文件就是瑜东一步的位置，以后的分支只替换对应文件的内容，不用改名。你看文件名，也就知道它对应瑜东的哪一步。

Step 2.5 选模板在瑜东流程里没有对应的步骤，所以文件名不带编号。到做 a10 大纲的分支时，再决定它是并进 a10 还是保留。

文件里的标题和步骤号这次都不改，比如 Step 1.5、"Step 2 item 20"，因为模板和其他步骤引用了这些编号。改编号留到替换内容的分支里一起做。

## 4. 两个技术点

### 4.1 路径变量只在 SKILL.md 里生效

Claude Code 只在 skill 的 Markdown 正文和 `allowed-tools` 里替换 `${CLAUDE_SKILL_DIR}`，文档没有说会替换辅助文件。所以搬出去的文件里如果还写着 `${CLAUDE_SKILL_DIR}`，Claude 读到的就是这串字面文字。

做法：搬出去的文件改成相对 skill 文件夹的路径，这也是 Agent Skills 规范的写法。SKILL.md 里写明 skill 文件夹在哪里，见第 5 节。受影响的只有三个文件，这也是这次唯一改动的正文：

| 文件 | 现在 | 改成 |
|---|---|---|
| a05-demand-facets.md | `${CLAUDE_SKILL_DIR}/templates/keyword-research.md` 等两处 | `templates/keyword-research.md` 等 |
| template-recommendation.md | `${CLAUDE_SKILL_DIR}/../blog/references/content-templates.md` 等两处 | `../blog/references/content-templates.md` 等 |
| a10-generate-brief.md | `${CLAUDE_SKILL_DIR}/templates/brief-template.md`、`${CLAUDE_SKILL_DIR}/../blog/templates/[type].md` | `templates/brief-template.md`、`../blog/templates/[type].md` |

### 4.2 所有文件都从 SKILL.md 一步找到

官方建议，每个文件都能从 SKILL.md 直接找到。隔了一层的文件，Claude 有时只读开头一部分。

做法：步骤顺序表多加一列"这一步还要读的文件"，把每一步用到的模板和 blog 共享参考文件都列出来。这样每个文件都只隔 SKILL.md 一层。

## 5. 新 Workflow 段草稿

替换现在的 `## Workflow` 标题和下面的 Step 1 到 Step 5，Step 6 原样接在后面。

```markdown
## Workflow

Do the steps in the order of the table. Before you start a step, read
its step file completely. Do not read a step file before you start
that step.

Paths in the step files are relative to this skill folder:
`${CLAUDE_SKILL_DIR}`.

| Step | Step file | Other files that the step reads |
|---|---|---|
| Step 1: Topic Intake | `${CLAUDE_SKILL_DIR}/references/a01-topic-intake.md` | None |
| Step 1.5: SERP Intent Gate | `${CLAUDE_SKILL_DIR}/references/a03-serp-intent-gate.md` | None |
| Step 2: Keywords to Demand Facets | `${CLAUDE_SKILL_DIR}/references/a05-demand-facets.md` | `${CLAUDE_SKILL_DIR}/templates/keyword-research.md`, `${CLAUDE_SKILL_DIR}/templates/demand-facets.md` |
| Step 2.5: Template Recommendation | `${CLAUDE_SKILL_DIR}/references/template-recommendation.md` | `${CLAUDE_SKILL_DIR}/../blog/references/content-templates.md`, `${CLAUDE_SKILL_DIR}/../blog/templates/[type].md` |
| Step 3: Competitive Analysis | `${CLAUDE_SKILL_DIR}/references/a06-competitive-analysis.md` | None |
| Step 4: Statistics Research | `${CLAUDE_SKILL_DIR}/references/a07-statistics-research.md` | None |
| Step 5: Generate the Brief | `${CLAUDE_SKILL_DIR}/references/a10-generate-brief.md` | `${CLAUDE_SKILL_DIR}/templates/brief-template.md`, `${CLAUDE_SKILL_DIR}/../blog/templates/[type].md` |
```

"Do not read a step file before you start that step" 学的是原型 SKILL.md "只读当前阶段，后面的阶段到时再读"。好处是每一步开始时，Claude 手上只有这一步的说明，不会把别的步骤的规则混进来。

## 6. 路线图（这个分支不做）

阶段 A 按瑜东的做法，暂定这样分支。每个分支开始前，再单独写开发文档、单独确认。

| 顺序 | 分支（暂定名） | 做什么 | 瑜东步骤 |
|---|---|---|---|
| 1 | refactor/blog-brief-step-files | 本分支：拆文件，不改行为 | 无 |
| 2 | feat/blog-brief-run-folder | 每篇简报一个文件夹 `briefs/<slug>/`，每步结果存进去，加进度文件，中断后能续跑 | 阶段门要求的"产物落盘" |
| 3 | feat/blog-brief-a01-task-brief | Step 1 换成任务单：业务边界、支撑的商业页、客户事实和缺失项 | 01 |
| 4 | feat/blog-brief-a05-business-fit | 需求面读任务单，按业务相关性筛选和定去留 | 05 |
| 5 | feat/blog-brief-a06-gap-list | Step 3 换成竞品差距清单 | 06 |
| 6 | feat/blog-brief-a07-evidence-table | Step 4 换成证据表：问题对证据、原文摘句、采用状态；加信息增量最小版（2026-10-23 拆分：信息增量先在 feat/blog-brief-a08-information-gain 单独做，见 `docs/plans/2026-10-23-blog-brief-a08-information-gain.md`） | 07、08 |
| 7 | feat/blog-brief-a10-outline | Step 5 换成大纲 v1、自审、v2；决定 Step 2.5 的去留 | 10 |
| 8 | feat/blog-brief-gate-a-to-b | 动笔前的 A→B 阶段门 | 阶段门 |
| 9 | feat/blog-write-use-brief | `/blog write` 直接用大纲和证据表，不再重做研究和大纲 | 路线二第三段 |

下面三步暂缓，到时单独讨论。原型也还没做这三步。

- 02 先复用再研究：要先有知识卡。
- 04 竞争机会：要 Ahrefs 或 DataForSEO Labs 的难度数据。
- 09 语义基准：要 NEURONwriter。

另外，a05 里去重、分组、排序这些每次结果都应该一样的操作，适合改成 Python 脚本。这件事单独一个分支，放在第 4 个分支前后。

## 7. 验证

1. 文字没变。每个新文件和旧 SKILL.md 的对应段落逐行比较，只允许第 4.1 节列出的路径不同。例如 Step 1.5 是旧文件第 58 到 74 行：

   ```bash
   diff <(git show main:skills/blog-brief/SKILL.md | sed -n '58,74p') skills/blog-brief/references/a03-serp-intent-gate.md
   ```

   另外用 `git diff main --color-moved=zebra -- skills/blog-brief/` 看整体，搬走的行和搬来的行会用同一种颜色标出。

2. 仓库检查全部通过：`python3 -m pytest tests/`、`python3 scripts/validate_skills.py --root .`、`python3 scripts/lint_prose.py`、`python3 scripts/consistency_check.py`。`claude plugin validate .` 只允许出现插件名 `claude-blog` 被保留这一条已知错误。

3. 真实跑一次。在 `claude-seo-playground` 里用 "2k dispensing problems" 跑完整的 brief，方法和 10 月 22 日的测试一样：子代理读这个分支的 SKILL.md，照着做。看三件事：
   - 是否按表的顺序读 step 文件；
   - 是否没有提前读后面步骤的文件；
   - 产物文件和栏目是否和 10 月 22 日那次一样。

   实时 SERP 每次结果不同，所以只比结构，不比数值。接口费用和 10 月 22 日那次相同。

## 8. 要同步改的地方

- `tests/test_release_safeguards.py` 第 184 行读 SKILL.md，检查里面有 `only when the user supplies supporting methodology`。这句话在 Step 5，搬家后在 `references/a10-generate-brief.md`。改成读这个文件，断言本身不变。
- `CLAUDE.md` 目录树里的 blog-brief 一项，改成 SKILL.md、references（7 个步骤文件）、templates（3 个输出模板）。
- `CHANGELOG.md` 不改。它是上游写给使用者的版本说明，这次改动使用者看不出来。
- 合并后在 `docs/FORK-DEVLOG.md` 加一条。日志现在只记到 006，PR #7 和 #9 还没记，可以一起补。

## 9. 风险

- Claude 可能不读 step 文件，凭印象做。SKILL.md 写明了"开始一步前完整读它的文件"，第 7 节第 3 项的真实测试会检查它有没有读。
- 以后从上游同步 blog-brief 时会冲突。上游的改动都在一个 SKILL.md 里，要手工搬到对应的 step 文件。本 fork 目前没有同步上游的计划。

## 10. 提交拆分

1. `docs(blog-brief): add design for splitting steps into files`：本文档。
2. `refactor(blog-brief): move each step into its own file`：SKILL.md、7 个 step 文件、测试路径、CLAUDE.md 目录树。分成两个提交的话，中间那个提交测试会失败，所以放在一起。

## 出处

- Agent Skills 规范（`references/` 目录的用途、用相对 skill 根目录的路径、引用只隔一层）：https://agentskills.io/specification
- Claude 官方 Skill 最佳实践（流程长了就拆成文件、引用只隔一层、SKILL.md 不超过 500 行）：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code skills 文档（`${CLAUDE_SKILL_DIR}` 只在 skill 正文和 `allowed-tools` 里替换）：https://code.claude.com/docs/en/skills
- Google 代码评审规范 Small CLs，"Separate Out Refactorings" 一节：https://google.github.io/eng-practices/review/developer/small-cls.html
- 原型的阶段登记表和读入规则：`/Users/Kai/个人项目/瑜东SEO/.claude/skills/yudong-blog-workflow/pipeline.md`、同目录 `SKILL.md`
