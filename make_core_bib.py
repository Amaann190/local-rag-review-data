"""Write LaTeX \\bibitem entries for the core studies cited in the paper, from OpenAlex/arXiv metadata."""
import json, re, pathlib

H = pathlib.Path(__file__).parent
recs = {r["record_id"]: r for r in json.load(open(H / "records_dedup.json", encoding="utf-8"))}
IDS = ("R0336 R0365 R0372 R0396 R0450 R0526 R0691 R0790 R0810 R0895 R0966 R1355 "
       "R1667 R2025 R2247 R2613 R2760 R2915 R2944").split()


def esc(s):
    for a, b in (("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#")):
        s = (s or "").replace(a, b)
    return s


lines = []
for i in IDS:
    r = recs[i]
    a = r.get("authors") or []
    if not a:
        au = "Anonymous"
    elif len(a) == 1:
        au = a[0]
    elif len(a) == 2:
        au = f"{a[0]} and {a[1]}"
    else:
        au = a[0] + r" \emph{et al.}"
    doi = (r.get("doi") or "").replace("https://doi.org/", "")
    ax = r.get("arxiv_id") or (re.search(r"arxiv\.(\d{4}\.\d{4,5})", doi.lower()) or [None, None])[1]
    ax = re.sub(r"v\d+$", "", ax) if ax else None
    venue = (r.get("venue") or "").replace("Zenodo (CERN European Organization for Nuclear Research)", "Zenodo")
    if ax:
        where = f"arXiv:{ax}"
        tail = ""
    else:
        where = r"\emph{" + esc(venue) + "}" if venue else ""
        tail = r", doi:\nolinkurl{" + doi + "}" if doi else ""
    lines.append(r"\bibitem{rec" + i + "} " + esc(au) + ", ``" + esc(r["title"]) + ",'' " + where + f", {r.get('year')}" + tail + ".")

(H / "core_bib.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(len(lines))
