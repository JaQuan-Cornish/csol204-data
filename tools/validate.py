"""Validate csol204-data company files.

Usage:
    python tools/validate.py                 # check every company
    python tools/validate.py microsoft       # check one company
Exits with code 1 if any error is found. Warnings don't fail the check.
"""
import csv, sys, os, re
from collections import Counter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "companies")

HEADERS = {
    "emissions.csv": ["company_slug", "reporting_entity", "period_label", "period_end", "period_type",
                      "scope", "scope3_category", "scope2_method", "status", "value_tco2e",
                      "value_original", "unit_original", "is_total", "restated", "method_note",
                      "source_doc", "source_url", "source_page", "source_quote"],
    "financials.csv": ["company_slug", "reporting_entity", "period_label", "period_end", "period_type",
                       "revenue_value", "currency", "unit_multiplier", "source_doc", "source_url",
                       "source_page", "source_quote"],
    "segments.csv": ["company_slug", "reporting_entity", "period_label", "split_type", "split_label",
                     "metric_type", "value", "unit", "additive", "source_doc", "source_url",
                     "source_page", "source_quote"],
}
SITES_HEADER = ["company_slug", "reporting_entity", "site_id", "site_name", "site_type", "activity", "country",
                "latitude", "longitude", "location_precision", "coord_source", "status", "source_doc",
                "source_url", "source_page", "source_quote", "note"]
STATUSES = {"reported", "not_relevant", "not_estimated", "not_disclosed"}
CATS = {str(i) for i in range(1, 16)} | {"total", ""}


def num(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def check_company(slug):
    errs, warns = [], []
    folder = os.path.join(ROOT, slug)
    for fname, header in HEADERS.items():
        path = os.path.join(folder, fname)
        if not os.path.exists(path):
            errs.append(f"{slug}/{fname}: file missing")
            continue
        with open(path, newline="", encoding="utf-8") as f:
            try:
                rows = list(csv.reader(f, strict=True))
            except csv.Error as e:
                errs.append(f"{slug}/{fname}: CSV parse error: {e}")
                continue
        if not rows or rows[0] != header:
            errs.append(f"{slug}/{fname}: header doesn't match SCHEMA.md")
            continue
        for i, r in enumerate(rows[1:], start=2):
            if len(r) != len(header):
                errs.append(f"{slug}/{fname} line {i}: {len(r)} fields, expected {len(header)}")
                continue
            d = dict(zip(header, r))
            if d["company_slug"] != slug:
                errs.append(f"{slug}/{fname} line {i}: company_slug '{d['company_slug']}' != folder '{slug}'")
            if fname == "emissions.csv":
                if d["scope"] not in {"1", "2", "3"}:
                    errs.append(f"{slug}/{fname} line {i}: scope must be 1, 2 or 3")
                if d["status"] not in STATUSES:
                    errs.append(f"{slug}/{fname} line {i}: status '{d['status']}' not in {sorted(STATUSES)}")
                if d["scope"] == "2" and d["scope2_method"] not in {"location", "market"}:
                    errs.append(f"{slug}/{fname} line {i}: Scope 2 rows need scope2_method location or market")
                if d["scope"] == "1" and d["scope2_method"] not in {"", "market"}:
                    errs.append(f"{slug}/{fname} line {i}: Scope 1 rows leave scope2_method blank (or 'market' for a company's market-based Scope 1)")
                if d["scope"] == "3" and d["scope2_method"]:
                    errs.append(f"{slug}/{fname} line {i}: Scope 3 rows leave scope2_method blank")
                if d["scope"] == "3" and d["scope3_category"] not in CATS - {""}:
                    errs.append(f"{slug}/{fname} line {i}: Scope 3 rows need scope3_category 1-15 or total")
                if d["status"] == "reported":
                    if not num(d["value_tco2e"]):
                        errs.append(f"{slug}/{fname} line {i}: reported row needs a numeric value_tco2e")
                    if not d["source_page"] or not (d["source_url"] or d["source_doc"]):
                        errs.append(f"{slug}/{fname} line {i}: reported row needs source_doc/source_url and source_page")
                elif d["value_tco2e"]:
                    errs.append(f"{slug}/{fname} line {i}: status '{d['status']}' must have a blank value (missing is not zero)")
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", d["period_end"] or ""):
                    warns.append(f"{slug}/{fname} line {i}: period_end should be YYYY-MM-DD")
            else:
                vcol = "revenue_value" if fname == "financials.csv" else "value"
                if not num(d[vcol]):
                    errs.append(f"{slug}/{fname} line {i}: {vcol} must be numeric")
                if not d["source_page"]:
                    errs.append(f"{slug}/{fname} line {i}: source_page missing")
        if fname == "emissions.csv" and len(rows) > 1:
            keys = Counter((r[1], r[2], r[5], r[6], r[7]) for r in rows[1:] if len(r) == len(header))
            for k, c in keys.items():
                if c > 1:
                    errs.append(f"{slug}/{fname}: duplicate row for entity/period/scope/category/method {k}")
    e2, w2 = check_sites(slug, folder)
    return errs + e2, warns + w2


def check_sites(slug, folder):
    """Optional Lab 3 file: places where the company meets nature."""
    errs, warns = [], []
    path = os.path.join(folder, "sites.csv")
    if not os.path.exists(path):
        return errs, warns
    with open(path, newline="", encoding="utf-8") as f:
        try:
            rows = list(csv.reader(f, strict=True))
        except csv.Error as e:
            return [f"{slug}/sites.csv: CSV parse error: {e}"], warns
    if not rows or rows[0] != SITES_HEADER:
        return [f"{slug}/sites.csv: header doesn't match SCHEMA.md"], warns
    seen = Counter()
    for i, r in enumerate(rows[1:], start=2):
        if len(r) != len(SITES_HEADER):
            errs.append(f"{slug}/sites.csv line {i}: {len(r)} fields, expected {len(SITES_HEADER)}")
            continue
        d = dict(zip(SITES_HEADER, r))
        where = f"{slug}/sites.csv line {i}"
        if d["company_slug"] != slug:
            errs.append(f"{where}: company_slug '{d['company_slug']}' != folder '{slug}'")
        if d["site_type"] not in {"own_operation", "supplier", "sourcing_region", "other"}:
            errs.append(f"{where}: site_type must be own_operation, supplier, sourcing_region or other")
        if d["status"] == "located":
            if not (num(d["latitude"]) and num(d["longitude"])):
                errs.append(f"{where}: located rows need numeric latitude and longitude")
            elif not (-90 <= float(d["latitude"]) <= 90 and -180 <= float(d["longitude"]) <= 180):
                errs.append(f"{where}: coordinates out of range")
            if d["location_precision"] not in {"exact", "approximate", "region"}:
                errs.append(f"{where}: location_precision must be exact, approximate or region")
            if not d["coord_source"]:
                errs.append(f"{where}: coord_source missing")
        elif d["status"] == "not_located":
            if d["latitude"] or d["longitude"]:
                errs.append(f"{where}: not_located rows keep latitude and longitude blank")
        else:
            errs.append(f"{where}: status must be located or not_located")
        if not d["source_page"] or not (d["source_doc"] or d["source_url"]):
            errs.append(f"{where}: needs source_doc or source_url, and source_page")
        seen[(d["reporting_entity"], d["site_name"])] += 1
    for k, c in seen.items():
        if c > 1:
            warns.append(f"{slug}/sites.csv: '{k[1]}' appears {c} times for {k[0]}")
    return errs, warns


def main():
    slugs = sys.argv[1:] or sorted(d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)))
    all_errs = 0
    for s in slugs:
        errs, warns = check_company(s)
        status = "OK" if not errs else f"{len(errs)} error(s)"
        print(f"{s}: {status}" + (f", {len(warns)} warning(s)" if warns else ""))
        for e in errs:
            print("  ERROR", e)
        for w in warns[:5]:
            print("  warn ", w)
        all_errs += len(errs)
    sys.exit(1 if all_errs else 0)


if __name__ == "__main__":
    main()
