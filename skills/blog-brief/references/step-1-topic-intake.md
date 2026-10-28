### Step 1: Topic Intake

Before any research, get clear on what to write, for whom, what the
brand can say, and what this run can spend.

#### Tools

- The user, and `BRAND.md` when SKILL.md loaded it through the fenced
  helper. No API, no web page.

#### Inputs

The four groups below are the four tables of the task brief.

- Topic: focus keyword, working title, market, the decision that the
  reader is making, who the readers are.
- Business: brand, domain, what it sells, what it does not sell or
  must not claim, first-party material that it can publish.
- Existing Pages and Page: each existing page of the site, the page
  that this post supports, the next step for the reader.
- Delivery: positioning, role, deliverable, scope and publishing
  approval, API budget, author and platform.

#### Actions

1. Make the slug from the focus keyword: lowercase, only `a` to `z`,
   `0` to `9`, and one hyphen between words. Then run
   `brief_state.py init --slug [slug] --focus "[focus keyword]"`
   (SKILL.md, State File).
2. Fill `templates/task-brief.md` as `briefs/[slug]-task-brief.md`.
   Write `missing` in a cell when the user and `BRAND.md` give
   nothing. When both give a value, use the value of the user. When
   only `BRAND.md` gives a value, add `(from BRAND.md)` after it.
3. If the user gives no market, write `2840 / en, default` in Market.
   2840 is the DataForSEO location code of the United States, `en` is
   the language code.
4. Write each warning of the user in Does not sell or claim. Write
   each statement without proof there too, as
   `claim, no proof given: [the claim]`.
5. Write one row in Existing Pages for each page that the user gives.
   Write `missing` in Covers or Type when the user did not give it.
   When the Covers cell of a page names the same reader decision,
   write its URL and `ask` in Existing post on this topic.
6. When Positioning, Role, or Deliverable has no value from the user,
   draft it from Reader decision, Reader, and Sells. Start a drafted
   value with `draft:`. A drafted Role is `standalone`. Never draft
   Scope, API budget, or Author and platform.
7. Save the file. If it has a `draft:` value, an `ask`, or `missing`
   in a Page row, stop. A Page row is Page this post supports or
   Reader next step. Ask the user in one message. Show each draft and
   ask the user to accept or
   change it. For each `ask` row, ask: new post, update that page, or
   new angle. For Page this post supports and Reader next step, ask
   for a value, or write `missing, the user has none`. List the other
   `missing` cells and ask the user to fill them or to say that none
   exists. If a draft or an `ask` gets no answer, ask again.

#### Outputs

- `briefs/[slug]-task-brief.md`
- `briefs/[slug]-state.json`, created by `init` in action 1

#### Rules

- Do not infer a brand fact. Write `missing` and ask once, because an
  invented capability, certificate, patent, or case becomes a false
  claim in the post.
- A statement is a claim until the user gives proof. A claim never
  enters the Sells row.
- A draft is a proposal. Only the user turns it into a value.
- Do not ask for the search intent. Step 2 reads it from the SERP.

#### Example

Ebestron, task brief:

- Focus keyword `2k dispensing problems`, title "7 common faults of
  two-part dispensing".
- Client Ebestron, adhesivespackage.com, industrial packaging
  supplies: cartridges, glue guns, static mixers, needles.
- Does not sell or claim: glue formulas. Do not present it as a glue
  maker. Do not blame every fault on the hardware to sell parts.
- Positioning `draft:` a troubleshooting post that leads buyers of
  dispensing supplies to the matching products. Deliverable `draft:`
  a table of 7 faults, about 2.8K words. Role `draft:` standalone.
- Reader, First-party material, Existing Pages, Page this post
  supports, Reader next step, Scope, API budget, Author and platform:
  `missing`.
- Result: saved, then one stop for three drafts and two missing Page
  values.

#### Check

- No `draft:` value, no `ask`, every cell filled or `missing`.
- Nothing in Topic or Business comes from outside the user and
  `BRAND.md`.
- Page this post supports and Reader next step have a user value, or
  `missing, the user has none`.
