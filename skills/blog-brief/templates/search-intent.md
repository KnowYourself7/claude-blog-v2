<!-- Output template for the blog-brief skill (Step 2). Fill every
     [bracket] and keep the section order. The rules for filling it are
     in ../references/step-2-serp-intent-gate.md. -->

# Search Intent: [focus keyword]

## Query

| Item | Value |
|------|-------|
| Focus keyword | [keyword] |
| Market | [location_code] / [language_code] |
| Date | [YYYY-MM-DD] |
| Source | DataForSEO Live SERP, `serp/google/organic/live/advanced`, depth 10 |

## Results

One row for each organic item. Labels come from the URL and the title.

| Rank | URL | Title | Label | On topic |
|------|-----|-------|-------|----------|
| [1] | [url] | [title] | [blog / product / category / tool / other kind] | [yes / consumer / local / brand / other meaning] |

## Counts

| Label | Count | Example URL |
|-------|-------|-------------|
| blog | [n] | [url] |
| [label] | [n] | [url] |

- Blog share: blog [n]/[organic count] = [n]%
- Off topic: [n] of [organic count]

## Reader Task

The searcher wants to [one sentence].

## SERP Features

| Feature | Result |
|---------|--------|
| AI Overview | [present or none] |
| Featured snippet | [present or none] |

An absent feature is not evidence of low demand or weak competition.

## Decision

| Rule | Result |
|------|--------|
| Blog share below 30% (internal rule, not a Google standard) | [yes / no] |
| Tool count equal to or above blog count | [yes / no] |
| Off topic 5 or more | [yes / no] |

- Decision: [continue / stop]
- Page type that fits the SERP: [blog / product page / category page / tool page / another keyword]
- User choice: [not needed / pending / write anyway / another keyword / end]
