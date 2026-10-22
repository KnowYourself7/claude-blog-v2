### Step 1.5: SERP Intent Gate

Plan a blog post only if Google already ranks blog posts for the keyword.

1. Call `mcp__dataforseo__api_request` once: `POST /v3/serp/google/organic/live/advanced`,
   `depth: 10`, `noAiMode: true`, `location_code: 2840`, `language_code: "en"` unless the user
   names another market. If the tool is missing or fails twice, stop and say
   why; never fall back to WebSearch.
2. Label each `organic` item from its URL and title: `blog` (any article
   answering the query, including guides on store sites), `product`,
   `category`, or the specific other kind (`video`, `forum`, ...). Count each
   label separately.
3. Continue only if `blog` strictly outnumbers every other label. Otherwise
   stop, ties included: show the counts with one example URL each and ask the
   user to write anyway, try another keyword, or end.
4. Carry the table, counts, and decision into the brief's Search Intent section.
