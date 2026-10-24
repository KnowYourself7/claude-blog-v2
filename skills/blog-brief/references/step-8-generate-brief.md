### Step 8: Generate the Brief

#### Goal

Turn the research into the brief that `/blog write` reads.

#### Inputs

- `templates/brief-template.md`: the output template. Each
  placeholder says where its content comes from.
- `briefs/[slug]-search-intent.md`: the reader task and the decision.
- `briefs/[slug]-demand-facets.md`: the kept facets, the questions
  that the post must answer.
- `briefs/[slug]-evidence-plan.md`: the adopted sources, for
  Statistics to Include and the charts of the Visual Element Plan.
- `briefs/[slug]-information-gain.md`: the gains, and the evidence for
  each gain.

#### Rules

- Every kept facet gets at least one H2. Write the facet IDs in each
  H2.
- Use only the gains in the information gain file. Do not add gains of
  your own.
- From the Gains table, take only This post adds and Evidence into the
  Content Outline. Do not name a ranking page, a rank, or a gap there.
- Include first-hand insight, a case study, or test results
  only when the user supplies supporting methodology, evidence, and
  results. Otherwise propose sourced analysis, without a first-hand
  claim.

#### Steps

1. Fill `templates/brief-template.md` in its order.

#### Outputs

- The filled brief. Step 9 saves it as `briefs/[slug]-brief.md`.

#### Check

- Every kept facet appears in at least one H2.
- Every gain of the information gain file appears in Information Gain
  Opportunities.
- No line of the Content Outline names a ranking page, a rank, or a
  gap.
- No first-hand claim lacks the method, the evidence, and the results
  of the user.
- Every placeholder of the template is filled.
