"""Deduplicate raw search records and write the blinded screening input.

Duplicates are matched on DOI, arXiv id, or normalized title. When an arXiv preprint and a
published version match, the published (OpenAlex, non-preprint) record is kept.
Outputs:
  records_dedup.json     all unique records with full metadata and the queries that found them
  screening_input.csv    record_id, title, year, venue, abstract (what screeners see)
  dedup_stats.json       counts for the PRISMA diagram
"""
import csv, json, pathlib, re, unicodedata

HERE = pathlib.Path(__file__).parent
raw = json.load(open(HERE / "raw" / "records_raw.json", encoding="utf-8"))


def norm_title(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def doi_key(d):
    return (d or "").lower().replace("https://doi.org/", "").strip() or None


def arxiv_key(r):
    if r.get("arxiv_id"):
        return re.sub(r"v\d+$", "", r["arxiv_id"])
    d = doi_key(r.get("doi"))
    m = re.search(r"arxiv\.(\d{4}\.\d{4,5})", d or "")
    return m.group(1) if m else None


def rank(r):  # lower is preferred
    return (r.get("type") == "preprint", r["source_db"] == "arXiv", -(r.get("cited_by") or 0))


groups, index = [], {}
no_title = 0
for r in raw:
    nt = norm_title(r.get("title"))
    if not nt:
        no_title += 1
        continue
    keys = [k for k in (("doi", doi_key(r.get("doi"))), ("arxiv", arxiv_key(r)), ("title", nt)) if k[1]]
    gid = next((index[k] for k in keys if k in index), None)
    if gid is None:
        gid = len(groups)
        groups.append([])
    groups[gid].append(r)
    for k in keys:
        index.setdefault(k, gid)

unique = []
for g in groups:
    best = sorted(g, key=rank)[0].copy()
    best["found_by_queries"] = sorted({x["query"] for x in g})
    best["found_in_dbs"] = sorted({x["source_db"] for x in g})
    if not best.get("abstract"):
        best["abstract"] = next((x["abstract"] for x in g if x.get("abstract")), "")
    best.pop("query", None)
    unique.append(best)

unique.sort(key=lambda r: norm_title(r["title"]))
for i, r in enumerate(unique, 1):
    r["record_id"] = f"R{i:04d}"

json.dump(unique, open(HERE / "records_dedup.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(HERE / "screening_input.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", "title", "year", "venue", "abstract"])
    for r in unique:
        w.writerow([r["record_id"], r["title"], r.get("year"), r.get("venue") or "", (r.get("abstract") or "")[:2500]])

stats = {
    "retrieved_total": len(raw),
    "retrieved_openalex": sum(r["source_db"] == "OpenAlex" for r in raw),
    "retrieved_arxiv": sum(r["source_db"] == "arXiv" for r in raw),
    "removed_no_title": no_title,
    "duplicates_removed": len(raw) - no_title - len(unique),
    "unique_records": len(unique),
    "unique_without_abstract": sum(not r.get("abstract") for r in unique),
}
json.dump(stats, open(HERE / "dedup_stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))
