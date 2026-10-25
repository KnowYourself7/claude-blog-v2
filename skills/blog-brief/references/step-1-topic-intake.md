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
2. Slug: make the slug from the focus keyword. The slug starts the
   name of every output file.
   - Change the letters to lowercase. Change each accented letter to
     its plain letter, for example `é` to `e`.
   - Delete each character that is not `a` to `z`, `0` to `9`, a
     space, or a hyphen. For example, `men's` becomes `mens`.
   - Replace each run of spaces and hyphens with one hyphen. Delete the
     hyphens at the start and at the end.
   - If nothing stays, stop and ask the user for an English slug.

   For example, `can you wear linen in winter` gives
   `can-you-wear-linen-in-winter`.
3. Business: the brand, the domain, what it sells, and what it does
   not sell or must not claim.
4. Page: the page that this post supports, and the next step for the
   reader.

#### Outputs

- `briefs/[slug]-task-brief.md`

#### Check

- Every cell has a value or `missing`.
- No brand fact comes from outside the words of the user.
- The market has two codes and says `given` or `default`.
- The slug has only `a` to `z`, `0` to `9`, and single hyphens. The
  file name starts with it.
