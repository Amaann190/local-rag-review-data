"""PRISMA counts and mapping figures for the review. Writes prisma.json, mapping.json and fig_*.pdf."""
import csv, json, collections, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = pathlib.Path(__file__).parent
recs = {r["record_id"]: r for r in json.load(open(H / "records_dedup.json", encoding="utf-8"))}
dd = json.load(open(H / "dedup_stats.json"))
log = json.load(open(H / "raw" / "search_log.json"))
claude = {r["record_id"]: r for r in csv.DictReader(open(H / "screening_claude.csv", encoding="utf-8"))}
codex = {}
for f in ("screening_codex.csv", "screening_codex_sample.csv"):
    codex.update({r["record_id"]: r for r in csv.DictReader(open(H / f, encoding="utf-8"))})
elig = {r["record_id"]: r for r in csv.DictReader(open(H / "eligibility_final.csv", encoding="utf-8"))}
core = json.load(open(H / "core_ids.json"))

adv = lambda d: d.strip().lower() in ("include", "unsure")
# Sensitivity re-screen of exclusions made without a full abstract (audit/sensitivity_rescreen.csv).
resc = {r["record_id"]: r for r in csv.DictReader(open(H / "audit" / "sensitivity_rescreen.csv", encoding="utf-8"))}
excluded_ta = [i for i in recs if not adv(claude[i]["decision"]) and not (i in codex and adv(codex[i]["decision"]))
               and not (i in resc and adv(resc[i]["decision"]))]
reasons = collections.Counter((claude[i]["reason_code"] or "").strip().upper()[:2] or "NA" for i in excluded_ta)
yes = [i for i, r in elig.items() if r["eligible"] == "yes"]
no_elig = [i for i, r in elig.items() if r["eligible"] != "yes"]
no_reason = collections.Counter(elig[i]["exclusion_reason"] for i in no_elig)
core_stats = json.load(open(H / "core_stats.json")) if (H / "core_stats.json").exists() else {}

prisma = {
    "search_date_utc": log["run_utc"],
    "identified_total": dd["retrieved_total"], "identified_openalex": dd["retrieved_openalex"], "identified_arxiv": dd["retrieved_arxiv"],
    "openalex_total_hits_all_queries": sum(q["openalex_total_hits"] for q in log["queries"]),
    "arxiv_total_hits_all_queries": sum(q["arxiv_total_hits"] for q in log["queries"]),
    "removed_duplicates": dd["duplicates_removed"], "removed_no_title": dd["removed_no_title"],
    "screened_title_abstract": dd["unique_records"],
    "screened_without_abstract": sum(not (r.get("abstract") or "") for r in recs.values()),
    "screened_abstract_truncated_2500": sum(len(r.get("abstract") or "") > 2500 for r in recs.values()),
    "excluded_title_abstract": len(excluded_ta), "excluded_ta_reasons": dict(reasons),
    "assessed_eligibility": len(elig),
    "excluded_eligibility": len(no_elig), "excluded_elig_reasons": dict(no_reason),
    "included_mapping": len(yes), "included_core": len(core),
    "core_local_rag": len(core_stats.get("local_rag_ids", [])),
}
json.dump(prisma, open(H / "prisma.json", "w"), indent=1)

fac_names = {"F1": "Hybrid/sparse-dense", "F2": "Grounding & abstention", "F3": "Local/constrained",
             "F4": "Security & privacy", "F5": "Multilingual/code-mixed", "F6": "RAG evaluation"}
fy = collections.Counter()
fac = collections.Counter()
pairs = collections.Counter()
for i in yes:
    fs = sorted({f for f in elig[i]["facets"].split(";") if f})
    for f in fs:
        fac[f] += 1
        fy[(f, recs[i].get("year"))] += 1
    for a in fs:
        for b in fs:
            if a < b:
                pairs[(a, b)] += 1
mapping = {"facets": dict(fac), "pairs": {f"{a}&{b}": n for (a, b), n in pairs.items()},
           "years": dict(collections.Counter(recs[i].get("year") for i in yes)),
           "preprint_share": round(sum(recs[i].get("type") == "preprint" or recs[i]["source_db"] == "arXiv" for i in yes) / len(yes), 3)}
json.dump(mapping, open(H / "mapping.json", "w"), indent=1)

plt.rcParams.update({"font.size": 8, "font.family": "serif",
                     "font.serif": ["Times New Roman", "Nimbus Roman", "DejaVu Serif"],
                     "mathtext.fontset": "stix", "pdf.fonttype": 42,
                     "axes.spines.top": False, "axes.spines.right": False})
# Facet co-occurrence heatmap
F = list(fac_names)
fig, ax = plt.subplots(figsize=(3.4, 2.7))
M = [[fac[a] if a == b else pairs.get(tuple(sorted((a, b))), 0) for b in F] for a in F]
im = ax.imshow(M, cmap="Blues")
ax.set_xticks(range(6)); ax.set_yticks(range(6))
ax.set_xticklabels(F); ax.set_yticklabels([f"{f} {fac_names[f]}" for f in F])
for a in range(6):
    for b in range(6):
        ax.text(b, a, M[a][b], ha="center", va="center", fontsize=7, color="white" if M[a][b] > 200 else "black")
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
fig.tight_layout(); fig.savefig(H / "fig_facets.pdf", bbox_inches="tight"); plt.close(fig)

# Facets by year
years = [y for y in sorted({recs[i].get("year") for i in yes}) if y and y >= 2023]
fig, ax = plt.subplots(figsize=(3.4, 1.9))
w = 0.13
for k, f in enumerate(F):
    ax.bar([x + (k - 2.5) * w for x in range(len(years))], [fy[(f, y)] for y in years], w, label=f)
ax.set_xticks(range(len(years))); ax.set_xticklabels(years)
ax.set_ylabel("Eligible studies")
ax.legend(ncol=6, fontsize=7, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), handlelength=1.2, columnspacing=1.0)
fig.tight_layout(); fig.savefig(H / "fig_years.pdf", bbox_inches="tight"); plt.close(fig)
print(json.dumps(prisma, indent=1)); print(json.dumps(mapping, indent=1))
