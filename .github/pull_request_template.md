## What I added

- Company and file (Lab 2: emissions, segments or financials; Lab 3: sites.csv):
- Series (what it measures, which periods):
- Question it helps answer:

## Sources

- Document, year, URL and page for each value:

## Checks

- [ ] Every new row has `source_doc` or `source_url`, `source_page` and a short `source_quote`.
- [ ] Units converted to tCO2e (or the stated unit) and the original value and unit kept.
- [ ] Lab 3 sites: every located row has coordinates with a `coord_source`; sourcing regions are marked `region`; places a source names but we couldn't find are `not_located` with blank coordinates; every row has a `source_type`, and a non-company source quotes the company link.
- [ ] A person on our team opened each source page and checked each value.
- [ ] Lab 3 sites: our `site_id`s don't reuse an id already in the file for a different place.
- [ ] `python tools/validate.py <company>` passes.
