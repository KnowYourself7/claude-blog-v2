<!-- Output template for the blog-brief skill (Step 3, items 7 to 12).
     Fill every [bracket] and keep the section order. The rules for
     filling it are in ../references/step-3-demand-facets.md. -->

# Demand Facets: [focus keyword]

| Item | Value |
|------|-------|
| Focus keyword | [keyword] |
| Date | [YYYY-MM-DD] |
| Keyword evidence | `briefs/[slug]-keyword-research.md` |
| Business scope | `briefs/[slug]-task-brief.md` |
| Related Keywords | [not called / called in Step 3 item 10] |

## Focus Keyword

Rows that restate the focus keyword: pool [n], [n]. other [n].

## Kept Facets

Copy this table and the Other Facets table from
`briefs/[slug]-facet-tables.md`, written by `scripts/keyword_pool.py`.
Each kept facet goes into at least one H2 of the brief. The table goes
from the highest evidence count to the lowest. For equal counts, it goes
from the highest volume to the lowest, with `-` after the volumes. If
volumes are equal too, the order of the keyword file stays. This order
does not set the H2 order. Evidence numbers are the `#` in Question Evidence. Rows are the
`#` in the Keyword Pool and in Other Sources. Search volume, KD, and
intent are the values of the representative keyword only.

| ID | Reader question | Values | Evidence | Evidence types | Representative keyword | Search volume | KD | Intent | Rows | Reason kept |
|----|-----------------|--------|----------|----------------|------------------------|---------------|----|--------|------|-------------|
| F1 | [one full question] | [values, or -] | [evidence numbers, or -] | [1-6] | [keyword or -] | [n, null, or -] | [0-100, null, or -] | [main_intent, null, or -] | pool [n], [n]. other [n] | [one sentence] |

## Other Facets

The post does not cover these facets.

| ID | Reader question | Evidence | Rows | Reason not kept |
|----|-----------------|----------|------|-----------------|
| F[n] | [one full question] | [evidence numbers, or -] | [rows, or -] | [other page / outside business / lower rank] |

## Keyword Check

| Check | Result |
|-------|--------|
| First 50 pool rows | [n] attached to a facet, [n] restate the focus keyword, [n] other page |
| New facets from keyword rows | [n] |
| Other Sources rows | [n] attached, [n] other page, of [n] |
