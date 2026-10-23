### Step 3: Keywords to Demand Facets

Read these files first:

- `templates/keyword-research.md` is the keyword evidence. Save it as
  `briefs/[slug]-keyword-research.md`.
- `templates/demand-facets.md` is the facets. Save it as
  `briefs/[slug]-demand-facets.md`.
- `briefs/[slug]-search-intent.md` gives the reader task.
- `briefs/[slug]-task-brief.md` gives the market and the business
  scope.

A demand facet is one part of the reader task: one question that the
post must answer.

Rules:

- Volume, KD, and intent come only from DataForSEO Labs responses.
  Write `null` for a missing value, never `0`. Do not add the volumes
  of two keywords.
- Send calls with `mcp__dataforseo__api_request`, with `noAiMode: true`
  and the `location_code` and `language_code` of the task brief. If a
  call fails two times, stop and say why. Do not use WebSearch.
- Reuse the Step 2 Live SERP response. Do not call the SERP again.

Keywords, in `keyword-research.md`:

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
4. Keyword Suggestions: call
   `dataforseo_labs/google/keyword_suggestions/live` once for each
   seed, with `limit: 300`. Fill the Keyword Pool as the template
   says.
5. Other Sources: the PAA questions and the related searches that are
   not in the pool.
6. Removed Keywords: from both tables, remove the keywords that do not
   ask about the reader task. Give each one the first class that
   applies, in this order: other audience, other task, other meaning
   of the same word, store or platform navigation, business conflict.
   A product brand, such as nike, is not a store. A business conflict
   asks for a thing outside the business scope, such as another
   audience or another product type. Keep a keyword when you are not
   sure. Never remove a keyword for its volume or intent. Give one
   reason for each class.
7. Keyword Overview: call `dataforseo_labs/google/keyword_overview/live`
   once for the related searches that stay in Other Sources. Skip the
   call if none stays.
8. Save the keyword file.

Facets, in `demand-facets.md`:

9. Make facets from the Question Evidence items. Items that differ in
   one value only form one facet, with the values listed. For example,
   black and white linen pants differ only in the color. An item about
   another task goes to Other Facets with the reason `other page`.
10. Read the first 50 Keyword Pool rows and all Other Sources rows.
    A row that restates the focus keyword goes to the focus keyword.
    A row that answers a facet goes to that facet. A row that names a
    new part of the reader task becomes a new facet. A row that fits
    nothing is `other page`.
11. Representative keyword: the attached keyword with the highest
    volume. On a tie, the first in the keyword file. Copy its volume,
    KD, and intent, or `-` if the facet has no keyword.
12. Sort the facets as the template says. The six evidence types are
    the five parts of Question Evidence and the attached rows.
13. Business scope: move a facet outside the scope to Other Facets
    with the reason `outside business`. Keep a facet that matches a
    product line even at low or `null` volume, and say so in Reason
    kept.
14. Then keep the first 9 facets. The rest go to Other Facets with
    the reason `lower rank`.
15. If fewer than 5 facets are kept, call
    `dataforseo_labs/google/related_keywords/live` once for the focus
    keyword, with `depth: 2`. Its `core_keyword` is under
    `keyword_data.keyword_properties`. Add the keywords to the Keyword
    Pool and the Removed Keywords tables as items 4 and 6 say, with no
    new Suggestions call. Record the call and save the keyword file
    again. Then do items 10 to 14 again. Do this item once.
16. If fewer than 3 facets are kept after that, stop. Tell the user
    that the keyword is possibly too narrow for one post. Ask the user
    to write anyway, try another keyword, or end.
17. Save the facets file.
