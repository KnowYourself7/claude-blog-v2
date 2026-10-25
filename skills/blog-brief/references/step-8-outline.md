### Step 8: Outline

#### Goal

Turn the research files into an answer plan for the post, in two
versions. An answer plan gives each H2 a reader question, an answer,
and the evidence for the answer.

#### Inputs

- `templates/outline.md`: the output template.
- `briefs/[slug]-search-intent.md`: the Reader Task, for the review of
  the order.
- `briefs/[slug]-task-brief.md`: the Reader decision, the Page this
  post supports, the Reader next step, and the Does not sell or claim
  row.
- `briefs/[slug]-demand-facets.md`: the Kept Facets, the questions
  that the post must answer.
- `briefs/[slug]-evidence-plan.md`: the Facet and Weak columns of the
  Questions table. The #, Question, Finding, Status, and Chart columns
  of the Sources table.
- `briefs/[slug]-information-gain.md`: the gain IDs and their Use, the
  Evidence requirement of each gain, and First-Party Evidence.

#### Rules

- Use only the kept facets, the `adopted` sources, and the gains of the
  information gain file. Do not add facts, sources, or gains of your
  own.
- Cite a source by its #. Do not copy its numbers into the outline.
- Do not copy the cells of the information gain file. Say in your own
  words what an H2 builds for a gain.
- Do not name a ranking page, a rank, or a gap.
- Do not write a claim that the Does not sell or claim row forbids.
- If evidence is missing for a claim or a part of it, write a narrower
  claim. If the Evidence requirement of a gain has one, use it. Write
  it as the thing that the post says, not as what the sources lack. Do
  not keep the claim and add a disclaimer.
- Include first-hand insight, a case study, or test results
  only when the user supplies supporting methodology, evidence, and
  results. Otherwise propose sourced analysis, without a first-hand
  claim.
- Write each line of Outline V1 and V2 in one or two sentences of 25
  words at most. Do not count the label or the question of a line. The
  outline is a plan, not a long prompt for the writer.

#### Steps

1. Fill Outline V1. For each H2, write the facet IDs that it answers,
   the gain IDs that it delivers, and one core answer. A core answer is
   the conclusion that the reader takes from the H2.
2. In FAQ, write the questions inside the kept facets that need a
   short answer of their own. A facet in the FAQ still needs an H2.
3. Fill Calculator. If no adopted source gives a formula, write
   `none`. If a source gives one, decide if a calculator helps the
   Reader decision, and write the reason for the choice. A main
   calculator is the core tool of the page. A section calculator sits
   in one H2.
4. Review V1. Ask the question of each check, and write the finding in
   its row of the Self-Review table.

   | Check | Question |
   |-------|----------|
   | Intent | Does the order match the Reader Task? Does the first H2 answer the main question, or does it explain a concept first? |
   | Questions | Does each kept facet have an H2? Do two H2s answer the same question? |
   | Evidence | Does each core answer have an adopted source or a narrower claim? |
   | Gains | Does an H2 deliver each gain? |

5. Fill the Changes table, one row for each change from V1 to V2. For
   example, merge two H2s that answer the same question, or add an H2
   for a missing facet. Then write the change IDs in the Changes column
   of the Self-Review table.
6. Fill Outline V2. Apply the changes to V1, and fill the five lines of
   each H2.
   - In Evidence, write the source # of each adopted source. If the
     Evidence requirement of a gain marks a source `estimated` or
     `example`, write that word after its #.
   - In Components, put the tables, charts, images, cases, internal
     links, and calculators that the H2 needs. Put the decision
     framework and a kept calculator in the H2 that holds them.
   - Use a chart only for a source with `yes` in Chart. Use a case only
     from an adopted source or from First-Party Evidence.
   - Link only to the Page this post supports. If it is `missing`,
     plan no link.
7. Fill Still Open at the end of V2.

#### Outputs

- `briefs/[slug]-outline.md`

#### Check

- Every kept facet is in at least one H2 of Outline V2. Every gain ID
  is in at least one Gains line.
- Every Answer line gives a conclusion for the reader. No two Answer
  lines have the same text. No line has more than two sentences or a
  sentence over 25 words.
- Every source # is an `adopted` source. No line copies a number of a
  source. Every claim with missing evidence has a narrower claim.
- Every Self-Review row has a finding. Still Open lists claims, or
  says `none`.
- No line names a ranking page, a rank, or a gap. No first-hand claim
  lacks the method, the evidence, and the results of the user. Every
  internal link goes to the Page this post supports.
