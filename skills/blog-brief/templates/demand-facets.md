<!-- Output of blog-brief Step 3, action 7 (../references/step-3-demand-facets.md).
     Fill every [bracket] and keep the section order. -->

# Demand Facets: [focus keyword]

| Item | Value |
|------|-------|
| Focus keyword | [keyword] |
| Date | [YYYY-MM-DD] |
| Keyword evidence | `briefs/[slug]-keyword-research.md` |
| Business scope | `briefs/[slug]-task-brief.md` |
| Rounds | [1 or 2] |

## Kept Facets

Copy this table, its AI search volume line, and the Other Facets table
from `briefs/[slug]-facet-tables.md`, written by `scripts/keyword_pool.py`.
Each kept facet goes into at least one H2 of the brief. The table goes
from the highest source count to the lowest, then from the highest
volume to the lowest, `null` after the volumes. This order does not set
the H2 order. Questions are the `#` in the questions file. Search
volume, KD, intent, and AI search volume are the values of the
representative keyword only: `null` means the API gave no value,
`-` means the facet has no attached row. Sources are source names. The
AI search volume is not a Google volume; do not add the two.

| ID | Reader question | Values | Representative keyword | Search volume | AI search volume | KD | Intent | Sources | Questions | Reason kept |
|----|-----------------|--------|------------------------|---------------|------------------|----|--------|---------|-----------|-------------|
| F1 | [one full question] | [values, or -] | [keyword or -] | [n, null, or -] | [n, null, or -] | [0-100, null, or -] | [intent, null, or -] | [source names] | [question numbers] | [one sentence] |

AI search volume: [the endpoint, market, and date line from the facet tables file]

## Other Facets

The post does not cover these facets.

| ID | Reader question | Questions | Reason not kept |
|----|-----------------|-----------|-----------------|
| F[n] | [one full question] | [question numbers, or -] | [outside business / lower rank] |
