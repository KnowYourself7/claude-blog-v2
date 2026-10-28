### Step 3: Keywords to Demand Facets

#### Goal

Turn the keywords of the topic into demand facets. A demand facet is
one part of the reader task: one question that the post must answer.

#### Inputs

- `templates/keyword-research.md`: the template for the keyword
  evidence.
- `templates/demand-facets.md`: the template for the facets.
- `scripts/keyword_pool.py`: the script that calls DataForSEO Labs,
  builds the keyword pool, and ranks the facets. Run it with
  `python3`. `<subcommand> --help` lists the fields of each JSON file
  that you write for it.
- `briefs/[slug]-search-intent.md`: the reader task.
- `briefs/[slug]-task-brief.md`: the market codes, and the business
  scope in the Sells and Does not sell or claim rows.
- The Live SERP response of Step 2, SERP Intent Gate. Do not call the
  SERP again.

#### Rules

- Volume, KD (keyword difficulty, 0 to 100), and intent come only from
  DataForSEO Labs, through the script. Write `null` for a missing
  value, never `0`. Do not add the volumes of two keywords.
- The script reads `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` from
  the environment. If the script prints an error, stop and say why. Do
  not use WebSearch.
- The script does the grouping, the sorting, the tie breaks, and the
  counts. Do not do them again by hand.

#### Steps

Keywords:

1. Copy four parts of the Step 2 response as the Question Evidence:
   the AI Overview section titles, the PAA (People Also Ask)
   questions, the related searches, and the organic titles. Add the
   Step 2 label to each organic title.
2. Call `serp/google/autocomplete/live/advanced` one time for the
   focus keyword. Send it with `mcp__dataforseo__api_request`, with
   `client: "gws-wiz-serp"`, `noAiMode: true`, and the market codes of
   the task brief.
   - A modifier is a word that narrows the reader task, for example a
     color or an audience.
   - Add the questions to the Question Evidence as the fifth part. Add
     the suggestions that add a new modifier to the same part.
   - Do not use the questions or the suggestions for volume.
3. Make the seeds. A seed is a keyword that the script expands into
   more keywords. Write how you made each seed.
   - Seed 1 is the focus keyword.
   - Seed 2 is the focus keyword without its modifiers. If the focus
     keyword has no modifier, skip seed 2.
   - Seed 3 is a shorter phrase for the same reader task.
4. Write the PAA questions and the related searches of the Step 2
   response to `briefs/[slug]-evidence.json`. Then run the `pool`
   subcommand with the focus keyword, the seeds, the market codes, and
   that file. The subcommand writes `briefs/[slug]-keyword-pool.md`
   and `.json`. This step uses two tables of the pool file:
   - Keyword Pool: the keywords that DataForSEO Labs gives for the
     seeds. Item 10 can add more keywords.
   - Other Sources: the PAA questions and the related searches that
     are not in the Keyword Pool.
5. Read the Keyword Pool and Other Sources tables. Remove each keyword
   that does not ask about the reader task. Never remove a keyword for
   its volume or its intent. If you are not sure, keep the keyword.
   Give each removed keyword the first class that applies, in this
   order:
   - other audience
   - other task
   - other meaning of the same word
   - store or platform navigation. A product brand, such as nike, is
     not a store.
   - business conflict. The keyword asks for a thing outside the
     business scope, for example another audience or product type.

   Write the removals to `briefs/[slug]-removed.json`. Then run the
   `remove` subcommand.
6. Fill `keyword-research.md`: the Question Evidence, the Seeds, the
   SERP Features, and the link to the pool file.

Facets:

7. Make facets from the Question Evidence items. If items differ in
   one value only, make one facet and list the values. For example,
   black linen pants and white linen pants differ only in the color.
   If an item is about another task, put it in Other Facets with the
   reason `other page`.
8. Read the first 50 Keyword Pool rows and all Other Sources rows.
   Decide where each row goes:

   | The row | It goes to |
   |---------|------------|
   | restates the focus keyword | the focus keyword |
   | answers a facet | that facet |
   | names a new part of the reader task | a new facet |
   | fits nothing | `other page` |

9. Write the facets to `briefs/[slug]-facets.json`. Mark each facet
   `in` or `out` of the business scope. Do not drop a facet that
   matches a product line for a low or `null` volume. Say so in its
   reason. Then run the `rank-facets` subcommand. It picks the
   representative keyword of each facet and moves the `out` facets to
   Other Facets. Then it sorts the other facets, keeps the first 9,
   and writes `briefs/[slug]-facet-tables.md`.
10. If the script reports fewer than 5 facets, run the `related`
    subcommand one time. Then do items 8 and 9 again.
11. If fewer than 3 facets are kept after item 10, stop. Tell the user
    that the keyword is possibly too narrow for one post. Ask the user
    to write anyway, try another keyword, or end.
12. Copy the two tables from the facet tables file into
    `demand-facets.md`. Then fill the rest of the template.

#### Outputs

- `briefs/[slug]-keyword-research.md`
- `briefs/[slug]-keyword-pool.md` and `.json`, written by the script
- `briefs/[slug]-demand-facets.md`
- `briefs/[slug]-evidence.json`, `-removed.json`, `-facets.json`, and
  `-facet-tables.md`. You and the script use these files to pass data
  to each other.

#### Check

- 3 to 9 facets are kept, or you stopped and asked the user.
- Every kept facet has a reader question, evidence or rows, and a
  reason.
- No missing value is written as `0`.
- Each of the first 50 pool rows and each Other Sources row is in a
  facet, on the focus keyword, or `other page`.
- Every removed keyword has a class and a reason.
- The pool and facet tables came from the script, not by hand.
