# blog-brief 各步骤：限定过窄检查

- 日期：2026-10-24。
- 范围：`skills/blog-brief/references/` 里的 9 个步骤文件，以及它们读的模板。
- 判断依据：官方 Skill authoring best practices 的 "Set appropriate degrees of freedom"。
  意思是按任务的脆弱程度决定写多细。调接口、跑脚本这类易错操作要写死。有多种合理做法的判断，给原则和原因。
- 原文：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- 内容依据：`docs/yudong/` 瑜东小白讲解，它是 blog-brief 唯一参考。

## 结论

大部分写死的地方是合理的（接口参数、脚本、防编造）。真正过窄的有 3 处，另有 2 处缺退路。

## A. 过窄，建议改

### A1. 内链只许一个目标

- 位置：`step-8-outline.md:73-74`（Link only to the Page this post supports）、
  `step-9-generate-brief.md:26`、`templates/brief-template.md:76`（`Other pages: missing` 写死）。
- 问题：用户就算给了同站博客清单，brief 也只能有 1 条内链。
- 课程依据：第 01 课资料盘点单列了「已有网站资料：产品网址清单、同站博客清单，用于选内链和避免重复」(p.110)；
  第 07 课说内链「连接支柱页和相关内容」。Step 1 的任务单没有收这一项。
- 建议：Step 1 任务单加一格「已有页面清单（missing 可）」；Step 8/9 改成
  「只链接用户给出的网址，没给就写 missing」。防编造网址的目的不变。

### A2. Step 5 只许按排名页格式选模板

- 位置：`step-5-template-recommendation.md:17-18`、Check 第 2 条。
- 问题一：和 Step 4 冲突。Step 4 专门写了 Format Advantage（竞品都没有的表格、步骤、工具），
  Step 5 却规定只能照排名页格式选。
- 问题二：没有退路。排名页格式各不相同，或竞品全部 `fetch failed` 时，Check 第 2 条无法通过。
- 建议：保留「默认跟排名页格式」；补两句：格式不一致时按 Reader Task 选并写明；
  Format Advantage 作为模板里的组件加入，不用来换模板。

### A3. 分类表是封闭的，没有「其他」出口

| 位置 | 现有分类 | 放不进去的真实例子 |
|---|---|---|
| `step-2-serp-intent-gate.md:40-45` 离题分类 | consumer / local / brand / other meaning | 新闻页、别国市场的页面 |
| `step-4-competitor-gaps.md:49-53` 差距类型 | unanswered / no decision / weak evidence | 信息过时；页面写给专业人士，读者是新手 |
| `step-7-information-gain.md:52-56` 数据类型 | measured / estimated / example | 没有数字的依据，例如一条标准条款 |

- 问题：规则写「给一个类」「写第一个适用的类」，碰到不适用时 Claude 只能硬塞。
- 好的样子已经在 Step 2 的标签表里：最后一行 `another kind, for example video or forum`。
- 建议：三张表各加一行 `other: [一句原因]`。

## B. 缺退路（规则只写了常见情况）

- B1. `step-3-demand-facets.md:47-50`：seed 2 写了「没有修饰词就跳过」，seed 3（更短的词）没写。
  焦点词本来就是 1 个词时（例如 `linen`）做不出来。建议：加「做不出更短的词就跳过 seed 3」。
- B2. `step-4-competitor-gaps.md:30-32`：只写了「少于 3 条就用这几条」，没写 0 条。
  用户在 Step 2 被拦下后选「照写」，就可能 0 条。建议：0 条时停下告诉用户，Step 4 到 Step 7 无竞品可比。

## C. 看起来窄，但建议保留

- 接口和脚本参数写死（Step 2、3、4、6）：低自由度、易错操作，符合官方做法。可各补一句原因，说明为什么不用 WebSearch。
- 数字门槛（30%、5、9、3、前 50 行）：是本 skill 的规则，触发后停下问用户，不替用户做决定。
- Step 8「只用 adopted 来源，不加自己的事实」：防编造的核心规则。代价是常识性操作步骤也要有来源。
  建议先保留，等真实测试里出现「常识步骤被删掉」再改。
- Step 9「原样复制 Outline V2」：低自由度是对的，防止最后一步改内容。

## D. 顺手发现（与过窄无关）

- `templates/competitor-gaps.md:3` 和 `templates/competitor-details.md:3` 的注释指向
  `step-5-competitor-gaps.md`，实际文件是 `step-4-competitor-gaps.md`（改编号时漏改）。
