"""Logged literature search over OpenAlex and arXiv. Records date, query, total hits, and top-N records."""
import json, time, urllib.parse, urllib.request, datetime, xml.etree.ElementTree as ET, sys, pathlib
OUT = pathlib.Path(__file__).parent / "raw"
TOPN = 200
UA = {"User-Agent": "literature-review-script/1.0"}
def get(url):
    for i in range(8):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(20)
    raise RuntimeError(url)
def abstract(inv):
    if not inv: return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)
def openalex(q):
    base = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q) +
            "&filter=" + urllib.parse.quote("publication_year:2019-2026,type:article|preprint|review"))
    recs, cursor, total = [], "*", None
    while len(recs) < TOPN and cursor:
        d = json.loads(get(base + f"&per-page=200&sort=relevance_score:desc&cursor={cursor}"))
        total = d["meta"]["count"]; cursor = d["meta"].get("next_cursor")
        for w in d["results"]:
            src = (w.get("primary_location") or {}).get("source") or {}
            recs.append({"source_db": "OpenAlex", "openalex_id": w["id"], "doi": w.get("doi"), "title": w.get("title"),
                         "year": w.get("publication_year"), "venue": src.get("display_name"), "type": w.get("type"),
                         "cited_by": w.get("cited_by_count"), "authors": [a["author"]["display_name"] for a in w.get("authorships", [])][:6],
                         "abstract": abstract(w.get("abstract_inverted_index"))})
        if not d["results"]: break
    return total, recs[:TOPN]
def arxiv(q):
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "start": 0, "max_results": TOPN, "sortBy": "relevance"})
    root = ET.fromstring(get(url)); time.sleep(3)
    total = int(root.find("o:totalResults", ns).text)
    recs = []
    for e in root.findall("a:entry", ns):
        y = int(e.find("a:published", ns).text[:4])
        if y < 2019: continue
        recs.append({"source_db": "arXiv", "arxiv_id": e.find("a:id", ns).text.split("/abs/")[-1], "doi": None,
                     "title": " ".join(e.find("a:title", ns).text.split()), "year": y, "venue": "arXiv", "type": "preprint",
                     "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)][:6],
                     "abstract": " ".join(e.find("a:summary", ns).text.split())})
    return total, recs
log = {"run_utc": datetime.datetime.now(datetime.UTC).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", "top_n_per_query": TOPN, "years": "2019-2026", "queries": []}
allrecs = []
for q in json.load(open(pathlib.Path(__file__).parent / "queries.json")):
    t1, r1 = openalex(q["openalex"]); t2, r2 = arxiv(q["arxiv"])
    for r in r1 + r2: r["query"] = q["id"]
    allrecs += r1 + r2
    log["queries"].append({"id": q["id"], "openalex_query": q["openalex"], "openalex_total_hits": t1, "openalex_retrieved": len(r1),
                           "arxiv_query": q["arxiv"], "arxiv_total_hits": t2, "arxiv_retrieved": len(r2)})
    print(q["id"], t1, len(r1), t2, len(r2), flush=True)
json.dump(log, open(OUT / "search_log.json", "w"), indent=1)
json.dump(allrecs, open(OUT / "records_raw.json", "w", encoding="utf-8"), ensure_ascii=False)
print("total retrieved", len(allrecs))
