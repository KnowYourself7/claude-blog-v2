### Step 9: Generate the Brief

#### Goal

Turn Outline V2 and the research files into the brief that
`/blog write` reads.

#### Inputs

- `templates/brief-template.md`: the output template. Each
  placeholder says where its content comes from.
- `briefs/[slug]-outline.md`: Outline V2, for the Content Outline and
  the title.
- `briefs/[slug]-search-intent.md`: the market, the date, the reader
  task, the counts, and the decision.
- `briefs/[slug]-evidence-plan.md`: the adopted sources, for
  Statistics to Include.
- `briefs/[slug]-task-brief.md`: the Page this post supports, for
  Internal Link Architecture.
- `briefs/[slug]-information-gain.md`: First-Party Evidence, for the
  Experience line of E-E-A-T Signals.
- `briefs/[slug]-state.json`: the note of Step 5, the template and the
  reason, for the Template section.

#### Rules

- Copy Outline V2 into the Content Outline without change.
- Do not guess a URL.

#### Steps

1. Fill `templates/brief-template.md` in its order.

#### Outputs

- The filled brief. Step 10 saves it as `briefs/[slug]-brief.md`.

#### Check

- The Content Outline is the same as Outline V2 of the outline file,
  without its Title line.
- Every source # in the Content Outline has a row in Statistics to
  Include. Every row is an adopted source that the Content Outline
  cites.
- Internal Link Architecture names only the Page this post supports,
  or `missing`.
- Every placeholder of the template is filled.
