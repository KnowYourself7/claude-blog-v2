### Step 11: A-to-B Gate

#### Goal

Compare the brief files with each other before the brief goes to
`/blog write`. A gate is a set of tests at the end of a phase. Phase A
is the research and the outline.

#### Inputs

- `briefs/[slug]-state.json`: the state file. The gate writes its
  result into its `gate` section.
- `scripts/brief_state.py`: the script that runs the gate. It reads
  these files. You do not read them.
  - `briefs/[slug]-task-brief.md`
  - `briefs/[slug]-search-intent.md`
  - `briefs/[slug]-demand-facets.md`
  - `briefs/[slug]-competitor-gaps.md`
  - `briefs/[slug]-evidence-plan.md`
  - `briefs/[slug]-information-gain.md`
  - `briefs/[slug]-outline.md`
  - `briefs/[slug]-brief.md`

#### Rules

- To fix a `fail`, do the step in `redo_from` again with its step file.
  Do not edit a brief file by hand to pass the gate.
- A `warn` item does not stop the brief. The user decides about a
  change.
- A `not built` item is not a fail. It names a part of the workflow
  that does not exist yet.

#### Steps

1. Run `gate --slug [slug]` with `python3` from the project root.
2. If Step 11 is `done`, tell the user the result and each `warn` and
   `not built` item with its detail. Then tell the user that the brief
   is ready for `/blog write`.
3. If Step 11 is `in_progress`, the gate failed one time. Tell the
   user each `fail` item and the step in `redo_from`. Run
   `set --step [redo_from] --status in_progress`. Then do that step and
   each later step again, up to this step.
4. If Step 11 is `stopped`, the gate failed two times in a row. Show
   the user each `fail` item, its detail, and its `redo` step. Wait for
   the answer.
5. If the user accepts the brief as it is, run
   `set --step 11 --status in_progress`. Then run
   `set --step 11 --status done --note "[the answer]"`. If the user asks
   for a change, do the step of that change again.

#### Outputs

- No file. The result is in the `gate` section of
  `briefs/[slug]-state.json`.

#### Check

- After each change to a brief file, `gate` ran again.
- Step 11 is `done`, or the user answered a stopped gate.
- The user saw every `warn` item and every `not built` item.
