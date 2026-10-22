### Step 2: Keywords to Demand Facets

Turn the keywords of the topic into demand facets. A demand facet is one
part of the reader task. The reader task is the sentence that Step 1.5
wrote in `briefs/[slug]-search-intent.md`. Step 5 gives each kept facet
at least one H2.

In this step, you fill two templates:
`templates/keyword-research.md` for the keyword
evidence, and `templates/demand-facets.md` for the
facets. Take the volume, KD, and intent only from the DataForSEO Labs
responses. Write `null` for a missing value, not `0`. Do not add the
volumes of two keywords.

Use the Step 1.5 Live SERP response again. Send the other calls with
`mcp__dataforseo__api_request`. Use `noAiMode: true`, `location_code: 2840`,
and `language_code: "en"`. If the user names another market, use the codes
of that market. If a call fails two times, stop. Tell the user the reason.
Do not use WebSearch.

#### Evidence and keywords

1. Question evidence is the text that shows what readers ask. Copy four
   parts of it from the Step 1.5 response into the Question Evidence
   section: the AI Overview section titles (`ai_overview_element.title`),
   the PAA questions, the related searches, and the organic titles. Add
   the Step 1.5 label to each organic title.
2. Call `POST /v3/serp/google/autocomplete/live/advanced` one time for
   the focus keyword, with `client: "gws-wiz-serp"`. A modifier is a word
   that narrows the reader task, for example a color or an audience. Add
   these suggestions to the question evidence, as its fifth part: the
   questions, and the suggestions that add a modifier. Do not use the
   suggestions for volume.
3. Make two or three seeds. A seed is a keyword that you send to Keyword
   Suggestions. Seed 1 is the focus keyword. For seed 2, remove the
   modifiers from the focus keyword. If the focus keyword has no
   modifier, do not make seed 2. For seed 3, write another phrase for the
   same reader task. It must be shorter than the focus keyword. In the
   Seeds section, write how and why you made each seed.
4. Call `POST /v3/dataforseo_labs/google/keyword_suggestions/live` one
   time for each seed, with `limit: 300`.
5. Remove exact duplicates from the results. Ignore letter case.
6. Group the keywords by `core_keyword`, from `keyword_properties`. A
   keyword without `core_keyword` forms one group with the keywords that
   point to it. Each group is one row of the Keyword Pool.
7. In each row, the main keyword is the spelling with the highest volume.
   If volumes are equal, use the `core_keyword` spelling. If that spelling
   is not in the row, use the first spelling in the call order: seed 1,
   seed 2, seed 3.
8. Sort the rows of the Keyword Pool from the highest volume to the
   lowest. If volumes are equal, keep the call order.
9. Put the PAA questions and the related searches that are not in the
   Keyword Pool into the Other Sources table.
10. From both tables, remove the keywords that do not ask about the
    reader task of Step 1.5. The classes are other audience, other task, other
    meaning of the same word, store or platform navigation, and business
    conflict. Give each removed keyword the first class that applies, in
    this sequence. A product brand, for example nike, is not a store. If
    you are not sure, keep the keyword. Do not remove a keyword for its
    volume or intent. Give one reason for each class.
11. Call `POST /v3/dataforseo_labs/google/keyword_overview/live` for the
    related searches in the Other Sources table. If no related search
    stays in the table, do not call it.
12. Save the filled keyword template as
    `briefs/[slug]-keyword-research.md`.

#### Facets

13. List each item of the Question Evidence section.
14. Merge the items into facets. If two items differ only in one value,
    put them in one facet. For example, black and white linen pants
    differ only in the color. List the values in the facet.
15. If an item asks about another task, put it in the Other Facets table.
    Give the reason "other page".
16. Read the first 50 rows of the Keyword Pool and all rows of Other
    Sources. If a row restates the focus keyword, attach it to the focus
    keyword. If a row answers a facet, attach it to that facet. If a row
    names a new part of the reader task, add a facet for it. If a row
    fits no facet, mark it "other page".
17. For each facet, use the attached keyword with the highest volume as
    the representative keyword. If volumes are equal, use the row that
    comes first in the keyword file. Copy its volume, KD, and intent. If
    a facet has no attached keyword, write `-`.
18. Count the evidence types of each facet. There are six types: the five
    parts of Question Evidence, and the attached keyword rows. Sort the
    facets by this count, from high to low. If counts are equal, sort by
    the volume of the representative keyword. Put a facet with `-` after
    the facets with a volume. If volumes are also equal, keep the order
    of the keyword file.
19. Keep the first 9 facets. Put the others in the Other Facets table
    with the reason "lower rank".
20. If you keep fewer than 5 facets, call
    `POST /v3/dataforseo_labs/google/related_keywords/live` for the focus
    keyword with `depth: 2`. Read `core_keyword` from
    `keyword_data.keyword_properties`. Add the keywords to the Keyword
    Pool with items 5 to 8 and 10. Record the call in the Data Scope
    table. Save the keyword file again. Then do items 16 to 19 again. Do
    this item only one time.
21. If you keep fewer than 3 facets after item 20, stop. Tell the user
    that this keyword is possibly too narrow for one post. Ask the user
    to write anyway, try another keyword, or end.
22. Save the filled facet template as `briefs/[slug]-demand-facets.md`.
