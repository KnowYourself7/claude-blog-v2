### Step 1: Topic Intake

#### Goal

Turn the words of the user into a task brief. The task brief is a file
with four tables. It says who the post is for, what the post does for
the brand, and what the reader gets from it.

#### Inputs

- `templates/task-brief.md`: the output template.
- The `BRAND.md` that SKILL.md loaded: take the brand facts and the
  Audience section from it. If there is no `BRAND.md`, skip this input.

#### Rules

- A brand fact is a fact about the business, for example what it sells.
  Take the brand facts and the Reader row only from the words of the
  user and from `BRAND.md`. If both give a value, use the words of the
  user.
- Do not open the website of the brand. Do not infer a brand fact.
- A draft is a Delivery value that you write because the user did not
  give it. A draft is not a brand fact. The user accepts or changes it
  in item 6.
- Write only about this post in the Positioning row. Do not copy the
  brand positioning of `BRAND.md` into it.
- Do not ask the user for the search intent. Step 2, SERP Intent Gate,
  gets it from the live SERP.

#### Steps

1. Fill the Topic table. Write the focus keyword, the market, the
   Reader decision, and the Reader.
   - If the user names a market, write its DataForSEO location code,
     its language code, and `given`.
   - If the user names no market, write 2840 / en and `default`. 2840
     / en is the United States in English.
   - The Reader decision is the decision that the reader is making. You
     can infer it from the focus keyword.
   - In the Reader row, write the main readers and what they know. Use
     the language of the post.
2. Make the slug from the focus keyword, and write it in the Slug row.
   The slug is the short name of the post. The name of every output
   file starts with it.
   - Change the letters to lowercase. Change each accented letter to
     its plain letter, for example `é` to `e`.
   - Delete each character that is not `a` to `z`, `0` to `9`, a
     space, or a hyphen. For example, `men's` becomes `mens`.
   - Replace each sequence of spaces and hyphens with one hyphen.
     Delete the hyphens at the start and at the end.
   - If no character remains, stop. Ask the user for an English slug.

   For example, `can you wear linen in winter` gives
   `can-you-wear-linen-in-winter`.
3. Fill the Business table. Write the brand, the domain, what the brand
   sells, and what the brand does not sell or must not claim.
4. Fill the Page table. Write the page that this post supports, and the
   action that the post leads the reader to.
5. Fill the Delivery table. Use these definitions:

   | Row | What it says | Example |
   |---|---|---|
   | Positioning | The type of post, the reader, and the job of the post for the brand | A troubleshooting post for buyers of dispensing supplies leads them to the matching products. |
   | Role | The place of the post in the site: `pillar`, `cluster`, or `standalone` | `cluster` |
   | Deliverable | The main thing that the reader can take from the post and use, and its size | A table of 7 faults gives the symptom, the cause, and the part to examine. |

   A `pillar` is the core page of a topic. The cluster posts of the
   topic link to it. A `cluster` post answers one question of a topic
   and links to its pillar. A `standalone` post is neither.
   - If the user did not give a Delivery value, write a draft. Base it
     on the Reader decision, the Reader row, and the Sells row.
   - If you draft the Role, write `standalone`.
6. If a Delivery value starts with `draft:`, or a Page value is only
   `missing`, save the task brief. Then stop and ask the user. A Page
   value of `missing, the user has none` does not stop the step.
   - In one message, show each draft and ask for each missing Page
     value.
   - Write the answers of the user into the task brief.
   - If the user rejects a draft and gives no new value, ask again.

#### Outputs

- `briefs/[slug]-task-brief.md`

#### Check

- Every cell has a value or `missing`. No Delivery value starts with
  `draft:`.
- No brand fact and no Reader row comes from outside the words of the
  user and `BRAND.md`.
- The Positioning names the type of post, the reader, and the job for
  the brand. A part without a source says `missing`. The Role is
  `pillar`, `cluster`, or `standalone`. The Deliverable names a thing
  that the reader can use.
- Each Delivery value and each Page value comes from the user. The user
  gave it at the start or answered it in item 6.
- The Market has two codes and `given` or `default`. The Slug has only
  `a` to `z`, `0` to `9`, and single hyphens. The name of the output
  file starts with the slug.
