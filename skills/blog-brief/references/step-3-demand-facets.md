### Step 3: Keywords to Demand Facets

Expand the focus keyword into the questions that readers ask, then
merge them into demand facets. Each facet is one question that the
post must answer.

#### Tools

- `scripts/keyword_pool.py`, run with `python3` from the project
  root. `python3 scripts/keyword_pool.py <subcommand> --help` lists
  the flags. It reads `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.
  If they are not set, stop and ask the user to set them.
- Its five DataForSEO endpoints: Autocomplete, the organic SERP with
  the PAA box (People Also Ask) opened two levels deep, Related
  Keywords two levels deep, Keyword Overview, AI Keyword Data.

#### Inputs

- The Reader Task and the SERP Features section, from
  `briefs/[slug]-search-intent.md`.
- The Market row (location_code / language_code), Sells, and Does not
  sell or claim, from `briefs/[slug]-task-brief.md`.

#### Actions

1. Run
   `expand --slug [slug] --focus "[focus keyword]" --seed "[focus keyword]" --round 1 --location [location_code] --language [language_code]`.
   It writes `briefs/[slug]-questions.md`, the questions file below.
   The file has one row per distinct text from PAA, autocomplete,
   related searches, and related keywords, with its sources. It also
   has a Calls table with the cost of each call. The script prints a
   JSON summary. If the summary
   has `"short": true` (fewer than 9 questions), do action 2. If not,
   skip to action 3.
2. A modifier is a word that narrows the reader task, such as a color
   or an audience. Make the wider seed: remove the modifiers from the
   focus keyword. If the focus keyword has no modifier, use a shorter
   phrase for the same reader task. For example, `linen in winter`
   for `can you wear linen in winter`. Run `expand` again with
   `--seed "[wider seed]" --round 2`. Do not run a third round.
3. Run `volume --slug [slug]`. It fills the search volume, KD
   (keyword difficulty, 0 to 100), and intent of every row from
   Keyword Overview. A row that the API does not know stays `null`.
4. Read the questions file. Write `briefs/[slug]-facets.json`, a JSON
   list. Each item has `question`, `values`, `rows`, `business`, and
   `reason_kept`.
   - `question`: one reader question. Synonyms are one facet. Rows
     that differ in one value only, such as black and white linen
     pants, are one facet, and `values` lists those values.
   - `rows`: the `#` of each row that the facet covers. A row goes to
     one facet at most.
   - Attach no row that is about another task, another audience,
     another meaning of the word, or store or platform navigation.
     Keep its `#` and the reason for Removed Rows in action 7.
   - `business`: `out` when the facet asks for a thing outside Sells
     or inside Does not sell or claim. Else `in`. A styling or how-to
     question that only names such a thing is `in`. For example,
     "What shoes go with a cardigan?" is `in` for a brand with no shoes.
   - `reason_kept`: one sentence. For an `out` facet, say why it is
     out. For a facet that matches a product line with a low or `null`
     volume, say that the business sells the product.
5. Run `rank-facets --slug [slug] --facets briefs/[slug]-facets.json`.
   It picks the representative keyword, the attached row with the
   highest volume. It moves `out` facets to Other Facets, sorts by
   source count then volume, and keeps the first 9. It writes
   `briefs/[slug]-facet-tables.md`, the facet tables file below. If
   the summary note is `fewer than 3 facets kept`, stop. Tell the
   user that the keyword is possibly too narrow for one post. Ask:
   write anyway, another keyword, or end. Write anyway: do action 6.
   Another keyword: start again at Step 1. End: stop the run.
6. Run `ai --slug [slug]`. It adds the AI search volume of each
   representative keyword and a line with the endpoint, market, and
   date to the facet tables file.
7. Fill `templates/keyword-research.md` as
   `briefs/[slug]-keyword-research.md`: Data Scope, Rounds, Removed
   Rows, and the SERP Features section copied from
   `briefs/[slug]-search-intent.md`.
8. Fill `templates/demand-facets.md` as `briefs/[slug]-demand-facets.md`.
   Fill the header table. Then copy the Kept Facets table, the AI
   search volume line, and the Other Facets table from the facet
   tables file.

#### Outputs

- `briefs/[slug]-keyword-research.md`
- `briefs/[slug]-demand-facets.md`
- Work files, shared with the script: `briefs/[slug]-questions.md`,
  `briefs/[slug]-questions.json`, `briefs/[slug]-facets.json`,
  `briefs/[slug]-facet-tables.md`.

#### Rules

- Volume, KD, intent, and AI search volume come only from the script.
  A missing value is `null`, never `0`, because `0` reads as "nobody
  asks". Do not add the volumes of two keywords.
- AI search volume is not a Google volume. Keep the two columns apart
  and keep the line that names its endpoint, market, and date. A
  mention in an AI answer is not traffic and not a lead.
- If the script prints an error, stop the run and say why. Do not use
  WebSearch, because it is not DataForSEO data.
- The questions find the scope of the post. They are not a list of
  words to put into the text.

#### Example

Ebestron, demand facets, 5 of 9 shown:

- F1: question "Why does the epoxy not cure?", representative keyword
  `epoxy not curing`, section fault 1 of the post.
- F2: "Why is the mix uneven?", `static mixing nozzle`, fault 2.
- F3: "Why does the nozzle clog?", `clogged mixing nozzle`, fault 3.
- F4: "Why are there air bubbles?", `air bubbles in epoxy`, fault 4.
- F6: "Why does the gun drip?", `cartridge gun dripping`, the lowest
  volume, kept because the business sells the part.
- Warning: a low or missing volume does not mean that nobody asks.

#### Check

- Round 1 ran. Round 2 ran only if round 1 was short. 3 to 9 facets
  are kept, or the user chose write anyway.
- In `briefs/[slug]-facets.json`, no row number is in two facets, and
  every row of the questions file is in a facet or in Removed Rows.
- No missing value is `0`. The Kept Facets and Other Facets tables
  and the AI search volume line match the facet tables file.
