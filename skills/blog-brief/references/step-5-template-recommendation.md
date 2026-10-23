### Step 4: Template Recommendation

#### Goal

Choose one of the 12 content templates for this post.

#### Inputs

- `../blog/references/content-templates.md`: the selection criteria.
- `briefs/[slug]-search-intent.md`: the `blog` titles.
- `briefs/[slug]-keyword-research.md`: the keywords, for a tie.

#### Rules

- Choose one template. Use another format only when the assets of the
  user need it, and say why.
- If neither the titles nor the keywords show a format, ask the user.

#### Steps

1. Count the formats of the `blog` titles: a number of items or
   "ideas" is `listicle`, "how to" is `how-to-guide`, "vs" is
   `comparison`, "best" is `roundup`, and a question is
   `faq-knowledge`.
2. Take the format with the most titles. On a tie, or when no title
   shows a format, take the format that more Step 3 keywords show.
3. Read `../blog/templates/[type].md` for the chosen template.

The 12 templates:

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

#### Outputs

- No file. The template name and the title counts go into the
  Template section of the brief in Step 7.

#### Check

- One template is chosen, with the counts that decided it.
- The name and the counts are ready for the Template section of the
  brief.
