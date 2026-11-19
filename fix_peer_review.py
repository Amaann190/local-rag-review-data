"""Apply the peer-review rule: a study counts as peer-reviewed if it is published in, or stated on its own
landing page as accepted at, a peer-reviewed journal or conference. Two rows coded 'no' meet this rule."""
import csv, pathlib

H = pathlib.Path(__file__).parent
FIX = {"R1895": "yes (accepted at EuroSys 2026 per paper page)",
       "R1667": "yes (accepted in Computers and Electronics in Agriculture per paper page)"}
rows = list(csv.DictReader(open(H / "extraction.csv", encoding="utf-8")))
cols = list(rows[0].keys())
for r in rows:
    if r["record_id"] in FIX:
        r["peer_reviewed"] = FIX[r["record_id"]]
with open(H / "extraction.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print({r["record_id"]: r["peer_reviewed"] for r in rows if r["record_id"] in FIX})
