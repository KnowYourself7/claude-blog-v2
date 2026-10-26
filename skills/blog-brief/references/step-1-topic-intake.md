### Step 1: Topic Intake

#### Goal

Turn what the user wrote into a task brief. The task brief says who
the post is for, what it does for the brand, and what the reader takes
away from it.

#### Inputs

- `templates/task-brief.md`: the output template.
- The `BRAND.md` that SKILL.md loaded: the brand facts and the Audience
  section. Without `BRAND.md`, skip this input.

#### Rules

- Take brand facts and the Reader row only from the words of the user
  and from `BRAND.md`. If both give a value, use the words of the user.
  Do not open the website. Do not infer a brand fact.
- A Delivery draft is not a brand fact. It is a proposal that the user
  accepts or changes in item 6.
- The Positioning row is about this post. Do not copy the brand
  positioning of `BRAND.md` into it.
- Do not ask for the search intent. Step 2 reads it from the live
  SERP.

#### Steps

1. Topic: the focus keyword, the market, the decision that the reader
   is making, and the reader. If the user names a market, write its
   codes and `given`. If not, write 2840 / en and `default`. You can
   infer the reader decision from the keyword. For the reader, write
   the main readers and what they know, in the language of the post.
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
5. Delivery: the positioning and the deliverable of the post.
   - The positioning names the type of post, the reader, and the job
     of the post for the brand. For example, a troubleshooting post
     for buyers of dispensing supplies leads them to the matching
     products.
   - The deliverable is the main thing that the reader takes from the
     post and can use, and its size. For example, a table of 7 faults
     gives the symptom, the cause, and the part to check.
   - If the user did not give one of them, draft it from the reader
     decision, the Reader row, and the Sells row.
6. If a Delivery row is a draft, or a Page row is exactly `missing`,
   save the task brief and stop. In one message, show each draft and
   ask for each missing Page row.
   - Write the answers of the user into the task brief.
   - If the user rejects a draft and gives no new value, ask again.

#### Outputs

- `briefs/[slug]-task-brief.md`

#### Check

- Every cell has a value or `missing`. No Delivery row is a draft.
- No brand fact and no Reader row comes from outside the words of the
  user and `BRAND.md`.
- The Positioning names the type of post, the reader, and the job for
  the brand, or says `missing` for a part without a source. The
  Deliverable names a thing that the reader can use.
- The user answered each draft and each missing Page row. Or the user
  gave all four values: the two Delivery rows and the two Page rows.
- The market has two codes and says `given` or `default`. The slug has
  only `a` to `z`, `0` to `9`, and single hyphens. The file name
  starts with it.
