### Step 2: SERP Intent Gate

#### Goal

Decide if a blog post fits this keyword. Google must already rank
blog posts for it.

#### Inputs

- `templates/search-intent.md`: the output template.
- `briefs/[slug]-task-brief.md`: the market codes.

#### Rules

- Send the call with `mcp__dataforseo__api_request`. If the tool is
  missing or fails two times, stop and say why. Do not use WebSearch.
- Label a page from its URL and title only. Do not open the page.
- The 30% line is a rule of this skill, not a Google standard.
- When you stop, do not choose for the user.

#### Steps

1. Call `POST /v3/serp/google/organic/live/advanced` one time, with
   `depth: 10`, `noAiMode: true`, and the market codes of the task
   brief.
2. Give each `organic` item one label.

   | Label | Meaning |
   |-------|---------|
   | `blog` | An article that answers the query, also a guide on a store site. |
   | `product` | One item. |
   | `category` | A list of items, also a store search page. |
   | `tool` | A calculator or a converter. |
   | another kind | For example `video` or `forum`. |

3. Mark each item as on topic or off topic. Write `yes` if the page
   is for the reader of the focus keyword. If not, write the first
   class that applies.

   | Class | Meaning |
   |-------|---------|
   | `consumer` | A consumer use of an industrial word. |
   | `local` | A local business. |
   | `brand` | A page only for a search of that brand name. |
   | `other meaning` | The same word with another meaning. |

4. Count each label. Write the blog share as `blog [n]/[organic count]`
   and as a percent.
5. Read the `blog` titles and the PAA questions. Find the task that
   they answer. Write it in one sentence: "The searcher wants to ...".
   Do not write it from the keyword alone.
6. Write `present` or `none` for the AI Overview and for the featured
   snippet. `none` does not show low demand or weak competition.
7. Stop if one of these is true:
   - The blog share is below 30%.
   - The `tool` count is equal to or above the `blog` count.
   - The off-topic count is 5 or more.
8. If you stop, show the counts with one example URL for each label.
   Name the page type that fits the SERP, from the label with the most
   items. For a tie, name both. `product` leads to a product page,
   `category` to a category page, `tool` to a tool page, and off topic
   to another keyword. Ask the user to write anyway, try another
   keyword, or end. Write `pending` in the file until the user
   answers.

#### Outputs

- `briefs/[slug]-search-intent.md`. Step 8 copies the reader task,
  the counts, and the decision from it.

#### Check

- Every organic item has a Label and an On topic value.
- The blog share shows the count, the total, and the percent.
- The reader task is one sentence that starts with "The searcher
  wants to".
- If you stopped, User choice is `pending` and the file names the
  page type that fits the SERP.
