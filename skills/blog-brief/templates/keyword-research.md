<!-- Output template for the blog-brief skill (Step 2, items 1 to 12). Fill
     every [bracket] and keep the section order. The rules for filling it
     are in ../SKILL.md. -->

# Keyword Research: [focus keyword]

This file is the keyword evidence for `briefs/[slug]-demand-facets.md`.

## Data Scope

| Item | Value |
|------|-------|
| Focus keyword | [keyword] |
| Market | [location_code] / [language_code] |
| Date | [YYYY-MM-DD] |
| Search volume, KD, intent | DataForSEO Labs: Suggestions for the pool, Overview for other sources |

| Call | Endpoint | Parameters | Results |
|------|----------|------------|---------|
| Live SERP | Step 1.5 response, no new call | keyword "[focus keyword]", depth 10 | [n] AI Overview sections, [n] PAA, [n] related searches, [n] organic |
| Google Autocomplete | `autocomplete/live/advanced` | keyword "[focus keyword]", client "gws-wiz-serp" | [n], [n] kept as evidence |
| Keyword Suggestions, seed [n] | `keyword_suggestions/live` | keyword "[seed]", limit 300 | [n] of [total_count] |
| Keyword Overview | `keyword_overview/live` | [n] related searches, or not called | [n] |
| Related Keywords | `related_keywords/live` | keyword "[focus keyword]", depth 2 | not called, or [n] of [total_count] |

## Question Evidence

Copy the text as it is. If a part has no items, write one row with `none`.

| # | Part | Text | Label |
|---|------|------|-------|
| 1 | [AI Overview / PAA / related search / organic title / Autocomplete] | [text] | [Step 1.5 label for an organic title, or -] |

## Seeds

| # | Seed | How and why | Results |
|---|------|-------------|---------|
| 1 | [focus keyword] | focus keyword | [n] of [total_count] |
| 2 | [seed, or not made] | [the modifiers that you removed, or "the focus keyword has no modifier"] | [n] of [total_count] |
| 3 | [seed] | [why this phrase names the same reader task] | [n] of [total_count] |

## Keyword Pool

The table has one row for each `core_keyword` group. The rows go from
the highest volume to the lowest. If volumes are equal, the call order
stays. The main keyword has the highest volume. Peak month is the highest
month of the last 12 months. For a tie, give the last month and the tie
count, for example `Oct 2025: 8100 (3 tied)`. KD comes from the backlinks
of the ranking pages, so `0` means weak pages rank. Do not sort by KD
alone. `null` means no value.

| # | Main keyword | Variants | Search volume | Peak month | KD | Intent | Other intents | Source |
|---|--------------|----------|---------------|------------|----|--------|---------------|--------|
| 1 | [keyword] | [other spellings, or none] | [n or null] | [Mon YYYY: n] | [0-100 or null] | [main_intent or null] | [foreign_intent, or none] | [suggestions (seed n) / related] |

## Other Sources

PAA questions and related searches that are not in the Keyword Pool.
They are not grouped. PAA questions are not sent to Overview, so write
`-` in their data columns.

| # | Keyword | Source | Search volume | Peak month | KD | Intent |
|---|---------|--------|---------------|------------|----|--------|
| 1 | [word] | [PAA / related search] | [n or null] | [Mon YYYY: n] | [0-100 or null] | [main_intent or null] |

## Removed Keywords

| Class | Examples | Reason |
|-------|----------|--------|
| [other audience / other task / other meaning of the same word / store or platform navigation / business conflict] | [keyword], [keyword] | [one sentence] |

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
