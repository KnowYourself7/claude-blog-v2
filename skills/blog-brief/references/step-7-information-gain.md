### Step 7: Information Gain

#### Goal

Plan the gains of this post. A gain is a thing that the reader can
understand, decide, or do after this post, and not after the ranking
pages.

#### Inputs

- `templates/information-gain.md`: the output template.
- `briefs/[slug]-competitor-gaps.md`: Our Difference, the Gap List,
  and Format Advantage.
- `briefs/[slug]-task-brief.md`: the Does not sell or claim row.
- `briefs/[slug]-evidence-plan.md`: the adopted sources, the evidence
  for each gain, and the weak questions, where evidence is missing.
- The themes of `DISCOURSE.md` that SKILL.md loaded: more sources of
  gains. Without `DISCOURSE.md`, skip this input.

#### Rules

- A longer post, more fetched pages, or new wording is not a gain.
- Do not present the study or the data of another company as work of
  the user.
- A name for a framework or a checklist is not proof that it works.
- Do not write a gain that the Does not sell or claim row forbids.
- If no adopted source supports a gain, make the claim narrower. Do not
  keep the claim and add a disclaimer.

#### Steps

1. Read Our Difference. Plan the gain or the gains that make it real
   for the reader. For example, Our Difference "a diagnosis across
   parts" becomes the gain "a fault table across parts".
2. Read the Gap List and Format Advantage. Plan more gains from them.
   Each gain must let the reader understand, decide, or do more. For
   example, it shows how factors act together, it compares options
   with their conditions, or it gives steps that the reader can do.
3. Fill one row of the Gains table for each gain. In The ranking pages
   give, write in one line what the ranking pages give the reader now.
   In Use, write the structure of the gain in one line. End it with
   what the reader can understand, decide, or do, for example
   `symptom → cause → action → the part to check`. Do not restate a
   Finding of the evidence plan.
4. In Evidence requirement, write in one or two sentences the source #
   of the evidence plan, the owner of the data, and the type of the
   numbers. The owner is the person or the company that made the data.
   Name the owners in every row. Do not point to the sources of another
   row. If evidence is missing for the gain or a part of it, also write
   the narrower claim.

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

- At least one gain makes Our Difference real.
- Every row names a thing that the reader can use. Its Use ends with
  what the reader can understand, decide, or do.
- No cell names one ranking page, a rank, or a gap ID, or restates a
  Finding of the evidence plan.
- Every Evidence requirement names the owner and the type of each
  source. Where evidence is missing, it also has a narrower claim.
- First-Party Evidence names what the user supplied, or says
  `none supplied`.
