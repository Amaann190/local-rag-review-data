"""Apply the sensitivity re-screen of Stage-1 exclusions made without a full abstract.

Records re-screened as include/unsure advance to Stage 2 (same either-advance rule). Their Stage-2 decisions
were made by the authors against eligibility_codebook.md and are recorded here.
"""
import csv, pathlib

H = pathlib.Path(__file__).parent
STAGE2 = {
    "R0242": ("no", "no_evidence", "", "no", "Title only; no evaluation verifiable [sensitivity re-screen]"),
    "R0318": ("yes", "included", "F6", "yes", "Scoping review mapping RAG retrieval and evaluation designs [sensitivity re-screen]"),
    "R0321": ("yes", "included", "F6", "yes", "Scoping review of RAG evaluation approaches in nursing [sensitivity re-screen]"),
    "R0374": ("no", "no_core_facet", "", "yes", "Domain application; RAG vs no-RAG only, no facet studied [sensitivity re-screen]"),
    "R0865": ("no", "no_evidence", "", "no", "Title only; no evaluation verifiable [sensitivity re-screen]"),
    "R1441": ("no", "no_core_facet", "", "yes", "Domain application; RAG vs prompting only, no facet studied [sensitivity re-screen]"),
    "R1724": ("no", "no_evidence", "", "no", "Title only; offline retrieval claim not verifiable [sensitivity re-screen]"),
    "R1876": ("no", "no_core_facet", "", "yes", "Reliability check of one RAG tool; not a RAG evaluation framework [sensitivity re-screen]"),
}
resc = {r["record_id"]: r for r in csv.DictReader(open(H / "audit" / "sensitivity_rescreen.csv", encoding="utf-8"))}
advanced = {i for i, r in resc.items() if r["decision"].strip().lower() in ("include", "unsure")}
assert advanced == set(STAGE2), (sorted(advanced), sorted(STAGE2))

rows = list(csv.DictReader(open(H / "eligibility_final.csv", encoding="utf-8")))
cols = list(rows[0].keys())
have = {r["record_id"] for r in rows}
for i, (el, reason, fac, ev, note) in STAGE2.items():
    if i not in have:
        rows.append({"record_id": i, "eligible": el, "exclusion_reason": reason, "facets": fac, "evidence": ev, "note": note})
rows.sort(key=lambda r: r["record_id"])
with open(H / "eligibility_final.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print("eligibility rows", len(rows), "eligible", sum(r["eligible"] == "yes" for r in rows))
