"""Record an explicit exclusion reason for every Stage-2 record, including the authors' own prior version.

Reason codes (assigned facet-first, in this order, to every record that is not eligible):
  included            eligible
  authors_prior       the authors' own earlier version of this review (R2064)
  no_core_facet       facets empty: main contribution addresses none of F1-F6
  no_evidence         a facet is present but evidence=no (no quantitative evaluation and no explicit-search survey)
  out_of_scope        a facet is present and evidence=yes, but the record is still ineligible
                      (e.g. prompt injection not specific to RAG, generic quantization, pure IR without RAG framing)
"""
import csv, pathlib

H = pathlib.Path(__file__).parent
rows = list(csv.DictReader(open(H / "eligibility_final.csv", encoding="utf-8")))
for r in rows:
    if r["record_id"] == "R2064":
        r["eligible"] = "no"
        r["exclusion_reason"] = "authors_prior"
        r["note"] = "Authors' own earlier version of this review (ResearchGate); excluded as prior version"
    elif r["eligible"].strip().lower() == "yes":
        r["exclusion_reason"] = "included"
    elif not r.get("facets", "").strip():
        r["exclusion_reason"] = "no_core_facet"
    elif r.get("evidence", "").strip().lower() == "no":
        r["exclusion_reason"] = "no_evidence"
    else:
        r["exclusion_reason"] = "out_of_scope"
cols = ["record_id", "eligible", "exclusion_reason", "facets", "evidence", "note"]
with open(H / "eligibility_final.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in cols})
from collections import Counter
print(Counter(r["exclusion_reason"] for r in rows))
