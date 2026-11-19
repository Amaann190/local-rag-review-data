"""Author adjudication of the audit coding (two coders applied the numeric-inconsistency rule differently).

Strict rule applied to all 54 full-text rows: 'yes' only when the same quantity takes two different values in the
same paper, or a stated arithmetic does not hold. Claim-vs-number contradictions, rounding, unit formatting,
and suspicious-but-consistent numbers are 'no'.
"""
import csv, pathlib

A = pathlib.Path(__file__).parent
OVERRIDES = {
    # record_id: {column: (new_value, reason)}
    "R1242": {"numeric_inconsistency": ("yes", "model-capacity threshold given as 7B and as 3.8B"),
              "inconsistency_detail": ("Capacity threshold stated as 7B in one place and 3.8B in another.", "")},
    "R1598": {"numeric_inconsistency": ("no", "2.49 vs 2.5 is rounding; 'consistently improves' is a claim, not a numeric conflict")},
    "R1667": {"numeric_inconsistency": ("no", "unattributed bound and significance wording are not numeric conflicts")},
    "R1898": {"numeric_inconsistency": ("no", "omitted model run and validity wording are not numeric conflicts")},
    "R2025": {"numeric_inconsistency": ("no", "headline equals best per-table value; identical values are suspicious, not conflicting")},
    "R2783": {"numeric_inconsistency": ("no", "0.94% is a unit-format slip; 'about seven times' approximates 7.8")},
    "R2813": {"numeric_inconsistency": ("no", "'largest gains' is a claim contradicted by numbers, not a numeric conflict")},
    "R2949": {"numeric_inconsistency": ("no", "abstract framing vs table is a claim contradiction")},
    "R1255": {"rag_pipeline": ("no", "notes state no LLM is in the evaluated loop")},
    "R1642": {"judge_location": ("cloud_llm", "notes state Gemini API judged outputs")},
}
rows, order = {}, []
for p in sorted(A.glob("audit_part*.csv")):
    for r in csv.DictReader(open(p, encoding="utf-8")):
        rows[r["record_id"]] = r
        order.append((p, r["record_id"]))
log = []
for rid, ch in OVERRIDES.items():
    for col, (val, why) in ch.items():
        old = rows[rid][col]
        rows[rid][col] = val
        if col != "inconsistency_detail":
            log.append(f"| {rid} | {col} | {old} | {val} | {why} |")
    if rows[rid]["numeric_inconsistency"] == "no":
        rows[rid]["inconsistency_detail"] = ""
for p in sorted(A.glob("audit_part*.csv")):
    ids = [rid for (pp, rid) in order if pp == p]
    cols = list(rows[ids[0]].keys())
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for rid in ids:
            w.writerow(rows[rid])
(A / "ADJUDICATION.md").write_text(
    "# Audit adjudication\n\nTwo coders coded 54 rows each. Their numeric-inconsistency rates differed sharply "
    "(3/24 vs 26/30 full-text rows), so the authors re-applied one strict rule to all 54 full-text rows "
    "(see `adjudicate.py`). Changes:\n\n| Record | Column | Coder | Final | Reason |\n|---|---|---|---|---|\n"
    + "\n".join(log) + "\n", encoding="utf-8")
ft_yes = sorted(r for r in rows if rows[r]["numeric_inconsistency"] == "yes")
print("numeric_inconsistency yes:", len(ft_yes), ft_yes)
