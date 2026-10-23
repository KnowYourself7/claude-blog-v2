### Step 1: Topic Intake

#### Goal

Turn what the user wrote into a task brief.

#### Inputs

- `templates/task-brief.md`: the output template.

#### Rules

- Write `missing` in every cell that the user did not give.
- Do not open the website. Do not infer a brand fact.
- Do not ask for the search intent. Step 2 reads it from the live
  SERP.

#### Steps

1. Topic: the focus keyword, the market, and the decision that the
   reader is making. If the user names a market, write its codes and
   `given`. If not, write 2840 / en and `default`. You can infer the
   reader decision from the keyword.
2. Business: the brand, the domain, what it sells, and what it does
   not sell or must not claim.
3. Page: the page that this post supports, and the next step for the
   reader.

#### Outputs

- `briefs/[slug]-task-brief.md`

#### Check

- Every cell has a value or `missing`.
- No brand fact comes from outside the words of the user.
- The market has two codes and says `given` or `default`.
