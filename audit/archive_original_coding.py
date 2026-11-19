"""Reconstruct the two coders' original (pre-adjudication) files from ADJUDICATION.md and keep them alongside
the adjudicated files, so the initial coding and every correction can be checked directly."""
import csv, pathlib, re

A = pathlib.Path(__file__).parent
log = {}
for line in (A / "ADJUDICATION.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\| (R\d{4}) \| (\w+) \| ([^|]*) \| ([^|]*) \|", line)
    if m:
        log.setdefault(m.group(1), {})[m.group(2)] = m.group(3).strip()
(A / "original").mkdir(exist_ok=True)
for p in sorted(A.glob("audit_part*.csv")):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    cols = list(rows[0].keys())
    for r in rows:
        for col, old in log.get(r["record_id"], {}).items():
            r[col] = old
    with open(A / "original" / p.name.replace(".csv", "_coder.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    n_ft_yes = sum(r["numeric_inconsistency"] == "yes" for r in rows)
    print(p.name, "original numeric_inconsistency yes:", n_ft_yes)
