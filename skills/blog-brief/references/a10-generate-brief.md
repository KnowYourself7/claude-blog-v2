### Step 5: Generate the Brief

Read `templates/brief-template.md` and fill it in section
by section, keeping its order. Rules while filling it:

- **Template file** line: resolve `../blog/templates/[type].md`
  to an absolute path.
- **Target Keywords**: copy the focus keyword and its data from the Step 2
  keyword research file, and link to that file. Keep `null` as `null`. Never
  estimate a value.
- **Content Outline**: cover each kept Step 2 facet in at least one H2.
  One H2 can cover more than one facet. The facet order does not set the
  H2 order. Write the facet IDs in each H2.
- **Experience / E-E-A-T**: include first-hand insight, a case study, or test
  results only when the user supplies supporting methodology, evidence, and
  results; otherwise use differentiated sourced synthesis without implying
  personal experience.
- **Statistics**: only those that passed the Step 4 provenance rules.
- **Competitive Gaps**: copy the Gap List into item 1 and Our
  Difference into item 2 from the Step 3 file, and link to that file.
  Take item 3 from the Experience rows of that file; write `none` if no
  format is missing. Do not add a gap that is not in the file.
- **Generated SVG covers**: sanitize to remove scripts and event attributes, or
  rasterize to PNG before publishing.
- **FAQ**: optional, 3-5 items, not a Google rich-result target.
