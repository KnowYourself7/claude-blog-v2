### Step 7: Information Gain

#### Goal

Plan the gains of this post. A gain is a thing that the reader can
understand, decide, or do after this post, and not after the ranking
pages.

#### Inputs

- `templates/information-gain.md`: the output template.
- `briefs/[slug]-competitor-gaps.md`: the Gap List and Format
  Advantage, what the ranking pages give and what they miss.
- `briefs/[slug]-task-brief.md`: the Does not sell or claim row.
- `briefs/[slug]-evidence-plan.md`: the adopted sources and the weak
  questions, the evidence for each gain.

#### Rules

- A longer post, more fetched pages, or new wording is not a gain.
- Do not present the study or the data of another company as work of
  the user.
- A name for a framework or a checklist is not proof that it works.
- Do not write a gain that the Does not sell or claim row forbids.
- If no adopted source supports a gain, make the claim narrower. Do not
  keep the claim and add a disclaimer.

#### Steps

1. Read the Gap List and Format Advantage. Plan the gains in the kinds
   of this table. A kind can have no gain, one gain, or more.

   | Kind | The ranking pages give | This post adds |
   |------|------------------------|----------------|
   | `factor interaction` | A list of factors. | How the factors act together. |
   | `conditional comparison` | A general definition or rule. | A comparison of the options or the concepts, with the conditions of each. |
   | `check steps` | Broad advice. | Steps that the reader can do. |

2. Fill one row of the Gains table for each gain. In From gap, write
   all gap IDs that lead to the gain. Write `format` for a gain from
   Format Advantage. A gap can lead to more than one gain. If a gap
   leads to no gain, do not write a row for it.
3. In This post adds, describe the thing by its structure, for example
   the columns of a table or the order of the steps. Then write what
   the reader can understand, decide, or do with it. Do not restate a
   finding or write a number from the evidence plan. Do not name a
   ranking page, a rank, or a gap ID.
4. In Evidence requirement, write each adopted source that the gain
   needs: the source #, the owner of the data, and the type of each
   number. The owner is the person or the company that made the data.
   If another site shows the data, name both. If no adopted source
   supports the gain or a part of it, write `none` and the narrower
   claim for that part.

   | Type | Meaning |
   |------|---------|
   | `measured` | Someone measured or counted it, for example in a test, a survey, or a product specification. |
   | `estimated` | Someone calculated it from other numbers or from a model. |
   | `example` | Someone made it up to show an idea. |

5. In First-Party Evidence, write the method, the evidence, and the
   results that the user supplied. If the user supplied none, write
   `none supplied`.

#### Outputs

- `briefs/[slug]-information-gain.md`

#### Check

- Every row has one kind of the table in step 1.
- Every This post adds cell says what the reader can understand,
  decide, or do. It names no ranking page, rank, or gap ID, and it
  has no finding or number from the evidence plan.
- Every Evidence requirement cell gives the source # and the owner of
  each source, and the type of each number. Every part of a gain
  without an adopted source has `none` and a narrower claim.
- First-Party Evidence names what the user supplied, or says
  `none supplied`.
