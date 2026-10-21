# Design: DataForSEO keyword research in blog-brief Step 2

| Item | Value |
|---|---|
| Date | 2026-10-21 |
| Status | Approved. Not built yet. |
| Branch | feat/blog-brief-keyword-research |
| Scope | Step 2 and Step 5 of `skills/blog-brief/SKILL.md`, `skills/blog-brief/templates/brief-template.md`, one new template |

## 1. Request

Step 2 of blog-brief uses WebSearch to find keywords. WebSearch gives no Google search volume, no keyword difficulty (KD), and no intent. The brief template asks for a search volume from a named tool, so every brief says "not measured".

The user asks for two changes:

1. Replace WebSearch in Step 2 with four DataForSEO sources: Keyword Suggestions, Related Keywords, Live SERP for People Also Ask (PAA), and Keyword Overview for the data.
2. Save the research result in a new file that comes from a template.

A later branch adds a demand facet step. A demand facet is one reader question that the post must answer. That step groups the keywords into facets and ranks them by business value and search volume.

## 2. Why the change is necessary

| Question | Answer |
|---|---|
| What is wrong now? | WebSearch gives no search volume, KD, or intent. Secondary keywords come from guesses. |
| Can an existing step do it? | No. Step 1.5 uses DataForSEO for the SERP, but no step gets keyword data. |
| Cost for each brief | About 0.11 USD (section 5.4). |
| Who uses the data later? | The demand facet branch. It needs a full keyword pool with data. |

## 3. Reference: Yudong course step A·05

The Yudong SEO course, page 115, turns keywords into demand facets in this order:

1. Expand from the focus keyword and from more seed keywords. Add autocomplete, related searches, and PAA.
2. Remove duplicate phrasings. Filter by intent first, then by relevance, then by search volume (page 78).
3. Group the keywords by reader question. Pick one representative keyword for each facet. Do not stuff keywords into the post.
4. Combine the demand with business value, and rank the facets.

The workflow file `a05-demand-facets.md` in the local Yudong project adds two lessons from a real run on 2026-09-21:

- A long seed returns few results. Keyword Suggestions returns only terms that contain the seed. A 6-word seed gave 8 results. Two shorter seeds gave 72 and 91 results.
- The expand endpoints do not always return KD. Keyword Overview gives all data from one source on one date. Overview also returns no KD for many long-tail keywords, so `null` stays `null`.

This branch does the expand part and the data part of A·05. The next branch does the filter, group, and rank parts.

## 4. Evaluation of the request

The request matches the first half of A·05. We keep the four sources and the new file. We change four details:

| Item in the request | Change | Reason |
|---|---|---|
| Live SERP for PAA | Do not call it again. Read `people_also_ask` and `related_searches` from the Step 1.5 response. | Step 1.5 already called Live SERP for the same keyword. One call costs less, and both steps use the same data. |
| Keyword Suggestions on the focus keyword | Use the focus keyword and 1 or 2 shorter seeds. | A long seed returns few results (section 3). |
| Keyword Overview | Send the full pool after duplicates are removed, up to 200 keywords. | All data columns come from one source on one date. The next branch needs no API call. |
| Filtering | Do not remove keywords in this branch. | Filtering needs business judgment. It belongs with grouping and ranking. |

Step 2 must still give the brief one primary keyword, the secondary keywords, and the questions. Section 5.3 gives a temporary rule for this.

## 5. Design

### 5.1 Step 2 flow

Step 2 uses only DataForSEO. It makes no WebSearch call.

1. Pick the seeds. Seed 1 is the focus keyword.
2. Make 1 or 2 shorter seeds. Remove the modifiers and keep the reader task. Record each seed and the reason.
3. Call Keyword Suggestions once for each seed, with `limit: 50`.
4. Call Related Keywords once on the focus keyword, with `depth: 2`. Depth 2 returns about 72 keywords.
5. Read `people_also_ask` and `related_searches` from the Step 1.5 Live SERP response.
6. Merge all keywords and remove exact duplicates. Do not remove other keywords.
7. If the pool has more than 200 keywords, keep all PAA questions and related searches. Remove the other keywords with the lowest search volume until 200 remain.
8. Call Keyword Overview once with the full pool and `include_serp_info: true`.
9. Fill the template (section 5.2). Save it as `briefs/[slug]-keyword-research.md` in the user project.

Every call uses the market from Step 1.5: `location_code: 2840` and `language_code: "en"`, unless the user names another market.

Data rules:

- Search volume, KD, and intent come only from Keyword Overview.
- If Overview returns no data for a keyword, write `null`. Do not use a value from the expand endpoints. Do not write `0`.
- Item 5 of the current Step 2 stays. It reads AI Overview, featured snippet, and PAA from the Step 1.5 response. If the response does not include a feature, mark it `unavailable`.

### 5.2 Template: keyword-research.md

The new file is skills/blog-brief/templates/keyword-research.md. It has six sections:

| Section | Content |
|---|---|
| Data scope | Focus keyword, location, language, date, the path and parameters of each endpoint, and the cost of each call |
| Seeds | Each seed, how you shortened it, the reason, and the number of results |
| Keyword pool | One row for each keyword: keyword, search volume, KD, intent, source. Sort by search volume, highest first. Source is one or more of `suggestions`, `related`, `PAA`, and `related search`. |
| People Also Ask | The questions from the Step 1.5 response, as returned |
| Not in Overview | The keywords that Overview did not return, with the reason |
| Picks for the brief | Primary keyword, 3 to 5 secondary keywords, and 3 to 5 questions (section 5.3) |

The brief does not copy the keyword pool. The pool can have 200 rows. The `/blog write` command reads the brief, and it does not need every keyword.

### 5.3 Picks for the brief (temporary)

Until the demand facet branch is merged, Step 2 uses this rule to pick keywords for the brief:

1. Use the focus keyword as the primary keyword.
2. Pick 3 to 5 secondary keywords. Filter by intent first, then by topic relevance, then by search volume.
3. Pick 3 to 5 questions from PAA.

The Target Keywords section of the brief shows each picked keyword with its search volume and KD. It also links to the keyword research file. The demand facet branch replaces this rule.

### 5.4 Errors and cost

If a call fails two times, stop and tell the user the reason. Do not fall back to WebSearch. Step 1.5 uses the same rule.

Each DataForSEO Labs call costs 0.012 USD for the task and 0.00012 USD for each returned item. Overview does not charge for keywords that it does not return.

| Call | Count | Estimated cost (USD) |
|---|---|---|
| Keyword Suggestions, 50 results | 2 to 3 | 0.036 to 0.054 |
| Related Keywords, depth 2 | 1 | about 0.021 |
| Keyword Overview, 200 keywords | 1 | about 0.036 |
| Total | 4 to 5 | about 0.09 to 0.11 |

## 6. Change list

1. `skills/blog-brief/SKILL.md`: Rewrite Step 2 in 30 lines or fewer. Change the search volume rule in Step 5 to point to the keyword research file.
2. skills/blog-brief/templates/keyword-research.md: Add the new template (section 5.2).
3. `skills/blog-brief/templates/brief-template.md`: Add search volume and KD to Target Keywords. Add a link to the keyword research file.
4. `docs/FORK-DEVLOG.md`: Add one entry after the merge.

Write all skill text with the simple-english skill.

## 7. Out of scope

- Demand facet grouping, ranking, and filtering. The next branch does them.
- Google Autocomplete. In the 2026-09-21 run, it gave no question phrasings.
- A script, JSON snapshots, or new tests. The rules are short, and the model can follow them. If a real run shows errors, add a script then.

## 8. How we test

1. Run the project test and lint commands: `python3 -m pytest tests/`, `python3 scripts/validate_skills.py --root .`, `python3 scripts/lint_prose.py`, and `python3 scripts/consistency_check.py`. The current tests match fixed sentences in blog-brief. This change does not touch those sentences.
2. This session has no DataForSEO MCP server. A subagent runs Step 2 with sample API responses. Make sure that it shortens the seeds, removes duplicates, uses only Overview data, writes `null` and not `0`, and fills the template.
3. Before the merge, the user runs one real brief in a session that has DataForSEO connected.

## 9. Notes for the demand facet branch

- Follow A·05. Filter by intent, then by relevance, then by search volume. Write one reason for each removed keyword class.
- Each facet is one full reader question with one representative keyword and its variants. Do not add the search volumes of the variants together.
- Keep 5 to 9 facets. If fewer than 3 remain, tell the user that the keyword cannot support a full post.
- The Yudong gap analysis of 2026-10-20 names one risk. One facet for each section can turn the post into a list of questions with no link between sections.

## Sources

- DataForSEO Keyword Suggestions: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/
- DataForSEO Related Keywords: https://docs.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live/
- DataForSEO Keyword Overview: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live/
- DataForSEO Labs pricing: https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api
- Yudong SEO course, pages 78 and 115: local file 瑜东SEO/sources/瑜东谷歌SEO线下课-结构化.md
- Yudong workflow stage A·05 and its run log of 2026-09-21: local folder 瑜东SEO/.claude/skills/yudong-blog-workflow
- Earlier design for Step 1.5: `docs/plans/2026-10-17-blog-brief-serp-intent-gate.md`
