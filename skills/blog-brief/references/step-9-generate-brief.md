### Step 9: Generate the Brief

#### Goal

Turn Outline V2 and the research files into the brief that
`/blog write` reads.

#### Inputs

- `templates/brief-template.md`: the output template. Each
  placeholder says where its content comes from.
- `briefs/[slug]-outline.md`: Outline V2, for the Content Outline and
  the title.
- `briefs/[slug]-search-intent.md`: the market, the date, the reader
  task, the counts, and the decision.
- `briefs/[slug]-evidence-plan.md`: the adopted sources, for
  Statistics to Include.
- `briefs/[slug]-task-brief.md`: the Positioning, the Reader, the Role,
  and the Deliverable rows, which the brief copies into its own
  Positioning section. The Page this post supports, for Internal Link
  Architecture.
- `briefs/[slug]-information-gain.md`: First-Party Evidence, for the
  Experience line of E-E-A-T Signals.
- `briefs/[slug]-state.json`: the note of Step 5, the template and the
  reason, for the Template section.
- The `VOICE.md` that SKILL.md loaded: its Readability target section,
  for the reading level. Without `VOICE.md`, skip this input.
- `../blog/references/content-rules.md`: the Readability Bands by
  Audience table and the default target under it, for the reading
  level.
- `../blog-cluster/references/cluster-architecture.md`: the Word count
  rows of the pillar table and of the spoke table, for the word count.
  A spoke is a cluster post.
- `../blog/templates/[template].md`: the Target Word Count or Target
  Length line of the template that Step 5 chose, for the word count.

#### Rules

- Copy Outline V2 into the Content Outline without change.
- Do not guess a URL.
- Do not present the word count as a target or as a Google rule.
  Google has no preferred word count.

#### Steps

1. Fill `templates/brief-template.md` in its order. Fill its Reading
   level line with item 2 and its Word count line with item 3.
2. Reading level: if `VOICE.md` gives a Readability target with values,
   copy its tier and its two ranges. If not, pick the band of the
   Readability Bands by Audience table whose Audience matches who the
   readers are in the Reader row. Match the readers, not the topic. If
   the Reader row is `missing` or matches no band, use the default
   target under the table.
3. Word count: take the range for the Role of the task brief.

   | Role | Range |
   |------|-------|
   | `pillar` | The pillar Word count row of `cluster-architecture.md` |
   | `cluster` | The spoke Word count row of `cluster-architecture.md` |
   | `standalone` | The Target Word Count or Target Length of the template |

   Count the needs in the Reader Task of the search intent file. For one
   need, use the low end. For two or three needs, use the middle. For a
   guide to a whole topic, use the high end. This rule is a rule of
   this skill, not a Google standard.

#### Outputs

- The filled brief. Step 10 saves it as `briefs/[slug]-brief.md`.

#### Check

- The Positioning section has the same four values as the task brief.
  The Content Outline is the same as Outline V2 of the outline file,
  without its Title line.
- Every source # in the Content Outline has a row in Statistics to
  Include. Every row is an adopted source that the Content Outline
  cites.
- Internal Link Architecture names only the Page this post supports,
  or `missing`.
- The Word count and the Reading level each name their source.
- Every placeholder of the template is filled.
