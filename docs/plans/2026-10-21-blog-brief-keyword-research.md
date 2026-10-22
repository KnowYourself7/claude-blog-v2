# Design: DataForSEO keyword research in blog-brief Step 2

| Item | Value |
|---|---|
| Date | 2026-10-21 |
| Status | Not built yet. |
| Branch | feat/blog-brief-keyword-research |

## 1. Goal

Step 2 of blog-brief uses WebSearch to find keywords. WebSearch gives no search volume, no keyword difficulty (KD), and no intent. The new Step 2 gets this data from DataForSEO. It saves the result in a new file in the user project: `briefs/[slug]-keyword-research.md`.

The next branch adds demand facets. A demand facet is one reader question that the post must answer. That branch groups the keywords into facets and ranks them. This branch does not.

## 2. Source: Yudong course step A·05

The Yudong SEO course (page 115) uses four steps in this order:

1. Expand the keywords.
2. Remove duplicates and off-topic keywords. Filter by intent, then relevance, then search volume (page 78).
3. Group the keywords by reader question.
4. Rank the groups.

This branch does steps 1 and 2. It removes keywords by relevance only. Intent and search volume are recorded, and the ranking step uses them.

## 3. Step 2 flow

Step 2 makes its own calls and uses no data from other steps. Every call uses `location_code: 2840` and `language_code: "en"`, unless the user names another market. Every call also sends `noAiMode: true`. The default AI mode cuts results and drops `null` fields. If a call fails two times, stop and tell the user why. Do not fall back to WebSearch.

1. Call Live SERP on the focus keyword with `depth: 10`. Take the PAA questions, the related searches, the SERP features, and the titles and URLs of the organic results.
2. Use the focus keyword as seed 1. From the titles and URLs of step 1, take 1 or 2 other phrasings of the focus keyword, for example "his and hers matching outfits". Each phrasing must name the same thing for the same audience.
3. Call Keyword Suggestions on each seed with `limit: 300`. If a seed has more than 300 matches, the call returns the 300 with the highest search volume.
4. If seed 1 has fewer than 50 matches (`total_count`), make 1 or 2 shorter seeds. Each shorter seed must keep the core noun and the audience. Call Keyword Suggestions on each one.
5. Call Related Keywords on the focus keyword with `depth: 2`.
6. Call Google Autocomplete on the focus keyword with `client: "gws-wiz-serp"`. Take the suggestions from the response.
7. Remove exact duplicates. Ignore letter case.
8. Group the keywords from Keyword Suggestions and Related Keywords by `core_keyword`. Read it from `keyword_properties` in Suggestions and from `keyword_data.keyword_properties` in Related Keywords. A keyword with no `core_keyword` and the keywords that point to it form one group. Put one row for each group in the keyword pool.
9. Put the words from Autocomplete, PAA, and related searches in a separate table after the keyword pool. Do not group them. If the same word, ignoring case, is in the keyword pool, keep it only in the keyword pool.
10. Remove off-topic keywords from both tables. Remove only these classes, in this order:
    - Other audience, for example mother and daughter outfits.
    - Other task, for example outfits for a game avatar.
    - Store or platform navigation, for example shein, amazon, or reddit.
    - Business conflict.

    A clothing brand, for example nike, is not a store. Keep it. If a keyword fits more than one class, use the first class. If you are not sure, keep the keyword. Do not remove keywords by search volume or intent. Write one reason for each class of removed keywords.
11. Call Keyword Overview with every spelling that remains in the keyword pool, and with the Autocomplete and related search words. Do not send PAA questions, because Overview has no data for full questions. Send up to 700 keywords in each call.
12. In each group, use the spelling with the highest Overview search volume as the main keyword. List the other spellings as variants.
13. Fill the template and save it.

Search volume, KD, intent, other intents, and the peak month come only from Keyword Overview. If Overview returns no value, write `null`. Do not write `0` for a missing value. If Overview returns a KD of `0`, write `0`. A KD of `0` can also mean that Overview did not calculate KD. For this reason, the next step must not rank keywords by KD alone.

## 4. Template: keyword-research.md

The new template is skills/blog-brief/templates/keyword-research.md. It has these sections:

| Section | Content |
|---|---|
| Data scope | Focus keyword, market, date, and the parameters of each call |
| Seeds | Each seed, where it came from (focus keyword, results page, or shortened), and the number of results |
| Keyword pool | One row for each group: main keyword, variants, search volume, peak month, KD, intent, other intents, source |
| Other sources | One row for each word from Autocomplete, PAA, and related searches: keyword, source, search volume, peak month, KD, intent. PAA rows have no data. |
| Removed keywords | Each removed class, examples, and the reason |
| Not in Overview | The keywords that Overview did not return |
| SERP features | AI Overview and the publishers that it cites, featured snippet. Write `none` for a feature that is not on the results page. |

Column definitions:

- Peak month is the month with the highest search volume in `keyword_info.monthly_searches`, with its volume. It shows seasonal keywords, for example Halloween outfits.
- Other intents come from `search_intent_info.foreign_intent`.
- Use the same class names in the skill and the template.

The template has no cost column. The default response mode of the MCP server does not return the cost.

## 5. Change list

1. `skills/blog-brief/SKILL.md`: Rewrite Step 2 from section 3. Change the Target Keywords rule in Step 5.
2. skills/blog-brief/templates/keyword-research.md: Add the template from section 4.
3. `skills/blog-brief/templates/brief-template.md`: In Target Keywords, show the focus keyword with its search volume, KD, and intent. Replace the Secondary and Questions lines with a link to the keyword research file.
4. `docs/FORK-DEVLOG.md`: Add one entry after the merge.

Write all skill text with the simple-english skill.

## 6. Out of scope

- Grouping keywords into demand facets, and ranking them. The next branch does this.
- Merging spellings that DataForSEO puts in different groups, for example "valentine's" and "valentine's day". The demand facet step does this.
- A script or new tests.

## 7. Test plan

1. Run `python3 -m pytest tests/`, `python3 scripts/validate_skills.py --root .`, `python3 scripts/lint_prose.py`, and `python3 scripts/consistency_check.py`.
2. Open a new session in the claude-seo-playground folder. Run Step 1.5 and Step 2 with real data for "matching outfits for couples".

## Sources

- DataForSEO Keyword Suggestions: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live/
- DataForSEO Related Keywords: https://docs.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live/
- DataForSEO Keyword Overview: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_overview/live/
- DataForSEO Labs pricing: https://dataforseo.com/pricing/dataforseo-labs/dataforseo-google-api
- Yudong SEO course, pages 78 and 115: local file 瑜东SEO/sources/瑜东谷歌SEO线下课-结构化.md
- Design of Step 1.5: `docs/plans/2026-10-17-blog-brief-serp-intent-gate.md`
