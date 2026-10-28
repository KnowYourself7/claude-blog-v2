### Step 11: A-to-B Gate

Compare the files of Step 1 to Step 10 with each other before the
brief goes to `/blog write`. The gate checks direction, structure, and
evidence.

#### Tools

- `scripts/brief_state.py gate`, run with `python3` from the project
  root. It reads the files. You do not.

#### Inputs

- The files of Step 1 to Step 10: `briefs/[slug]-task-brief.md`,
  `briefs/[slug]-search-intent.md`, `briefs/[slug]-demand-facets.md`,
  `briefs/[slug]-competitor-gaps.md`, `briefs/[slug]-evidence-plan.md`,
  `briefs/[slug]-information-gain.md`, `briefs/[slug]-outline.md`,
  `briefs/[slug]-brief.md`.
- The state file `briefs/[slug]-state.json`.

#### Actions

1. Run `gate --slug [slug]`. Each check prints one result. `pass`.
   `warn`: shown to the user, not a stop. `fail`: a step must be done
   again. `not built`: the check is planned, and its code does not
   exist yet. `redo_from` is the earliest step to do again. The script
   prints these and the status of Step 11 as JSON.
2. If the JSON shows Step 11 as `done`, tell the user the result and
   each `warn` and `not built` item with its detail. Then say that the
   brief is ready for `/blog write`.
3. If the JSON shows Step 11 as `in_progress`, the gate failed one
   time. Tell the user each `fail` item and `redo_from`. Run
   `set --slug [slug] --step [redo_from] --status in_progress`. Do
   that step and each later step again, up to Step 10. Then go to
   action 1.
4. If the JSON shows Step 11 as `stopped`, the gate failed two times
   in a row. Show each `fail` item, its detail, and its `redo` step,
   the step to do again for that item. Ask the user: accept the brief
   as it is, or do a step again. Wait for the answer.
5. If the user accepts the brief, run
   `set --slug [slug] --step 11 --status in_progress`, then
   `set --slug [slug] --step 11 --status done --note "[the answer]"`.
   If the user asks for a change, do action 3 with the step of that
   change as `redo_from`.

#### Outputs

- No file. The result is the `gate` section of
  `briefs/[slug]-state.json`.

#### Rules

- Fix a `fail` by doing the `redo_from` step again. Never edit a brief
  file by hand to pass the gate.
- `warn` does not stop the brief. The user decides. `not built` is not
  a fail. Its detail names the plan item, for example A-04.
- The article is not written and not published at this point.

#### Example

One run with result `warn`:

- Direction: Page this post supports `warn`, the row is `missing`.
- Evidence: Weak questions `warn`, one question has no adopted source.
- `not built`: Competitive opportunity (A-04), Semantic baseline
  (A-09).
- The user accepted the brief. The Step 11 note is `Gate: warn`.

#### Check

- In `briefs/[slug]-state.json`, `gate.checked` is later than
  `updated` of every step from Step 1 to Step 10.
- Step 11 is `done`, or the user answered a stopped gate.
- The Step 11 note holds `Gate: ...` or the answer of the user.
