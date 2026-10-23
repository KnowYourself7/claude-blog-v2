### Step 7: Generate the Brief

#### Goal

Turn the research into the brief that `/blog write` reads.

#### Inputs

- `templates/brief-template.md`: the output template. Each
  placeholder says where its content comes from.
- `briefs/[slug]-search-intent.md`: the reader task and the decision.
- `briefs/[slug]-demand-facets.md`: the kept facets, the questions
  that the post must answer.
- `briefs/[slug]-competitor-gaps.md`: the gaps to close, and what this
  post does that the competitors do not.

#### Rules

- Every kept facet gets at least one H2. Write the facet IDs in each
  H2.
- Use only the gaps in the competitor gaps file. Do not add gaps of
  your own.
- Include first-hand insight, a case study, or test results
  only when the user supplies supporting methodology, evidence, and
  results. Otherwise propose sourced analysis, without a first-hand
  claim.

#### Steps

1. Fill `templates/brief-template.md` in its order.

#### Outputs

- The filled brief. Step 8 saves it as `briefs/[slug]-brief.md`.

#### Check

- Every kept facet appears in at least one H2.
- The three numbered items of Competitive Gaps come from the
  competitor gaps file.
- No first-hand claim lacks the method, the evidence, and the results
  of the user.
- Every placeholder of the template is filled.
