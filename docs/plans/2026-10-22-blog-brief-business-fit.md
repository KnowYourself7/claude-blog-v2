# 开发文档：blog-brief Step 1 任务单 + Step 3 按业务边界筛需求面

| 项目 | 内容 |
|---|---|
| 日期 | 2026-10-22 |
| 状态 | 已确认，实现中 |
| 分支 | feat/blog-brief-a06-gap-list（用户决定不另开分支，接在 710a6f2 之后） |
| 依据 | 瑜东 A·01「输入与任务范围」和 A·05「从关键词到需求面」，`docs/yudong-blog-workflow-小白讲解/01-开工前-任务单与先复用再补研究.md`（p.107 到 108）、`03-需求面与竞品拆解.md`（p.115 到 116） |
| 路线图位置 | `docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节的第 3、4 个分支，合在一起做 |
| 改动范围 | `skills/blog-brief/references/step-1-topic-intake.md`、新建 `skills/blog-brief/templates/task-brief.md`、`skills/blog-brief/references/step-3-demand-facets.md` 三处、`skills/blog-brief/templates/demand-facets.md` 一行、`skills/blog-brief/SKILL.md` 步骤表两行、`CLAUDE.md` 模板数 |

## 1. 为什么改

Step 1 现在只在对话里问三样东西（主题、读者、业务背景），什么都不写下来。Step 3 的筛词规则里有一个「business conflict」类别，但没有任何文件告诉它业务是什么，这个类别等于不存在；需求面模板里干脆写着「Business context: None was used」。

2026-10-22 用户用 `can you wear linen in winter` 给 Coofandy（男装，主打亚麻服装和套装）跑真实测试时指出：不按业务筛，需求面不准。这个词尤其明显，linen 既是亚麻衣服也是床品，女装和床品的问题会和男装混在一起进需求面。

瑜东的做法分两步。A·01 开工先填任务单，其中「业务边界」一格写客户卖什么、不能冒称什么（Ebestron 卖点胶耗材，不能冒称生产胶水，p.108）；「缺少的品牌事实需要核实，不能由模型补成客户能力或案例」（p.107）。A·05 筛词「先看与客户业务和本文读者任务的相关性，再看搜索量」，定去留时「低量但重要的面写明理由保留」（F6 滴漏合计 0 照样保留，因为和客户的胶枪直接相关，p.116）。

## 2. 改完的样子

Step 1 产出 `briefs/[slug]-task-brief.md`，对应瑜东的任务启动单。取 p.107 四组里这次用得上的三组：

| 瑜东任务单（p.107 到 108） | 产物里的段落 |
|---|---|
| 主题与读者 | Topic：焦点词、市场、读者正在做什么决定 |
| 客户与品牌 | Business：品牌名、域名、卖什么（产品线）、不卖什么或不能声称什么 |
| 页面与转化 | Page：这篇支撑哪个商业页、希望读者下一步做什么 |

用户没给的格子写 `missing`，不让模型推断品牌事实。第四组「执行与交付」（预算、授权、交付目标）这次不做。

Step 3 读任务单，改三处：

1. 筛词的「business conflict」有定义：关键词问的东西在 Business 段的边界之外，比如别的受众或别的品类。
2. 归完面、定去留前加一条：面在业务边界之外，进 Other Facets，理由 `outside business`；面直接对应 Business 段的一条产品线、但搜索量低或 `null` 的，保留并在 Reason kept 写明。
3. 需求面模板的 Business context 行改成链接任务单。

Step 7 不改。CTA 和支撑页怎么进简报，以后单独做。

完成标准：
1. 任务单每个格子有值或 `missing`，没有模型补的品牌事实。
2. Coofandy 这个例子里，女装、床品的词进 Removed Keywords 的 business conflict 类；对应的面进 Other Facets 写 outside business。
3. 男装套装这类和产品线直接相关的面，即使搜索量低也保留并写理由。

## 3. 新 Step 1 的顺序

1. 从用户的话里取焦点词、市场、读者在做什么决定；市场没说就用 2840 / en 并写明是默认。
2. 从用户的话里取品牌名、域名、产品线、不卖什么或不能声称什么、支撑的商业页、读者下一步。没给的写 `missing`。不打开官网，不猜。
3. 存为 `briefs/[slug]-task-brief.md`。

## 4. 和瑜东不同的地方

| 项 | 怎么处理 | 理由 |
|---|---|---|
| 第四组「执行与交付」 | 不做 | 预算、授权、交付目标在本仓库由别的机制管 |
| 站内已有覆盖、支柱页、锚文本 | 不做 | 要站点数据，路线图里另有安排 |
| 「一手资料」 | 不做 | 属于 A·07 证据计划 |
| 核实品牌事实 | 不核实，只记 `missing` | 瑜东要求「核实」，本仓库这一步没有工具；写 missing 比模型补强 |

## 5. Step 3 整篇重写（用户 2026-10-22 追加）

用户看过业务筛选的改动后说 Step 3 太啰嗦，要求按 writing-skills 的规范重写。做法：开头列四个要读的文件，规则三条，步骤从 22 条压到 17 条；模板正文已经说明的填表规则（池的分组、排序、平局、代表词取值）不在步骤里复述，只写「按模板填」。字数 1036 降到 751。

子代理对照新旧两版，找出压缩时丢掉的 5 条规则（去重忽略大小写、无 core_keyword 的分组、主关键词平局、面排序最后一级平局、Related Keywords 只做一次）、1 处顺序错误（Overview 调用挪到了剔除之前，会给后来删掉的词付费）、6 句可两读、4 处重复。处理：填表规则补进两个模板的说明段；Overview 挪回剔除之后成第 7 条；歧义句改成单一读法（市场取任务单的 location_code 和 language_code、自动补全只加问句和带新修饰词的建议、挂行先查是否复述焦点词、补词时不再调 Suggestions、先移出 outside business 再取前 9 个）；删掉和模板重复的「每个面至少一个 H2」和 SERP 复用的第二遍说明。

## 6. 提交拆分

1. `docs(blog-brief): add design for the task brief and business fit`
2. `feat(blog-brief): write a task brief in Step 1 and filter facets by business scope in Step 3`
3. `refactor(blog-brief): rewrite Step 3 in fewer words and move fill rules into the templates`

## 7. 验证

1. 仓库检查：pytest、validate_skills、lint_prose、consistency_check。
2. 真实跑在 `claude-seo-playground`：`can you wear linen in winter`，业务背景 coofandy.com 男装、亚麻服装和套装。看任务单的格子、Removed Keywords 里 business conflict 的词、Other Facets 里 outside business 的面、低量面的保留理由。

## 出处

- 瑜东 01 课：`docs/yudong-blog-workflow-小白讲解/01-开工前-任务单与先复用再补研究.md`
- 瑜东 03 课：`docs/yudong-blog-workflow-小白讲解/03-需求面与竞品拆解.md`
- 路线图：`docs/plans/2026-10-22-blog-brief-step-files.md` 第 6 节
