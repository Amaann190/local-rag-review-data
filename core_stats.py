"""Merge the audit coding into extraction.csv and compute every core-set statistic reported in the paper.

Writes:
  extraction.csv     (adds the audit columns from audit/audit_part*.csv)
  core_stats.json    (all counts, with the record IDs behind each count)
"""
import csv, json, pathlib
from collections import Counter

H = pathlib.Path(__file__).parent
ext = list(csv.DictReader(open(H / "extraction.csv", encoding="utf-8")))
audit = {}
for p in sorted((H / "audit").glob("audit_part*.csv")):
    for r in csv.DictReader(open(p, encoding="utf-8")):
        audit[r["record_id"].strip()] = r
assert len(audit) == len(ext) == 108, (len(audit), len(ext))

AUDIT_COLS = ["rag_pipeline", "generator_location", "judge_location", "hybrid", "reranker",
              "hardware_specified", "public_benchmark", "attack_test", "numeric_inconsistency",
              "inconsistency_detail"]
base_cols = [c for c in ext[0].keys() if c not in AUDIT_COLS]
for r in ext:
    a = audit[r["record_id"]]
    for c in AUDIT_COLS:
        v = (a.get(c) or "").strip()
        r[c] = v if c == "inconsistency_detail" else v.lower()
with open(H / "extraction.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=base_cols + AUDIT_COLS)
    w.writeheader()
    w.writerows(ext)


def ids(rows, pred):
    return sorted(r["record_id"] for r in rows if pred(r))


def summarize(rows):
    n = len(rows)
    lo = lambda r: r["local_execution"].split()[0].lower() if r["local_execution"] else ""
    ft = [r for r in rows if r["source"].lower().startswith("full")]
    out = {
        "n": n,
        "source_fulltext": len(ft), "source_abstract": n - len(ft),
        "contribution_type": dict(Counter(r["contribution_type"].split()[0].lower() for r in rows)),
        "local_execution": dict(Counter(lo(r) for r in rows)),
        "generator_location": dict(Counter(r["generator_location"] for r in rows)),
        "judge_location": dict(Counter(r["judge_location"] for r in rows)),
        "hybrid_yes": len(ids(rows, lambda r: r["hybrid"] == "yes")),
        "reranker_yes": len(ids(rows, lambda r: r["reranker"] == "yes")),
        "hybrid_and_reranker": len(ids(rows, lambda r: r["hybrid"] == "yes" and r["reranker"] == "yes")),
        "abstention": dict(Counter(r["abstention"].split()[0].lower() for r in rows)),
        "citation": dict(Counter(r["citation"].split()[0].lower() for r in rows)),
        "security_privacy": dict(Counter(r["security_privacy"].split()[0].lower() for r in rows)),
        "attack_test_yes": ids(rows, lambda r: r["attack_test"] == "yes"),
        "public_benchmark_yes": len(ids(rows, lambda r: r["public_benchmark"] == "yes")),
        "multilingual": dict(Counter(r["multilingual"].split()[0].lower() for r in rows)),
        "hardware_specified_yes": len(ids(rows, lambda r: r["hardware_specified"] == "yes")),
        "peer_reviewed_yes": len(ids(rows, lambda r: r["peer_reviewed"].lower().startswith("yes"))),
        "quality": dict(Counter(int(float(r["quality_total"] or 0)) for r in rows)),
        "quality_mean": round(sum(float(r["quality_total"] or 0) for r in rows) / n, 2),
        "cloud_judge_ids": ids(rows, lambda r: r["judge_location"] == "cloud_llm"),
        "cloud_generator_ids": ids(rows, lambda r: r["generator_location"] in ("cloud", "both")),
        "fulltext_assessed": len(ft),
        "numeric_inconsistency_ids": ids(ft, lambda r: r["numeric_inconsistency"] == "yes"),
    }
    out["attack_test_yes_n"] = len(out["attack_test_yes"])
    out["cloud_judge_n"] = len(out["cloud_judge_ids"])
    out["cloud_generator_n"] = len(out["cloud_generator_ids"])
    out["numeric_inconsistency_n"] = len(out["numeric_inconsistency_ids"])
    return out


rag = [r for r in ext if r["rag_pipeline"] == "yes"]
stats = {"core_all": summarize(ext), "local_rag": summarize(rag),
         "local_rag_ids": sorted(r["record_id"] for r in rag),
         "excluded_from_local_rag_ids": sorted(r["record_id"] for r in ext if r["rag_pipeline"] != "yes")}
json.dump(stats, open(H / "core_stats.json", "w"), indent=1)
print(json.dumps({k: v for k, v in stats["local_rag"].items() if not k.endswith("_ids") and k != "attack_test_yes"}, indent=1))
print("core n", len(ext), "local RAG n", len(rag))
