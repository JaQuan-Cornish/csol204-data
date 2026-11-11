# Adding data (Labs 2 and 3)

**Lab 3:** every team adds its company's places to `sites.csv` (see "Lab 3: adding sites" at the end). You don't owe another emissions series.

**Lab 2:** every team adds at least one **cited series**: one measure for at least two periods (for example Scope 3 Category 11 for FY2021 and FY2022, emissions by region, or an earlier year's Scope 2), sourced to a page in a company document.

## Steps

1. **Find the number** in a company document (sustainability report, data book, CDP response, 10-K). Note the document title, URL and page.
2. **Fork** this repo on GitHub (button at top right).
3. **Edit** `companies/<slug>/emissions.csv` (or `segments.csv`, `financials.csv`). Add rows; don't change other teams' rows. If you find an error in an existing row, fix it and explain in the pull request.
4. **Check** it: `python tools/validate.py <slug>`.
5. **Open a pull request.** Fill in the template: what you added, the sources, and the checklist. A person on your team must have opened every source page.
6. The check runs on your pull request. Fix any errors it reports. The instructor merges it.

## Example: two rows a team might add

```csv
microsoft,Microsoft Corporation,FY2021,2021-06-30,fiscal,2,,location,reported,4300000,"4,300,000",mtCO2e,y,n,"Example only, not a real value.",Microsoft 2022 Environmental Data Fact Sheet,https://example.com/report.pdf,pdf 4,"Scope 2: Location-based (FY21)"
microsoft,Microsoft Corporation,FY2021,2021-06-30,fiscal,3,11,,not_relevant,,,,n,n,"Company states category not relevant.",Microsoft 2022 Environmental Data Fact Sheet,https://example.com/report.pdf,pdf 5,"Category 11 not applicable"
```

(The values above are made up to show the format. Don't copy them.)

## Using AI to help

An AI agent can find candidate numbers and draft rows. A person must open the page and check every value before the pull request. Log each AI-supplied number in your lab repo's `audit/ai_audit.csv`.

## Lab 3: adding sites

Every Lab 3 team adds its company's **places** to `companies/<slug>/sites.csv` (create the file with the header in `SCHEMA.md` if it doesn't exist yet). Include `not_located` rows for places a source names but you couldn't find coordinates for: they show the next team where the gaps are. (An activity with no named place isn't a row; it goes in your write-up.) Use your own `site_id`s; if one is already taken in this file for a different place, renumber yours. Your lab notebook writes your rows in this format to `outputs/sites_for_pr.csv`. Then follow steps 2–6 above: fork, add rows, `python tools/validate.py <slug>`, open a pull request. A person on your team must have opened every source page and checked the coordinates.
