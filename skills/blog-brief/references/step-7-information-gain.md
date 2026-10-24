### Step 7: Information Gain

#### Goal

Turn the competitor gaps into gains for the reader. A gain is a thing
that the reader can understand, decide, or do after this post, and not
after the ranking pages.

#### Inputs

- `templates/information-gain.md`: the output template.
- `briefs/[slug]-competitor-gaps.md`: the Gap List, Our Difference, and
  Format Advantage.
- `briefs/[slug]-task-brief.md`: the Does not sell or claim row.
- The statistics that Step 6, Statistics Research, kept. Step 6 writes
  no file.

#### Rules

- A longer post, more fetched pages, or new wording is not a gain.
- Do not present the study or the data of another company as work of
  the user.
- A name for a framework or a checklist is not proof that it works.
- Do not write a gain that the Does not sell or claim row forbids.
- If no kept statistic supports a gain, make the claim narrower. Do not
  keep the claim and add a disclaimer.

#### Steps

1. Write Main Gain in one sentence, from Our Difference.
2. For each gap in the Gap List, fill one row of the Gains table. If two
   gaps lead to the same gain, put both gap IDs in one row.
3. If Format Advantage is not none, fill one more row for it. Write
   `format` in From gap.
4. In Evidence, write the kept statistic that supports the gain. If no
   statistic supports it, write `none` and the narrower claim.
5. In First-Party Evidence, write the method, the evidence, and the
   results that the user supplied. If the user supplied none, write
   `none supplied`.

#### Outputs

- `briefs/[slug]-information-gain.md`

#### Check

- Every gap ID of the Gap List is in the From gap column.
- Every This post adds cell says what the reader can understand,
  decide, or do.
- No This post adds cell and no Main Gain names a ranking page, a rank,
  or a gap ID.
- Every Evidence cell has a statistic, or `none` and a narrower claim.
- First-Party Evidence names what the user supplied, or says
  `none supplied`.
