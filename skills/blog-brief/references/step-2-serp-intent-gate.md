### Step 2: SERP Intent Gate

Make sure that this keyword wants a blog post, not a product page, a
category page, or a calculator.

#### Tools

- DataForSEO Live SERP, through `mcp__dataforseo__api_request`.

#### Inputs

- Focus keyword, the Market row (location_code / language_code), and
  the type of post in the Positioning row, from
  `briefs/[slug]-task-brief.md`.

#### Actions

1. Call `POST /v3/serp/google/organic/live/advanced` one time with
   `keyword`, `location_code`, `language_code`, `depth: 10`, and
   `noAiMode: true`. If the tool is missing or fails two times, stop
   the run and say why.
2. Give each organic item one Label from its URL and title. `blog`:
   an article or guide, also on a store site. `product`: one item.
   `category`: a list of items, also a store search page. `tool`: a
   calculator or converter. Another kind, such as `video`: write the
   kind.
3. Give each item one On topic value. `yes`: for the reader of the
   focus keyword. `consumer`: a consumer use of an industrial word.
   `local`: a search for a nearby business. `brand`: a search for
   that brand name. `other meaning`: another meaning of the word.
4. Fill the Counts table. Write Blog share as
   `blog [n]/[total] = [n]%` and Off topic as `[n] of [total]`.
5. Read the `blog` titles and the PAA questions (PAA is the People
   Also Ask box of the results page). Write the Reader Task in one
   sentence, "The searcher wants to ...". Write the Post type in two
   or three words. If it differs from the type in the Positioning
   row, write both and do not change the task brief.
6. Write `present` or `none` for the AI Overview and the featured
   snippet.
7. Fill the Decision table with `yes` or `no` for each of its three
   rules. The rules are: blog share below 30%, `tool` count equal to
   or above `blog` count, off topic 5 or more. If every rule is `no`,
   write Decision `continue` and User choice `not needed`. If any
   rule is `yes`, write Decision `stop` and User choice `pending`.
   Write the page type that fits: the label with the most items, both
   for a tie, or `another keyword` when off-topic items lead. Then
   stop and ask the user.
   Show the Counts table with one example URL per label, and ask:
   write anyway, another keyword, or end. Write the answer in User
   choice.

#### Outputs

- `briefs/[slug]-search-intent.md`, from `templates/search-intent.md`.
  Step 9 copies the Reader Task, the counts, and the decision.

#### Rules

- The 30% line is a rule of this skill, not a Google standard.
- Label from URL and title only. Do not open pages. Do not use
  WebSearch, because it is not the ranked SERP.
- `none` for an AI Overview does not mean low demand, and does not
  mean weak competition.
- When you stop, do not choose for the user.

#### Example

Ebestron, search intent:

- Reader Task: fix sticky output, two colors, or a blocked mixer in
  two-part dispensing.
- Blog share about 80%. Blog pages include Permabond and btektech.
- Post type: troubleshooting post. Product selection stays with the
  product page.
- AI Overview: none. This does not mean low demand or weak
  competition.

#### Check

- Every organic item has a Label and an On topic value. Blog share
  shows the count, the total, and the percent.
- The Reader Task is one sentence. The Post type is two or three
  words.
- If you stopped, User choice is `pending` or the answer of the user,
  and the page type that fits is named.
