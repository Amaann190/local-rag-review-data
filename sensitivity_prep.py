"""List Stage-1 exclusions made on missing or truncated abstracts, with the FULL abstract, for re-screening."""
import csv, json, pathlib

H = pathlib.Path(__file__).parent
recs = {r["record_id"]: r for r in json.load(open(H / "records_dedup.json", encoding="utf-8"))}
cl = {r["record_id"]: r for r in csv.DictReader(open(H / "screening_claude.csv", encoding="utf-8"))}
codex = {}
for f in ("screening_codex.csv", "screening_codex_sample.csv"):
    codex.update({r["record_id"]: r for r in csv.DictReader(open(H / f, encoding="utf-8"))})
adv = lambda d: d.strip().lower() in ("include", "unsure")
rows = []
for i, r in recs.items():
    ab = r.get("abstract") or ""
    excluded = not adv(cl[i]["decision"]) and not (i in codex and adv(codex[i]["decision"]))
    if not excluded:
        continue
    if not ab:
        rows.append({"record_id": i, "issue": "no_abstract", "title": r["title"], "full_abstract": ""})
    elif len(ab) > 2500:
        rows.append({"record_id": i, "issue": "truncated", "title": r["title"], "full_abstract": ab})
with open(H / "audit" / "sensitivity_input.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "issue", "title", "full_abstract"])
    w.writeheader()
    w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["issue"] for r in rows))
