## What I added

- Company and file (Lab 2: emissions, segments or financials; Lab 3: sites.csv):
- Series (what it measures, which periods):
- Question it helps answer:

## Sources

- Document, year, URL and page for each value:

## Checks

- [ ] Every new row has `source_doc` or `source_url`, `source_page` and a short `source_quote`.
- [ ] Units converted to tCO2e (or the stated unit) and the original value and unit kept.
- [ ] Lab 3 sites: every located row has coordinates with a `coord_source`; sourcing regions are marked `region`; places we couldn't find are `not_located` with blank coordinates.
- [ ] A person on our team opened each source page and checked each value.
- [ ] `python tools/validate.py <company>` passes.
