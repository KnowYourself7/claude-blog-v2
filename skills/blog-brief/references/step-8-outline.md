### Step 8: Outline

Write the outline, the last research file before the brief. Write V1,
review it line by line, and turn it into V2.

#### Tools

- The model. No API.

#### Inputs

- The Reader Task, for the order, from `briefs/[slug]-search-intent.md`.
- `briefs/[slug]-task-brief.md`: the Positioning, the Reader decision,
  the Page this post supports, the Reader next step, and the Does not
  sell or claim row.
- The questions that the post must answer: the Kept Facets of
  `briefs/[slug]-demand-facets.md`.
- From `briefs/[slug]-evidence-plan.md`: Facet and Weak of the
  Questions table. #, Question, Finding, Status, and Chart of the
  Sources table.
- From `briefs/[slug]-information-gain.md`: the gain IDs and their Use,
  the Evidence requirement of each gain, the Deliverable gain, and
  First-Party Evidence.

#### Actions

1. Fill Outline V1 of `templates/outline.md`, saved as
   `briefs/[slug]-outline.md`. Write the Title. For each H2, write the
   facet IDs that it answers, the gain IDs that it delivers, and one
   Answer, the conclusion that the reader takes. Write the Decision
   framework line: how the post leads to the Reader decision, and the
   H2 that holds it.
2. Fill FAQ: the questions inside kept facets that need a short answer
   of their own. A facet in the FAQ still needs an H2.
3. Fill Calculator. If no adopted source gives a formula, write
   `none`. If a formula helps the Reader decision, plan a calculator.
   Write `main` when it is the core tool of the page, or `section`
   when it sits in one H2. Write the source # of the formula and the
   reason.
4. Fill the Self-Review table: five rows, one Finding each.
   - Positioning: does one H2 list the Deliverable gain first in its
     Gains line and answer it? Does an H2 explain background that the
     reader of the Positioning does not need?
   - Intent: does the order match the Reader Task? Does the first H2
     answer the main question, or explain a concept first?
   - Questions: does each kept facet have an H2? Do two H2s answer the
     same question?
   - Evidence: does each Answer have an adopted source or a narrower
     claim?
   - Gains: does an H2 deliver each gain?
5. Fill the Changes table, one row per change from V1 to V2. Typical
   changes: merge two H2s on the same question. Add an H2 for a
   missing facet. Shorten or merge a background H2, and keep its
   facets in an H2. Write the
   change IDs in the Changes column of the Self-Review. If a narrower
   claim is still too strong for the Reader decision, or no narrower
   claim exists, list the claim for Still Open.
6. Fill Outline V2: apply the changes. For each H2, fill the five
   lines Facets, Answer, Evidence, Gains, and Components. Fill
   Introduction, FAQ, and Conclusion as the template says.
   - Evidence: the # of each adopted source. Write `estimated` or
     `example` after a # when the Evidence requirement says so.
   - Components: the tables, charts, images, cases, internal links,
     decision framework, and calculator of the H2, each with its task.
     A chart only for a source with Chart `yes`. A case only from an
     adopted source or First-Party Evidence. An internal link only to
     the Page this post supports. If that page is `missing`, no
     internal link. The decision framework and a kept calculator go in
     the H2 that holds them.
7. Fill Still Open: each claim of V2 that is still too strong or still
   lacks evidence, or `none`.

#### Outputs

- `briefs/[slug]-outline.md`

#### Rules

- Use only kept facets, `adopted` sources, and the gains of
  `briefs/[slug]-information-gain.md`. Add no facts, sources, or gains
  of your own. Cite a source by its #, never copy its numbers.
- Do not copy the cells of the information gain file. Say in your own
  words what an H2 builds for a gain. Do not name a ranking page, a
  rank, or a gap. Do not write a claim that Does not sell or claim
  forbids.
- If evidence is missing, write the narrower claim as what the post
  says, not as what the sources lack. If the Evidence requirement of
  the gain has one, use it. Do not keep the full claim with a
  disclaimer. Include first-hand insight, a case, or test results
  only when the user supplies supporting methodology, evidence, and
  results.
- Each line of V1 and V2 is one or two sentences, 25 words at most,
  the label and the question not counted. The outline is a plan, not
  a long prompt.

#### Example

Ebestron, Changes table:

- Quick table at the top: V1 9 rows, V2 12 rows, with sub-symptoms
  and parts.
- Fault 2 gets a selection example and question headings.
- Fault 5: no adopted source for force and viscosity, so its claim
  goes to Still Open.
- The site has 6 posts on selection, so V2 drops the selection guide
  H2.
- "Almost always a hardware cause" was too absolute. V2 keeps the
  other causes.
- Warning: a new version does not make every sentence right.

#### Check

- Every kept facet is in an H2 of V2. Every gain ID is in a Gains
  line. One H2 lists the Deliverable gain first.
- Every Answer is a conclusion, no two are the same, and no line has
  more than two sentences or a sentence over 25 words.
- Every source # is `adopted`, no number is copied, every Self-Review
  row has a Finding, and Still Open lists claims or `none`.
