"""Reconstruct the two coders' original (pre-adjudication) coding from ADJUDICATION.md.

The coders' own exports were overwritten during adjudication and were not kept. These files are therefore
RECONSTRUCTIONS: the adjudicated files with each logged change reversed. They restore the coded values
(e.g. the initial 3/24 and 26/30 numeric-inconsistency counts) but not the coders' free-text
`inconsistency_detail`, which the log did not record. See original/README.md."""
import csv, pathlib, re

A = pathlib.Path(__file__).parent
log = {}
for line in (A / "ADJUDICATION.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\| (R\d{4}) \| (\w+) \| ([^|]*) \| ([^|]*) \|", line)
    if m:
        log.setdefault(m.group(1), {}).setdefault(m.group(2), m.group(3).strip())  # first logged value = the coder's (Round-2 rows log the Round-1 value, which equals the coder's)
(A / "original").mkdir(exist_ok=True)
for p in sorted(A.glob("audit_part*.csv")):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    cols = list(rows[0].keys())
    for r in rows:
        for col, old in log.get(r["record_id"], {}).items():
            r[col] = old
    with open(A / "original" / p.name.replace(".csv", "_coder_reconstructed.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    n_ft_yes = sum(r["numeric_inconsistency"] == "yes" for r in rows)
    print(p.name, "original numeric_inconsistency yes:", n_ft_yes)
