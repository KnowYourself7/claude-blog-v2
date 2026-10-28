### Step 5: Template Recommendation

A content template is one of the 12 post structures in
`../blog/references/content-templates.md`. Choose one from the format
of the pages that rank.

#### Tools

- `../blog/references/content-templates.md`: the 12 content templates
  and what each is for.

#### Inputs

- The Reader Task, from `briefs/[slug]-search-intent.md`.
- The Structure section (the H2 list) of each
  `briefs/[slug]-competitor-[n].md`. This is the format of the page.

#### Actions

1. Read the Reader Task. Then read the Structure section of each
   competitor. Write the format that most pages share in two or three
   words, for example `guide in sections` or `numbered list`. If no
   two pages share a format, write `mixed`.
2. Choose the content template that fits that format and the Reader
   Task. If the format is `mixed`, choose from the Reader Task and
   say so in the reason. Write the reason in one sentence.
3. Read `../blog/templates/[template name].md`, for example
   `../blog/templates/how-to-guide.md`, to make sure that its
   sections fit the Reader Task.
4. Write the note text `Template: [name]. Reason: [sentence]`. Use it
   as the `--note` of the done command (SKILL.md, State File).

#### Outputs

- No file. The note of Step 5 in `briefs/[slug]-state.json` holds the
  content template and the reason. Step 9 copies them into the
  Template section of the brief.

#### Rules

- Choose from the ranking pages, not from the demand facets or the
  words of a title. A question in a title is not a FAQ page.

#### Example

Coofandy, `can you wear linen in winter` (the Ebestron case has no
format conflict):

- Five ranking pages are guides in sections: layering, items,
  occasions.
- Two titles are questions, and the kept facets are questions too.
  Neither is a format signal.
- Choice: `how-to-guide`, not `faq-knowledge`.

#### Check

- One content template is chosen.
- The reason names the format of the ranking pages.
- The note text has `Template: [name]` and `Reason: [one sentence]`.
