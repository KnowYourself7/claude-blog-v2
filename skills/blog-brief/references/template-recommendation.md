### Step 2.5: Template Recommendation

Recommend one of 12 content templates from the Step 1.5 results and the Step 2
keyword research. Load `../blog/references/content-templates.md` for selection
criteria.

**Available templates:**
| Template | Best For |
|----------|----------|
| `how-to-guide` | Step-by-step instructional content |
| `listicle` | Curated lists, ranked items, resource roundups |
| `case-study` | In-depth analysis of a specific example or result |
| `comparison` | Side-by-side evaluation of 2+ options |
| `pillar-page` | Comprehensive topic hub linking to cluster content |
| `product-review` | Detailed evaluation with pros/cons/verdict |
| `thought-leadership` | Expert opinion, industry trends, predictions |
| `roundup` | Expert quotes, tool collections, best-of lists |
| `tutorial` | Technical walkthrough with code/config examples |
| `news-analysis` | Timely coverage with expert commentary |
| `data-research` | Original data, survey results, benchmark findings |
| `faq-knowledge` | Question-driven reference content |

**Selection process:**
1. Use the format that most Step 1.5 `blog` titles have: a number of items
   or "ideas" (`listicle`), "how to" (`how-to-guide`), "vs" (`comparison`),
   "best" (`roundup`), or a question (`faq-knowledge`). If titles tie or show
   no format, use the format that more Step 2 keywords show. If neither shows
   one, ask the user.
2. Use another format only when the user's assets need it, and say why.
3. Load the matching template file from `../blog/templates/[type].md`
4. Include the template name in the brief output, with the title counts as
   the rationale.
