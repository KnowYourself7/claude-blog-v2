<!-- Output template for the blog-brief skill (Step 2). Fill every [bracket]
     and keep the section order. The rules for filling it are in ../SKILL.md. -->

# Keyword Research: [focus keyword]

## Data Scope

| Item | Value |
|------|-------|
| Focus keyword | [keyword] |
| Market | [location_code] / [language_code] |
| Date | [YYYY-MM-DD] |
| Search volume, KD, intent | DataForSEO Labs: Suggestions and Related for the pool, Overview for other sources |

| Call | Endpoint | Parameters | Results |
|------|----------|------------|---------|
| Live SERP | Step 1.5 response, no new call | keyword "[focus keyword]", depth 10 | [n] PAA, [n] related searches |
| Keyword Suggestions, seed [n] | `keyword_suggestions/live` | keyword "[seed]", limit 300 | [n] of [total_count] |
| Related Keywords | `related_keywords/live` | keyword "[focus keyword]", depth 2 | [n] of [total_count] |
| Google Autocomplete | `autocomplete/live/advanced` | keyword "[focus keyword]", client "gws-wiz-serp" | [n] |
| Keyword Overview | `keyword_overview/live` | [n] other-source words, or skipped | [n] |

## Seeds

If seed 1 has 50 or more matches, there are no shorter seeds.

| # | Seed | Source | Results |
|---|------|--------|---------|
| 1 | [focus keyword] | focus keyword | [n] of [total_count] |
| 2 | [seed] | [results page / shortened] | [n] of [total_count] |

## Keyword Pool

Keywords from Keyword Suggestions and Related Keywords, one row for each
`core_keyword` group. The main keyword is the spelling with the highest
search volume. Sorted by search volume, highest first. `null` means that
DataForSEO returned no value. Peak month is the month with the highest
volume in the last 12 months. If months tie, write the most recent one and
the number of tied months, for example `Oct 2025: 8100 (3 tied)`. KD comes
mostly from the backlinks of the ranking pages. A KD of `0` means that weak
pages rank, not that the keyword is easy, so do not rank by KD alone.

| # | Main keyword | Variants | Search volume | Peak month | KD | Intent | Other intents | Source |
|---|--------------|----------|---------------|------------|----|--------|---------------|--------|
| 1 | [keyword] | [other spellings, or none] | [n or null] | [Mon YYYY: n] | [0-100 or null] | [main_intent or null] | [foreign_intent, or none] | [suggestions (seed n) / related] |

## Other Sources

Words from Google Autocomplete, PAA, and related searches. They are not
grouped. PAA questions are not sent to Overview, so write `-` in their data
columns.

| # | Keyword | Source | Search volume | Peak month | KD | Intent |
|---|---------|--------|---------------|------------|----|--------|
| 1 | [word] | [autocomplete / PAA / related search] | [n or null] | [Mon YYYY: n] | [0-100 or null] | [main_intent or null] |

## Removed Keywords

| Class | Examples | Reason |
|-------|----------|--------|
| [other audience / other task / store or platform navigation / business conflict] | [keyword], [keyword] | [one sentence] |

## Not in Overview

Overview returned no data for these keywords.

- [keyword] ([source])

## SERP Features

From the Live SERP response. Write `none` for a feature that is not on the
results page.

| Feature | Result |
|---------|--------|
| AI Overview | [present or none]. Cited publishers: [names] |
| Featured snippet | [present or none]. Answer format: [paragraph / list / table] |
