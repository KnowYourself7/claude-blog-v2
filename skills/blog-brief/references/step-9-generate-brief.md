### Step 9: Generate the Brief

Turn Outline V2 and the research files into the brief that
`/blog write` reads.

#### Tools

- The Readability Bands by Audience table and the default target line
  of `../blog/references/content-rules.md`.
- The Word count rows of the pillar table and the spoke table of
  `../blog-cluster/references/cluster-architecture.md`. A spoke is a
  cluster post.
- The Target Word Count or Target Length line of
  `../blog/templates/[template].md`, the content template of the Step
  5 note.

#### Inputs

- Outline V2, for the Content Outline and the title, from
  `briefs/[slug]-outline.md`.
- The market, the date, the Reader Task, the counts, and the decision,
  from `briefs/[slug]-search-intent.md`.
- The adopted sources, for Statistics to Include, from
  `briefs/[slug]-evidence-plan.md`.
- `briefs/[slug]-task-brief.md`: the Positioning, the Reader, the Role,
  and the Deliverable rows, which the brief copies into its own
  Positioning section. The Page this post supports, for Internal Link
  Architecture.
- First-Party Evidence, for the Experience line of E-E-A-T Signals,
  from `briefs/[slug]-information-gain.md`.
- The note of Step 5 in `briefs/[slug]-state.json`: the content
  template and the reason, for the Template section.
- The Readability target section of the `VOICE.md` that SKILL.md
  loaded, if any.

#### Actions

1. Fill `templates/brief-template.md` in its order. Where a
   placeholder names a source file, copy from it. Where it does not,
   write from Outline V2 and the task brief. Write `missing` for a
   fact that no file gives.
2. Reading level: if `VOICE.md` has a Readability target section,
   copy its Audience tier, Flesch Grade, and Flesch Ease. If not, take
   the band whose Audience matches the readers of the Reader row.
   Match the readers, not the topic. If the Reader row is `missing`,
   or matches no band, use the default target line under the table.
3. Word count: take the range from the Role. Role `pillar`: the pillar
   Word count row. Role `cluster`: the spoke Word count row. Role
   `standalone`: the template line. A need is one thing that the
   Reader Task says the searcher wants. One need: the low end of the
   range. Two or three needs: the middle. A whole-topic guide: the
   high end. This rule is a rule of this skill, not a Google standard.

#### Outputs

- The filled brief. Step 10 saves it as `briefs/[slug]-brief.md`.

#### Rules

- Copy Outline V2 into the Content Outline. Drop its Title line.
  Change nothing else.
- Do not guess a URL.
- Do not present the word count as a target or a Google rule. Google
  has no preferred word count.

#### Example

Coofandy, `can you wear linen in winter`:

- `VOICE.md` gives Audience tier consumer, Flesch Grade 6 to 8,
  Flesch Ease 60 to 80: copied as the Reading level.
- Role `cluster`: the spoke Word count row. Two needs in the Reader
  Task: the middle of the range, named as a planning estimate.
- Internal Link Architecture: the mens-linen-sets collection page
  only.

#### Check

- The Positioning section has the same four values as the task brief,
  and the Content Outline equals Outline V2 without its Title line.
- Every row of Statistics to Include is an `adopted` source, and the
  Content Outline cites its #.
- Internal Link Architecture names only the Page this post supports
  or `missing`. Word count and Reading level name their source. Every
  placeholder is filled.
