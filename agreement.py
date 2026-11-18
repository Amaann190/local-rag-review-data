"""Inter-screener agreement and adjudication list.

Usage: python agreement.py screening_claude.csv screening_codex.csv [label_a] [label_b]
Reports raw agreement and Cohen's kappa for (a) the 3-way decision and (b) the binary
decision used for advancement, where 'unsure' counts as 'include' (forwarded to full text).
Writes disagreements_<a>_vs_<b>.csv for adjudication.
"""
import csv, json, sys, pathlib
from collections import Counter

HERE = pathlib.Path(__file__).parent


def load(p):
    with open(p, encoding="utf-8") as f:
        return {r["record_id"].strip(): r for r in csv.DictReader(f)}


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else 1.0


a_path, b_path = sys.argv[1], sys.argv[2]
la = sys.argv[3] if len(sys.argv) > 3 else pathlib.Path(a_path).stem
lb = sys.argv[4] if len(sys.argv) > 4 else pathlib.Path(b_path).stem
A, B = load(a_path), load(b_path)
ids = sorted(set(A) & set(B))
missing = sorted(set(A) ^ set(B))
dec = lambda r: r["decision"].strip().lower()
three = [(dec(A[i]), dec(B[i])) for i in ids]
binary = [tuple("include" if d in ("include", "unsure") else "exclude" for d in p) for p in three]
po3, k3 = kappa(three)
po2, k2 = kappa(binary)
res = {
    "screener_a": la, "screener_b": lb, "n_compared": len(ids), "n_missing_in_one": len(missing),
    "three_way": {"agreement": round(po3, 4), "kappa": round(k3, 4)},
    "binary_advance": {"agreement": round(po2, 4), "kappa": round(k2, 4)},
    "counts_a": dict(Counter(a for a, _ in three)), "counts_b": dict(Counter(b for _, b in three)),
    "both_advance": sum(a == b == "include" for a, b in binary),
    "disagree_binary": sum(a != b for a, b in binary),
}
print(json.dumps(res, indent=1))
json.dump(res, open(HERE / f"agreement_{la}_vs_{lb}.json", "w"), indent=1)
with open(HERE / f"disagreements_{la}_vs_{lb}.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", f"{la}_decision", f"{la}_reason", f"{lb}_decision", f"{lb}_reason"])
    for i, (x, y) in zip(ids, binary):
        if x != y:
            w.writerow([i, dec(A[i]), A[i].get("reason_code", ""), dec(B[i]), B[i].get("reason_code", "")])
