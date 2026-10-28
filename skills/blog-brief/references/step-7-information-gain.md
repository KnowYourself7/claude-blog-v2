### Step 7: Information Gain

Plan what the post adds to what the ranking pages give, and the
evidence that each addition needs.

#### Tools

- The model. No API.

#### Inputs

- Our Difference, the Gap List, and Format Advantage, from
  `briefs/[slug]-competitor-gaps.md`.
- `briefs/[slug]-task-brief.md`: the Positioning row, the Deliverable
  row, the Does not sell or claim row, and First-party material.
- The `adopted` rows of the Sources table, and the Weak `yes` rows of
  the Questions table, from `briefs/[slug]-evidence-plan.md`.
- The themes of `DISCOURSE.md` that SKILL.md loaded, if any: more
  sources of gains.

#### Actions

1. Read the Deliverable of the task brief. Plan the gain that delivers
   it, and write its ID in Deliverable gain of
   `templates/information-gain.md`, saved as
   `briefs/[slug]-information-gain.md`. Its Use ends with what the
   reader can do. If a part of the gain has no source, for example the
   pieces of an outfit, write type `example` for that part. The type
   goes in its Evidence requirement (action 5).
2. Read Our Difference. Plan the gain or gains that make it real. For
   example, "a diagnosis across parts" becomes "a fault table across
   parts". The deliverable gain can be one of them. If a part of Our
   Difference does not serve the Positioning, plan no gain for it.
3. Plan more gains from the Gap List and Format Advantage. Each gain
   lets the reader understand, decide, or do more: how factors act
   together, options compared with their conditions, steps to follow.
4. Fill one Gains row per gain. The ranking pages give: one line on
   what the reader gets now. Gain: the thing, for example a fault
   table. Name: a short name for it. Use: its structure in one line,
   ending with what the reader can understand, decide, or do, for
   example `symptom → cause → action → the part to check`. Do not
   restate a Finding of the evidence plan.
5. Evidence requirement: write one or two sentences. Name the source #
   from the evidence plan and the owner of the data, the one who made
   it. Write the type. `measured`: a test, a survey, or a
   specification. `estimated`: calculated from other numbers or a
   model. `guidance`: a rule that an expert, an editor, or a maker
   publishes, with no test behind it. `example`: made up to show an
   idea. Name the owner in every
   row. Do not point to another row. If no adopted source supports the
   gain, write the narrower claim: the smaller statement that the
   adopted sources do support.
6. Fill First-Party Evidence from the First-party material row of the
   task brief: the method, the evidence, and the results. If the row
   is `missing`, write `none supplied`. If no item of the row is about
   this topic, write `none supplied for this topic`.

#### Outputs

- `briefs/[slug]-information-gain.md`

#### Rules

- Plan only gains that serve the Positioning: they fit the type of
  post and the reader. More words, more fetched pages, or new wording
  is not a gain.
- Do not present the study or the data of another company as work of
  the user. Do not write a gain that Does not sell or claim forbids.
- If a gain has no adopted source, make its claim narrower. Do not
  keep the full claim with a disclaimer.
- Do not name a ranking page, a rank, or a gap ID in the Gains table.
  The brief copies the table, and its reader does not see the
  competitor files. A name for a framework or a checklist is not proof
  that it works.

#### Example

Ebestron, Gains table:

- 7-Symptom Fault Finder: symptom → likely cause → action → part.
- Symptom-to-Part Index: locate the part from what you see.
- 60-Second Triage: observe → rule out → check → part.
- Pot-Life Clock: keep the working-time concepts apart.
- Warning: naming a framework does not prove that it works.

#### Check

- Deliverable gain names a Gains row that delivers the Deliverable,
  and at least one gain makes Our Difference real.
- Every row names a thing that the reader can use, and its Use ends
  with what the reader can understand, decide, or do. No cell names a
  ranking page, a rank, or a gap ID, or restates a Finding.
- Every Evidence requirement names owner and type, with a narrower
  claim where evidence is missing. First-Party Evidence names what
  the user supplied or says `none supplied`.
