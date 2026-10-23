### Step 3: Keywords to Demand Facets

#### Goal

Turn the keywords of the topic into demand facets. A demand facet is
one part of the reader task: one question that the post must answer.

#### Inputs

- `templates/keyword-research.md`: the keyword evidence that you
  write.
- `templates/demand-facets.md`: the facets.
- `scripts/keyword_pool.py`: the script that calls DataForSEO Labs,
  builds the keyword pool, and ranks the facets. Run it with
  `python3`. `<subcommand> --help` lists the fields of each JSON file
  that you write for it.
- `briefs/[slug]-search-intent.md`: the reader task.
- `briefs/[slug]-task-brief.md`: the market and the business scope.

#### Rules

- Volume, KD, and intent come only from DataForSEO Labs, through the
  script. Write `null` for a missing value, never `0`. Do not add the
  volumes of two keywords.
- The script reads `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` from
  the environment. If it prints an error, stop and say why. Do not use
  WebSearch.
- Send the Autocomplete call with `mcp__dataforseo__api_request`, with
  `noAiMode: true` and the market codes of the task brief. Reuse the
  Step 2 Live SERP response. Do not call the SERP again.
- The script does the grouping, sorting, tie breaks, and counts. Do
  not redo them by hand.

#### Steps

Keywords:

1. Question Evidence: copy four parts from the Step 2 response. They
   are the AI Overview section titles, the PAA questions, the related
   searches, and the organic titles. Add the Step 2 label to each
   organic title.
2. Autocomplete: call `serp/google/autocomplete/live/advanced` once for
   the focus keyword, with `client: "gws-wiz-serp"`. A modifier is a
   word that narrows the reader task, such as a color or an audience.
   Add the questions, and the suggestions that add a new modifier, as
   the fifth part. Do not use them for volume.
3. Seeds: seed 1 is the focus keyword. Seed 2 is the focus keyword
   without its modifiers. Skip seed 2 if there is no modifier. Seed 3
   is a shorter phrase for the same reader task. Write how you made
   each seed.
4. Pool: write `briefs/[slug]-evidence.json` with the PAA questions
   and the related searches from the Step 2 response. Run the `pool`
   subcommand with the focus keyword, the seeds, the market codes, and
   that file. It writes `briefs/[slug]-keyword-pool.md` and `.json`.
5. Removed Keywords: read the Keyword Pool and Other Sources tables in
   the pool file. Remove the keywords that do not ask about the reader
   task. Give each one the first class that applies, in this order:
   other audience, other task, other meaning of the same word, store
   or platform navigation, business conflict. A product brand, such as
   nike, is not a store. A business conflict asks for a thing outside
   the business scope, such as another audience or another product
   type. Keep a keyword when you are not sure. Never remove a keyword
   for its volume or intent. Write the removals to
   `briefs/[slug]-removed.json` and run the `remove` subcommand.
6. Fill `keyword-research.md`: Question Evidence, Seeds, SERP
   Features, and the link to the pool file.

Facets:

7. Make facets from the Question Evidence items. Items that differ in
   one value only form one facet, with the values listed. For example,
   black and white linen pants differ only in the color. An item about
   another task goes to Other Facets with the reason `other page`.
8. Read the first 50 Keyword Pool rows and all Other Sources rows.
   A row that restates the focus keyword goes to the focus keyword.
   A row that answers a facet goes to that facet. A row that names a
   new part of the reader task becomes a new facet. A row that fits
   nothing is `other page`.
9. Rank: write the facets to `briefs/[slug]-facets.json`. Mark each
   facet `in` or `out` of the business scope. Keep a facet that
   matches a product line even at low or `null` volume, and say so in
   its reason. Run the `rank-facets` subcommand. It picks the
   representative keyword, sorts, moves the `out` facets to Other
   Facets, keeps the first 9, and writes `briefs/[slug]-facet-tables.md`.
10. If the script reports fewer than 5 facets, run the `related`
    subcommand once. Then do items 8 and 9 again.
11. If fewer than 3 facets are kept after that, stop. Tell the user
    that the keyword is possibly too narrow for one post. Ask the user
    to write anyway, try another keyword, or end.
12. Copy the two tables from the facet tables file into
    `demand-facets.md`, and fill the rest of it.

#### Outputs

- `briefs/[slug]-keyword-research.md`
- `briefs/[slug]-keyword-pool.md` and `.json`, written by the script
- `briefs/[slug]-demand-facets.md`
- `briefs/[slug]-evidence.json`, `-removed.json`, `-facets.json`, and
  `-facet-tables.md`, the files between you and the script

#### Check

- 3 to 9 facets are kept, or you stopped and asked the user.
- Every kept facet has a reader question, evidence or rows, and a
  reason.
- No missing value is written as `0`.
- Every one of the first 50 pool rows and all Other Sources rows is
  attached, on the focus keyword, or `other page`.
- Every removed keyword has a class and a reason.
- The pool and facet tables came from the script, not by hand.
