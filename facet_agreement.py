"""Facet-level inter-screener agreement on the 300-record eligibility sample.

Screener A = eligibility_final.csv (Claude), Screener B = eligibility_codex_sample.csv (Codex), compared on the
records in eligibility_input_sample.csv. For each facet F1-F6 the binary label is "facet assigned" vs "not assigned".

Convention used for the published facet kappas (agreement_eligibility_claude_vs_codex.json):
  a screener's facets are BLANKED for every record that screener judged ineligible, and kappa is computed over
  all 300 records. A facet label therefore counts only for records the screener judged eligible; a record one
  screener rejects counts as "facet not assigned" even if the other assigned the facet.
Alternative (reported for comparison, not used in the paper): facets compared only over the records BOTH
screeners judged eligible (a conditional agreement that ignores the eligibility disagreement).

Writes facet_agreement.json and prints both sets.
"""
import csv, json, pathlib
from collections import Counter

H = pathlib.Path(__file__).parent
FACETS = [f"F{k}" for k in range(1, 7)]


def load(p):
    return {r["record_id"].strip(): r for r in csv.DictReader(open(H / p, encoding="utf-8"))}


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


sample = [r["record_id"].strip() for r in csv.DictReader(open(H / "eligibility_input_sample.csv", encoding="utf-8"))]
A, B = load("eligibility_final.csv"), load("eligibility_codex_sample.csv")
assert len(sample) == 300 and all(i in A and i in B for i in sample)
yes = lambda r: r["eligible"].strip().lower() == "yes"
fac = lambda r: {f for f in r["facets"].replace(",", ";").split(";") if f.strip()} if yes(r) else set()
raw = lambda r: {f for f in r["facets"].replace(",", ";").split(";") if f.strip()}

blanked = {f: kappa([(f in fac(A[i]), f in fac(B[i])) for i in sample]) for f in FACETS}
both = [i for i in sample if yes(A[i]) and yes(B[i])]
conditional = {f: kappa([(f in raw(A[i]), f in raw(B[i])) for i in both]) for f in FACETS}
res = {"n_sample": len(sample), "n_both_eligible": len(both),
       "facet_kappa_blanked_all300": blanked,
       "facet_kappa_both_eligible_only": conditional}
json.dump(res, open(H / "facet_agreement.json", "w"), indent=1)
print(json.dumps(res, indent=1))
published = json.load(open(H / "agreement_eligibility_claude_vs_codex.json"))["facet_kappa"]
print("matches published facet_kappa:", blanked == published)
