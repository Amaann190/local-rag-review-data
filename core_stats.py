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
host_rows = list(csv.DictReader(open(H / "audit" / "execution_host.csv", encoding="utf-8")))
host = {r["record_id"]: r["execution_host"] for r in host_rows}
host_evidence = {r["record_id"]: r["evidence_type"] for r in host_rows}
for r in ext:
    r["execution_host"] = host.get(r["record_id"], "n.a.")
AUDIT_COLS.append("execution_host")
base_cols = [c for c in base_cols if c != "execution_host"]
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
        "execution_host": dict(Counter(r["execution_host"] for r in rows)),
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
        # No cloud use recorded (literal definition): the generator is coded local only and the judge is not coded cloud_llm.
        # An unstated judge (n.a.) is not evidence of a private pipeline; those are counted separately below.
        "no_cloud_recorded_ids": ids(rows, lambda r: r["generator_location"] == "local" and r["judge_location"] != "cloud_llm"),
        "numeric_inconsistency_ids": ids(ft, lambda r: r["numeric_inconsistency"] == "yes"),
    }
    out["attack_test_yes_n"] = len(out["attack_test_yes"])
    out["no_cloud_recorded_n"] = len(out["no_cloud_recorded_ids"])
    out["no_cloud_recorded_judge_na_n"] = len(ids(rows, lambda r: r["generator_location"] == "local" and r["judge_location"] == "n.a."))
    out["cloud_judge_n"] = len(out["cloud_judge_ids"])
    out["cloud_generator_n"] = len(out["cloud_generator_ids"])
    out["numeric_inconsistency_n"] = len(out["numeric_inconsistency_ids"])
    return out


# Local RAG set: builds or evaluates a RAG pipeline, the generator runs locally (alone or compared with cloud),
# AND it runs on user-controlled hardware (a device, an own or institutional server, or a stated local deployment).
# Hosted runtimes (Kaggle, RunPod, shared research clouds) and studies that never say where inference ran are excluded.
USER_CONTROLLED = ("device", "server", "local_unspecified")
pipelines = [r for r in ext if r["rag_pipeline"] == "yes"]
local_gen = [r for r in pipelines if r["generator_location"] in ("local", "both")]
rag = [r for r in local_gen if r["execution_host"] in USER_CONTROLLED]
# Strict local RAG set: additionally requires that the host is either named as hardware (hardware_specified == yes)
# or backed by a verified exact quote of the host statement (audit/execution_host.csv, evidence_type == exact_quote).
strict = [r for r in rag if r["hardware_specified"] == "yes" or host_evidence.get(r["record_id"]) == "exact_quote"]
is_ft = lambda r: r["source"].lower().startswith("full")
stats = {"core_all": summarize(ext), "rag_pipelines": summarize(pipelines),
         "open_weight_rag": summarize(local_gen), "local_rag": summarize(rag),
         "local_rag_ids": sorted(r["record_id"] for r in rag),
         "local_rag_strict": summarize(strict),
         "local_rag_strict_ids": sorted(r["record_id"] for r in strict),
         "local_rag_fulltext": summarize([r for r in rag if is_ft(r)]),
         "local_rag_abstract": summarize([r for r in rag if not is_ft(r)]),
         "hosted_ids": sorted(r["record_id"] for r in local_gen if r["execution_host"] == "hosted"),
         "host_not_stated_ids": sorted(r["record_id"] for r in local_gen if r["execution_host"] == "not_stated"),
         "generator_not_local_ids": sorted(r["record_id"] for r in pipelines if r not in local_gen),
         "excluded_from_local_rag_ids": sorted(r["record_id"] for r in ext if r not in rag),
         "fulltext_partly_read_ids": sorted(r["record_id"] for r in rag if r["source"].lower().startswith("full")
                                            and any(k in r["notes"].lower() for k in ("first ~", "truncated", "unread", "partly", "only first", "read except")))}
json.dump(stats, open(H / "core_stats.json", "w"), indent=1)
print(json.dumps({k: v for k, v in stats["local_rag"].items() if not k.endswith("_ids") and k != "attack_test_yes"}, indent=1))
print("strict n", len(strict), "fulltext", stats["local_rag_fulltext"]["n"], "abstract", stats["local_rag_abstract"]["n"])
print("core n", len(ext), "pipelines", len(pipelines), "local generator", len(local_gen), "local RAG n", len(rag))
