"""Second adjudication pass: re-apply the ADJUDICATION.md numeric-inconsistency rule uniformly to every full-text row.

Rule: 'yes' only when the same quantity takes two materially different values in the same paper, or a stated
calculation does not hold. Rounding differences, unit/format slips, naming differences and claim-vs-number
contradictions are 'no'. Run after adjudicate.py; it edits audit_part*.csv in place and (re)writes the
'Round 2' section at the end of ADJUDICATION.md (idempotent).
"""
import csv, pathlib

A = pathlib.Path(__file__).parent
FLIPS = {  # record_id: (new numeric_inconsistency, reason)
    "R2269": ("no", "text '21%' matches the tables figure (21.4%) cited for steps; OOD4 5% vs 9% are different conditions (without vs with suggestions) and the rest are claims"),
    "R2570": ("no", "'additive' gains (0.31+0.21 vs 0.45) is a claim about the numbers, not a stated calculation; prompt-variant scores differ only by a configuration ambiguity"),
    "R2825": ("no", "4.4 vs 4.53 ms vs about 4.5 ms is rounding; 91-99% vs 0.91-1.00 is a format slip; '2-8 points' is a loose range claim"),
}
DETAIL_TRIMS = {  # non-qualifying items removed from inconsistency_detail; the verdict stays 'yes'
    "R1424": "Table 7 test-set n varies (259, 250, 244, 254) for the same set.",
    "R1642": "Table 5 MS MARCO success 96.8% but 1 minus 6.2% equals 93.8%; 'over 1,500' judged pairs vs 1,000 reported.",
    "R1719": "Miss-Strict-Rate at tau=0.50 is 87.5% (Table 4) vs 83.3% (Table 9).",
    "R1833": "EmbeddingGemma-300m described as 22.7M parameters.",
    "R1895": "Latency reduction 88% in Sec 6.2 vs 89.2% in Table 3.",
    "R2559": "SQuAD query counts 3,648/3,301 (Table 2) vs 3,646/3,148 (Fig 1); FiQA 230 vs 225 queries.",
    "R2247": "Chunking 300-word with 60 overlap in Sec 3.4 vs 500-word with 90 overlap in Sec 4.1.",
}
# Rows re-checked and left unchanged: R1898 and R2025 (no): their items are naming, claim-vs-number or
# suspicious-but-consistent values. All remaining 'yes' rows have a same-quantity conflict or a failed calculation.

rows, order, cols = {}, [], {}
for p in sorted(A.glob("audit_part*.csv")):
    for r in csv.DictReader(open(p, encoding="utf-8")):
        rows[r["record_id"]] = r
        order.append((p, r["record_id"]))
        cols[p] = list(r.keys())
log = []
for rid, (val, why) in FLIPS.items():
    old = rows[rid]["numeric_inconsistency"]
    if old != val:
        log.append(f"| {rid} | numeric_inconsistency | {old} | {val} | {why} |")
    rows[rid]["numeric_inconsistency"] = val
    rows[rid]["inconsistency_detail"] = ""
for rid, d in DETAIL_TRIMS.items():
    rows[rid]["inconsistency_detail"] = d
for p, c in cols.items():
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=c)
        w.writeheader()
        for pp, rid in order:
            if pp == p:
                w.writerow(rows[rid])

md = (A / "ADJUDICATION.md").read_text(encoding="utf-8")
md = md.split("\n## Round 2")[0].rstrip() + "\n"
if log:
    section = ("\n## Round 2: uniform re-check of every full-text 'yes'\n\n"
               "All full-text rows coded `yes` (and the `no` rows R1898 and R2025) were re-read against the rule above: "
               "`yes` only when the same quantity takes two materially different values, or a stated calculation does not hold; "
               "rounding, unit/format slips, naming differences and claim-versus-number contradictions are `no` "
               "(see `adjudicate_round2.py`). Changes (Round-1 value = the value after the first pass):\n\n"
               "| Record | Column | Round-1 | Final | Reason |\n|---|---|---|---|---|\n" + "\n".join(log) + "\n\n"
               "Rows kept as `yes` with `inconsistency_detail` trimmed to the qualifying items only (non-qualifying items such as "
               "model-name mismatches and claim contradictions removed): " + ", ".join(DETAIL_TRIMS) + ".\n")
    md += section
(A / "ADJUDICATION.md").write_text(md.replace("\r\n", "\n").replace("\n", "\r\n"), encoding="utf-8", newline="")
print("flipped:", [l.split("|")[1].strip() for l in log])
print("numeric_inconsistency yes:", sorted(r for r in rows if rows[r]["numeric_inconsistency"] == "yes"))
