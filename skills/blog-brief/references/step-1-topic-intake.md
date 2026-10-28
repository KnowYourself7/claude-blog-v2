### Step 1: Topic Intake

#### Goal

Turn the words of the user into a task brief: who the post is for,
what the brand can say, which page it serves, and what this run
delivers. The only sources are the user and `BRAND.md`. This step
calls no API and opens no web page.

#### Inputs

- `templates/task-brief.md`: the output template.
- `BRAND.md`, if SKILL.md loaded it: brand facts and the Audience
  section.

#### Rules

- Take brand facts and the Reader row only from the user and
  `BRAND.md`. If both give a value, use the user, because the user
  is the newer source.
- Do not infer a brand fact, and do not open any website or URL. Only
  the client knows what the client can say.
- Write no capability, certificate, patent, case, or test data that
  the user did not give. An invented one becomes a false claim in the
  post. Write `missing` and let the user fill it.
- A statement without proof is a claim, not a fact. Write it in the
  Does not sell or claim row as `claim, no proof given: [the claim]`,
  nowhere else, so the writer sees it as a limit, not as evidence.
- A draft is a Positioning, Role, or Deliverable that you wrote
  because the user did not give it. The user accepts or changes it,
  because these decide what the whole brief is for.
- Do not ask for the search intent. Step 2 reads it from the SERP,
  which is more reliable than a guess.

#### Steps

1. Fill the Topic table. If the user names no market, write 2840 / en
   and `default`. Infer the Reader decision from the focus keyword if
   the user did not give it.
2. Make the slug from the focus keyword: lowercase, accented letters to
   plain, delete every character except `a` to `z`, `0` to `9`, space,
   and hyphen, then join with single hyphens. If nothing remains, ask
   the user for an English slug.
3. Fill the Business table. Put each warning that the user gives about
   the content in the Does not sell or claim row. First-party material
   is material that the brand owns and can publish, for example test
   data or a spec sheet. Write each item and where it is.
4. Fill the Existing Pages table from the pages that the user gives.
   Do not infer a type from a URL. A URL path often lies.
5. Fill the Page table. For the Existing post on this topic row, judge
   from the Covers cells only, because you do not open pages. If a
   page answers the Reader decision, write its URL and `ask`. A new
   post on the same question competes with the old one for the same
   search, so the user must choose. Otherwise write `none in the
   list`, or `missing` if there is no list.
6. Fill the Delivery table. A Positioning is given only if the user
   named the type of post, the reader, and the job for the brand. A
   Deliverable is given only if the user named the thing and its size
   (a count or a length). If not given, draft it from the Reader
   decision, the Reader row, and the Sells row. Keep the parts that
   the user gave. A drafted Role is `standalone`. Never draft Scope,
   API budget, or Author and platform.
7. Save the task brief. Stop if any value is a draft, if a row ends
   with `ask`, or if Page this post supports or Reader next step is
   `missing`. Without a supported page and a next step, nothing ties
   the post to the business. Ask in one message, so the user answers
   once: show the drafts, ask for the missing Page values, and for
   each `ask` page ask: new post, update it, or new angle. Then list
   every other `missing` cell as optional. Write the answers in. If a
   draft or an `ask` gets no answer, ask again.

#### Outputs

- `briefs/[slug]-task-brief.md`
- `briefs/[slug]-state.json`, created by `init` (SKILL.md, State File)

#### Check

- No cell is empty, no value starts with `draft:`, no row ends with
  `ask`.
- No brand fact, claim, or Reader value comes from outside the user
  and `BRAND.md`. Claims carry `no proof given`.
- The Positioning names the type, the reader, and the job for the
  brand. The Deliverable names a thing the reader can use.
- Page this post supports and Reader next step have a user value or
  `missing, the user has none`.

#### Example

Input, the words of the user: focus keyword `2k dispensing problems`,
title "7 common faults of two-part dispensing". Client Ebestron,
adhesivespackage.com, industrial packaging supplies: cartridges, glue
guns, static mixers, needles. It does not make glue formulas, so do
not present it as a glue maker. Do not blame every fault on the
hardware to sell parts. A troubleshooting post that leads readers to
the matching products, about 2.8K words, 7 fault topics. No
`BRAND.md`.

Output, the task brief:

| Row | Value | Source |
|---|---|---|
| Focus keyword, Working title | 2k dispensing problems, 7 common faults of two-part dispensing | the user |
| Slug, Market | 2k-dispensing-problems, 2840 / en, default | items 1 and 2 |
| Reader decision | what causes a two-part dispensing fault, and how to fix it | inferred |
| Brand, Domain, Sells | Ebestron, adhesivespackage.com, industrial packaging supplies: cartridges, glue guns, static mixers, needles | the user |
| Does not sell or claim | glue formulas. Do not present Ebestron as a glue maker. Do not blame every fault on the hardware. | the user |
| Positioning | draft: A troubleshooting post for buyers of dispensing supplies leads them to the matching products. | the user gave the type and the job, the reader is drafted |
| Role | draft: standalone | drafted |
| Deliverable | draft: A table of 7 faults with the symptom, the cause, and the part to fix, about 2.8K words. | the user gave the size, the thing is drafted |
| Every other row | missing | the user gave none |

Result: the step saves the brief and stops, because of three drafts
and two missing Page values. One message shows the drafts, asks for
the supported page and the reader next step, and lists the other
`missing` cells as optional.
