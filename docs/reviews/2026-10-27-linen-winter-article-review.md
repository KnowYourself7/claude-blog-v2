# 冬季亚麻文章最终版：对照 COOFANDY 推广要求和瑜东工作流

- 日期：2026-10-27。
- 评的文章：claude-seo-playground/drafts-v2/can-you-wear-linen-in-winter/can-you-wear-linen-in-winter.md。这是之前三方对比里的文章 C，2026-10-26 生成，1,892 词。
- 生成方式：feat/blog-brief-positioning 分支的 blog-brief 出简报，原版 blog-write 写作。简报的 Content Parameters 由用户手工改过。这次运行早于 #25，所以任务单还没有 Role 行。
- 对照依据：
  1. COOFANDY 推广要求：测试场的 BRAND.md、VOICE.md，以及这篇任务单的 Page 表和 Delivery 表。
  2. 瑜东工作流：`docs/yudong/` 第 01、02、05、06、07、09 课。
- 只读评估。没有改文章，也没有改 skill 文件。

## 结论

| 问题 | 结论 |
|---|---|
| 合 COOFANDY 推广要求吗 | 合规红线全过，写法合 VOICE.md。推广作用只发挥了一半：和自家旧文撞题，只带一个集合页，没有链 pillar，自家产品参数是空白 |
| 合瑜东工作流吗 | 正文写法基本合 B·12 四段式和三条护栏。缺口在两头：开工前没查站内覆盖（A·01），收尾时交付合同其实没过（C·17） |
| 下一步先做什么 | 任务单收同站页面清单，先用它查撞题。理由见第 3 节 |

## 1. 对照 COOFANDY 推广要求

### 1.1 符合的

| 要求和出处 | 文章里的做法 |
|---|---|
| 品牌名全大写，署名 The COOFANDY Style Desk（BRAND.md 的 Editorial Rules 和 Required disclosures） | 都做到了 |
| 不以 Style Desk 的名义声称亲测（Never do） | 两处写明穿搭是示例、没有试穿（第 61、203 行） |
| 禁用词、涤纶、贬低竞品、质量宣称（Taboo phrases 和 Never do） | 全文没有命中 |
| 先给结论再给条件（Always do，VOICE 的 Body patterns） | 标题、导语、第一个 H2 都用 "Yes, with conditions" |
| 摘要框叫 Key Takeaways，每句不超过 25 词（VOICE 的 Lexical rules） | 都做到了。审稿人数过：平均 13.6 词，最长 25 词 |
| 题材在范围内（Topic Scope 的「季节换装：秋冬层搭」） | 是 |
| 回应读者痛点「秋冬层搭显臃肿，高领毛衣怎么配 Blazer」（Audience 的 Active problems） | 节日派对那一行写了高领毛衣加亚麻西装外套 |
| 品牌观点「按场合解决，不堆单品，一套 Set 更有用」（Distinctive POV） | 6 个场合的穿搭表，加上套装集合页 |
| 支撑页（任务单的 Page this post supports） | mens-linen-sets 链了 2 次：穿搭表后面一次，结尾一次 |

### 1.2 不符合或有风险的，按严重程度排

| # | 问题 | 依据 | 从哪一步来 |
|---|---|---|---|
| 1 | 和自家旧文撞题。站内已有 "Can Men Wear Linen in Winter? A Practical Layering Guide"，网址 /blogs/inspire-me/can-men-wear-linen-in-winter-mens-guide，lastmod 2026-09-28。新文上线会和它抢同一个搜索词 | coofandy-posts.csv。三轮审稿都提了，写作时用户选了「只记录」 | 简报不查站内已有文章 |
| 2 | 定位只兑现一半。任务单的 Positioning 要把读者带到亚麻单品，以及盖在外面的秋冬层搭单品。正文里的毛衣、开衫、大衣、靴子一个都没链 | 任务单的 Delivery 表 | 任务单只有一个 Page 格子，写作拿不到别的页面 |
| 3 | 没链 pillar。站内有 The Complete Men's Linen Guide 2026（/blogs/guides/the-complete-mens-linen-guide-2026-shirts-pants-sets-and-everything-in-between）。讲层搭的同站文章也没链，例如 turtleneck-under-a-blazer-the-complete-formula、best-mens-sweaters-for-fall-and-winter、mens-fall-outfits-the-complete-2026-style-guide | coofandy-posts.csv。简报的 Pillar connection 是 missing | 同上 |
| 4 | 可能和货盘打架，需确认。文章建议长裤选 190-260 GSM、选亚麻羊毛混纺，还引用了「低于 190 GSM 的亚麻裤一季就鼓膝」。没人核对过 COOFANDY 卖不卖混纺、自家亚麻裤多重。如果自家裤子更轻，这句话等于劝读者别买 | BRAND.md：面料成分只引用产品页或 products.md | 简报的 First-Party Evidence 是 none supplied。增量单 I4 写明没有来源给出 COOFANDY 亚麻的克重 |
| 5 | 标题去掉了 "Men's"。简报推荐的标题带 "(Men's Guide)"，VOICE 的标题例子也是这个格式。这个词的排名页多是女装（增量单 I1），男装限定是差异点 | 简报的 Recommended Title，VOICE 的 Headline patterns | 写作时为了把 64 个字符缩到 60 以内删掉了，用户选的「缩短」。删别的词也能缩短 |
| 6 | 没有实拍图或产品图，首图是文字卡 | 审稿 Low 项 | 品牌没有提供图库 |
| 7 | 小问题：schema 作者标成 Person；NOAA 链接是数据接口生成的 PDF，DOE 链接是邮件公告页；「亚麻比棉保暖差」重复了 3 到 5 次 | review.md | 作者类型是渲染器写死的，其余来自写作 |

## 2. 对照瑜东工作流

### 2.1 阶段 A：简报

| 瑜东步骤 | 这次的情况 | 结论 |
|---|---|---|
| A·01 任务单四组输入 (p.107-108) | 主题与读者、客户与品牌、执行与交付三组有了。页面与转化只有支撑页和读者下一步，缺「站内已有文章是否覆盖过」，也缺支柱页和锚文本清单（第 01 课第 21、32 行） | 部分符合。漏掉的正是造成撞题的那一项 |
| A·02 先复用再补研究 | 没有知识卡库，没做 | 没有 |
| 第 02 课的「进入方式：新建还是更新旧文」 | 没判断，默认新建 | 没有 |
| A·03 到 A·08 | 搜索意图、需求面、竞品、证据计划、信息增量都落盘了 | 符合 |
| A·09 语义基准 | 还没做 | 没有 |
| A·10 大纲 V2 的「站内关系」（第 05 课第 97 行） | V2 没写和同站文章的边界 | 没有 |

### 2.2 阶段 B：原版 blog-write

| 瑜东步骤 | 这次的情况 | 结论 |
|---|---|---|
| B·12 四段式 (p.130) | 每个 H2 先给答案，条件写得足，多数节末给了下一步（内链或动作） | 基本符合 |
| B·12 场景标来源，不虚构亲历 | 穿搭写明是示例，不是试穿 | 符合 |
| B·12 字数是结果 | 1,892 词，简报估 1,500 词，没有凑字 | 符合 |
| B·13 决策表 (p.132) | 三张表，都交代了条件和来源 | 符合 |
| B·13 FAQ 不重复正文 | blazer 和白色亚麻两条 FAQ 基本在重复正文（审稿 Medium 项） | 不符合 |
| B·13 内链连支柱页 | 没链 pillar | 不符合 |
| B·13 文末汇总参考资料 | 没有参考资料列表。About 一节只说了来源类型 | 不符合 |
| B·14 信息增量落实 | 增量单的 I1 到 I4 都写进了正文 | 符合 |
| B·14 语义覆盖 | 没有 A·09，无从对照 | 没有 |
| B·15、B·16 自然化 | 原版没有这一段 | 没有。已记在 2026-10-25 的阶段 B 对照文档 |

### 2.3 阶段 C：交付

| 瑜东步骤 | 这次的情况 | 结论 |
|---|---|---|
| C·17 改稿后旧的通过作废 (p.140) | 审稿用 nonce 绑定文件。三轮审稿分别是 80、86、90 分，每次改稿都重审 | 符合 |
| C·17 查「是否与站内既有页面争抢同一意图」 | 审稿查出来了，但不计分，文章照样放行 | 发现了，没处理 |
| C·17 有警告就写 WARN (p.141) | preflight-report.json 是 `blocked: true`。本机没有浏览器，出不了 PDF，Gate 2、3、5 都没过，外链检查没有跑 | 按瑜东的口径，这篇是没通过，不是完成 |
| C·18 配图冷读 | 只有文字封面和一张条形图。图表在手机上字太小（审稿 Low 项） | 部分符合 |

## 3. 二开建议，按先后

| 顺序 | 做什么 | 为什么排这里 |
|---|---|---|
| 1 | 任务单收同站页面清单。Step 1 用它查撞题：站内已有同一读者任务的文章，就停下来问用户「新建、更新旧文，还是换角度」 | 撞题是这篇唯一会让发布变成净损失的问题。依据第 01 课 p.107 和第 02 课的「进入方式」。改动只在 Step 1 和任务单模板 |
| 2 | 大纲按清单安排内链：pillar、同站相关文章、层搭单品集合页，放进需要它们的 H2 | 解决 1.2 的第 2、3 条。已有计划 `docs/plans/2026-10-24-blog-brief-internal-link-pages.md`，要按新任务单改写。它的「不做」表把撞题检查推到了以后，第 1 项做完后要删掉那一行 |
| 3 | Step 6 证据计划读任务单。按交付物取证，把自家产品参数（克重、成分、有没有混纺）列为要找的证据。找不到就标需确认，不写会和货盘冲突的阈值 | 解决 1.2 的第 4 条。这也是之前定好的第二个 brief 分支 |
| 4 | 再评估 blog-write 计划：FAQ 去重、文末参考资料、标题保留简报里的限定词 | 原版写作表现不差，这几条都是小改，排在简报之后 |
| 不算二开 | 装上 patchright 需要的 chromium_headless_shell-1243，让 Gate 2、3、5 能跑 | 这是环境问题，不改代码。不装的话，每次实跑交付合同都会是 blocked |

这篇文章本身：发布前要先定和旧文的关系。用这篇的内容更新旧文的网址，比新开一个网址更合两份要求。
