"""Build hybrid_comparisons.csv and local_vs_cloud.csv from extraction.csv (key_result + notes + models fields).

Hand-coded from the extraction text only; nothing is taken from the full papers except the R0372 direction,
read from the public arXiv abstract page (https://arxiv.org/abs/2609.27359).
hybrid_comparisons.csv: every local-set study coded hybrid == yes (26) plus the two core studies outside the local
set that the paper cites as retrieval-only (R2613, R0450). `comparison` = yes only when the extraction names a
dense-only, BM25-only or sparse-only baseline with values or a direction; baselines called only 'naive RAG',
'baseline RAG' or 'single-pass RAG' do not count.
local_vs_cloud.csv: every local-set study with generator_location == both (8).
"""
import csv, json, pathlib
from collections import Counter

H = pathlib.Path(__file__).parent.parent
ext = {r["record_id"]: r for r in csv.DictReader(open(H / "extraction.csv", encoding="utf-8"))}
local = set(json.load(open(H / "core_stats.json"))["local_rag_ids"])

KR = "key_result"
KN = "key_result+notes"
HYB = [  # record_id, comparison, metrics, direction, values, source_field
    ("R0069", "no", "", "n.a.", "baseline RAG (not stated as dense-only or BM25-only): nDCG@10 +27.3%", KR),
    ("R0269", "no", "", "n.a.", "no baseline", KN),
    ("R0336", "no", "", "n.a.", "dense nDCG@10 only (0.910 at 100K docs, 0.736 at 1M); no hybrid-vs-single-channel result in extraction", KR),
    ("R0372", "no", "", "n.a.", "local vs cloud LLM comparison only", KR),
    ("R0587", "no", "", "n.a.", "hybrid+rerank HitRate@10 0.964, MRR@10 0.625; no single-channel baseline", KR),
    ("R0594", "no", "", "n.a.", "latency comparison local vs cloud only", KR),
    ("R0691", "yes", "nDCG@10", "hybrid worse", "hybrid trails BM25/E5 on several nDCG@10, e.g. SciFact 0.399 vs 0.550 (BM25)", "notes"),
    ("R0742", "no", "", "n.a.", "latency and semantic accuracy of generators only", KR),
    ("R0750", "no", "", "n.a.", "no baseline", KN),
    ("R0767", "no", "", "n.a.", "internal Top-K/chunk configurations only", KN),
    ("R0790", "yes", "EM; F1 (answer quality)", "hybrid better", "fixed RRF hybrid EM 55.0 vs single-pass dense EM 43.1 (F1 54.0); the full agentic pipeline EM 53.2, F1 61.6; hybrid and dense rows differ in pipeline stages, so confounded", KN),
    ("R0895", "no", "", "n.a.", "Hybrid BM25 F1 compared with Oracle Context only", KR),
    ("R0988", "no", "", "n.a.", "sparse retrieval gave best F1 0.726 among configurations; hybrid value not in extraction", KR),
    ("R1315", "no", "", "n.a.", "cascade vs zero-shot LLM, not retrieval channels", KR),
    ("R1334", "no", "", "n.a.", "qualitative only: ensemble with keyword boosting best of five retrieval configurations; no metric values", KR),
    ("R1355", "no", "", "n.a.", "grounding rate 89.6% vs 71.2% single-pass RAG (retrieval type of baseline not stated)", KR),
    ("R1366", "no", "", "n.a.", "MRR 39.63% vs 27.76% for best baseline (RRF, a fusion baseline); no single-channel baseline", KR),
    ("R1378", "no", "", "n.a.", "no baseline", KN),
    ("R1394", "no", "", "n.a.", "no baseline", KN),
    ("R1642", "yes", "Recall@10; MRR", "mixed", "Recall@10 hybrid vs dense 0.974 vs 0.959 (SQuAD), 0.620 vs 0.605 (MS MARCO); MRR 0.250 vs 0.315 on MS MARCO (hybrid lower), equal MRR on SQuAD (0.805 hybrid)", "key_result+notes; effect_sizes.csv"),
    ("R1667", "no", "", "n.a.", "model and format comparison only", KR),
    ("R1812", "yes", "MRR@10; EM (answer quality)", "hybrid better", "full multi-agent pipeline MRR@10 0.910, EM 78.4% vs single-stage dense MRR@10 0.761, EM 63.8%; confounded with KG expansion, reranking and verifier", KR),
    ("R1833", "no", "", "n.a.", "MRR 0.132 to 0.340 vs a Naive-RAG baseline (not stated as dense-only); RRF/reranker not ablated", KN),
    ("R2025", "no", "", "n.a.", "response-time speedup 14.2 s to 3.7 s vs a sequential dense-RAG baseline reflects pipelining, not channel choice", KN),
    ("R2318", "no", "", "n.a.", "best Macro-F1 reported with dense RAG; hybrid vs dense not in extraction", KR),
    ("R2836", "no", "", "n.a.", "hybrid Recall@5 0.88 (44/50); no single-channel baseline", KR),
    ("R2613", "yes", "MRR; Hit@5", "hybrid not better (n.s. vs BM25)", "raw BM25 had the highest MRR 0.492 and Hit@5 0.722; hybrid exceeded LSA (p=0.011) but did not differ from BM25 (p=0.302); hybrid values not in extraction", KR),
    ("R0450", "yes", "nDCG@10", "mixed", "adaptive fusion 0.629 vs multilingual-E5 0.674 and EmbeddingGemma 2 0.633 (dense, higher or equal) and plain BM25 0.450, lemmatized BM25 0.482 (lower); notes: no demonstrated advantage over dense or RRF", KN),
]
expected = {i for i in local if ext[i]["hybrid"] == "yes"} | {"R2613", "R0450"}
assert {h[0] for h in HYB} == expected, sorted({h[0] for h in HYB} ^ expected)
with open(H / "audit" / "hybrid_comparisons.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", "in_local_set", "comparison", "metrics", "direction", "values", "source_field"])
    for rid, comp, met, d, val, src in HYB:
        w.writerow([rid, "yes" if rid in local else "no", comp, met, d, val, src])

NS = "not stated"
LVC = [  # record_id, task, local model, cloud model, metric, local value, cloud value, direction, note
    ("R0336", "open-domain QA generation (NQ-open, 147 scored queries)", "Ollama qwen2.5:7b", "gpt-4o-mini", "contains rate", "0.560", "0.600", "cloud higher", "small generation eval; other local sizes (1.5B, 3B, gemma4:e4b) not valued in extraction"),
    ("R0372", "Vietnamese RoPA field extraction, 32 paired scenarios", "Qwen3.5-27B-GPTQ-Int4", "DeepSeek-V4-Flash", NS + " in extraction (the arXiv abstract does not name the metric)", NS, NS, "cloud higher by 0.20 percentage points, not significant", "difference 0.20 pp, 95% CI [-0.93, 1.32], p = 0.72; direction ('in favor of DeepSeek') from the arXiv abstract, https://arxiv.org/abs/2609.27359; Gemma-4-31B was significantly worse"),
    ("R0594", "Pakistani criminal-law QA, edge CPU system vs cloud system", "local edge LLM (unnamed), Intel i5 6th gen, 8 GB RAM", "cloud system via Groq inference (model " + NS + ")", "warm-start latency", "105-118 s", "1.5-3.5 s", "cloud faster", "cache hits 0.1-0.5 s; no quality metrics in extraction"),
    ("R0773", "UltraDomain QA, edge-cloud distributed graph RAG", "Qwen2.5-14B AWQ (edge)", "Qwen-Max (cloud)", "LLM-judged win rate of DGRAG vs centralized RAG", "66.8% within-domain, 73.5% out-of-domain (DGRAG)", NS + " (centralized RAG is the reference)", "edge-cloud system wins", "system comparison, not a model-vs-model score; cloud LLM tokens cut from 178.6M to 69.9M"),
    ("R2318", "abusive-clause detection in Spanish terms of service, dense RAG", "Qwen3 14b (Ollama)", "GPT 5.2", "Macro-F1", "0.603 +/- 0.007", "0.613 +/- 0.008", "cloud higher", "difference 0.010"),
    ("R2360", "article identification for forensic legal scenarios (Ukrainian), RAG", "local LLMs (names " + NS + ")", "GPT-4o-mini", "article identification accuracy", "41.7%", "54.2%", "cloud higher", "GPT-4o-mini RAG vs few-shot 29.2% (p=0.03) and direct prompting 52.1% (p=0.89); percentages correspond to 48 scored cases, not 60"),
    ("R2595", "enterprise document QA, 45 documents, 200 queries", "local LLM (name " + NS + ")", "GPT-4", "semantic answer accuracy relative to GPT-4, identical retrieved contexts", "up to 87% of GPT-4", "baseline (100% by construction)", "cloud higher", "metric is ambiguous in the extraction; latency 2-5 s, memory below 4 GB"),
    ("R2836", "Thai wellness QA; no-retrieval frontier probe (71 questions)", "Qwen3.6-35B-A3B (AWQ, vLLM)", "Gemini 2.5 Flash (no-retrieval probe)", NS, NS, NS, NS, "extraction records the cloud model only as a no-retrieval probe, not a scored head-to-head"),
]
both = {i for i in local if ext[i]["generator_location"] == "both"}
assert {r[0] for r in LVC} == both, sorted({r[0] for r in LVC} ^ both)
with open(H / "audit" / "local_vs_cloud.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["record_id", "task", "local_model", "cloud_model", "metric", "local_value", "cloud_value", "direction", "note"])
    w.writerows(LVC)
print(Counter(h[3] for h in HYB if h[1] == "yes"), "yes in local set:", sum(h[1] == "yes" for h in HYB if h[0] in local))
