### Step 1.5: SERP Intent Gate

Plan a blog post only if Google ranks blog posts for the keyword. In
this step, you fill `templates/search-intent.md` and save it as
`briefs/[slug]-search-intent.md`.

1. Call `mcp__dataforseo__api_request` one time: `POST /v3/serp/google/organic/live/advanced`,
   `depth: 10`, `noAiMode: true`, `location_code: 2840`, `language_code: "en"`.
   If the user names another market, use its codes. If the tool is
   missing or fails two times, stop and say why. Do not use WebSearch.
2. Give each `organic` item one label from its URL and title. Do not
   open the page. The labels are:
   - `blog`: an article that answers the query, also a guide on a store site.
   - `product`: one item.
   - `category`: a list of items, also a store search page.
   - `tool`: a calculator or a converter.
   - Another kind, for example `video` or `forum`.
3. Mark each item on topic or off topic. If the page is for the reader
   of the focus keyword, write `yes`. If not, write the first class
   that applies:
   - `consumer`: a consumer use of an industrial word.
   - `local`: a local business.
   - `brand`: a page only for a search of that brand name.
   - `other meaning`: the same word with another meaning.
4. Count each label. Write the blog share as `blog [n]/[organic count]`
   and as a percent.
5. Read the `blog` titles and the PAA questions. Find the task that
   they answer: what the searcher wants to do or know. When you
   understand that task, write it in one sentence: "The searcher wants
   to ...". Do not write the sentence from the keyword alone. Step 2
   uses this sentence to filter the keywords.
6. Write `present` or `none` for the AI Overview and for the featured
   snippet. A feature that is `none` does not show low demand or weak
   competition.
7. Stop if one of these is true: the blog share is below 30%; the `tool`
   count is equal to or above the `blog` count; the off-topic count is 5
   or more. The 30% line is a rule of this skill, not a Google standard.
8. If you stop, show the counts with one example URL for each label.
   Name the page type that fits the SERP, from the label with the most
   items. For a tie, name both. `product` leads to a product page,
   `category` to a category page, `tool` to a tool page, and off topic
   to another keyword. Ask the user to write anyway, try another
   keyword, or end. Do not choose for the user. Write `pending` in the
   file until the user answers.
9. Save the file. Step 5 copies the reader task, the counts, and the
   decision into the Search Intent section of the brief.
