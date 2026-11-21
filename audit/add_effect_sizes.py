"""Append to effect_sizes.csv the values the paper quotes for core studies that the file did not yet list.
Values come from extraction.csv (key_result and notes); 'Not recorded' marks a table/section the extraction did not keep.
Idempotent: rows already present (same paper and finding) are skipped."""
import csv, pathlib

H = pathlib.Path(__file__).parent.parent
NR = "Not recorded in extraction (key_result)"
ABS = "Abstract (extraction key_result)"
ROWS = [
 ("retrieval", "Source Page Eval. of Local RAG (Sorour 2026, R2613)", "BM25 MRR and Hit@5 (highest of the compared retrievers)", "0.492; 0.722", "18 industrial safety documents; raw BM25", ABS),
 ("retrieval", "Source Page Eval. of Local RAG (Sorour 2026, R2613)", "Hybrid vs BM25 difference", "p = 0.302 (not different)", "Hybrid exceeded LSA after Holm correction (p = 0.011); hybrid MRR not in extraction", ABS),
 ("efficiency", "RoPA Hybrid RAG (Hinh 2026, R0372)", "Local vs cloud LLM difference (cloud higher)", "0.20 percentage points, 95% CI [-0.93, 1.32], p = 0.72", "32 paired scenarios; Qwen3.5-27B-GPTQ-Int4 (local) vs DeepSeek-V4-Flash (cloud); direction in favor of DeepSeek from the arXiv abstract (arXiv 2609.27359); metric not named in extraction", ABS + "; arXiv abstract"),
 ("efficiency", "CUBO (Astrino 2026, R0691)", "Median single-query retrieval latency (p50)", "185 ms", "16 GB consumer laptop", NR),
 ("efficiency", "CUBO (Astrino 2026, R0691)", "Peak memory while ingesting a 9.8 GB corpus", "15.1 GB", "16 GB consumer laptop; extraction notes record steady-state memory as 8.2 vs 14.2 GB in different tables", NR),
 ("efficiency", "Local Hybrid QA (Astrino 2025)", "Median single-user latency", "2.0 s", "30/70 hybrid, local", NR),
 ("efficiency", "Local Hybrid QA (Astrino 2025)", "Median latency with 10 concurrent users", "6.8 s", "30/70 hybrid, local", NR),
 ("efficiency", "Pocket RAG (Kang 2026, R2025)", "Response time, baseline to proposed", "14.2 s to 3.7 s", "On-device first-aid RAG; extraction notes record the 3.7 s as time to first token (identical 3.7 s on SQuAD and HotpotQA); the baseline is labelled Dense RAG, Baseline (Sequential) and LLaMA.cpp in different sections", NR),
 ("efficiency", "As We May Search (Zerhoudi 2026, R0336)", "Local vs cloud generation contains rate", "0.560 vs 0.600", "NQ-open, 147 scored queries; Ollama qwen2.5:7b vs gpt-4o-mini", NR),
 ("retrieval", "Operator Manuals over ISO 11783 (Oksanen 2026, R1667)", "F1: Qwen 2.5 7B vs open 120B model", "0.83 vs 0.81", "108 English questions, English manual in Markdown; GPT-OSS 120B scored 0.81", NR),
 ("grounding", "Authentic Sources, Unsafe Conclusions (Hu 2026, R0365)", "Change in faithfulness with RAG (Qwen3)", "-0.24 (P < 0.001)", "50-question perioperative IBD benchmark; accuracy delta +0.44 (P < 0.001) for Qwen3", NR),
 ("retrieval", "Dissecting Agentic RAG (Shaikh 2026, R0790)", "Exact match: agentic vs single-pass dense vs fixed RRF hybrid", "53.2 vs 43.1 vs 55.0", "HotpotQA distractor dev, local 7B model; full agentic pipeline EM 53.2 (F1 61.6), single-pass dense EM 43.1 (F1 54.0), fixed RRF hybrid EM 55.0", NR),
 ("grounding", "On-Premises RAG for Health Records (Gatimu 2026, R0966)", "Key-fact context precision: naive vs two advanced configurations", "0.687 vs 0.633 and 0.591", "12 curated queries, synthetic health-record corpus", ABS),
 ("retrieval", "Beyond Search Scores (Pylypenko 2026, R0450)", "nDCG@10: multilingual-E5 / EmbeddingGemma 2 / adaptive fusion / lemmatized BM25 / plain BM25", "0.674 / 0.633 / 0.629 / 0.482 / 0.450", "170 answerable queries, UA-PAR corpus; LLM-judged labels", ABS),
]
p = H / "effect_sizes.csv"
raw = p.read_text(encoding="utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
have = {(r["paper"], r["finding"]) for r in csv.DictReader(open(p, encoding="utf-8"))}
new = [r for r in ROWS if (r[1], r[2]) not in have]
if raw and not raw.endswith("\n"):
    raw += nl
with open(p, "w", newline="", encoding="utf-8") as f:
    f.write(raw)
    w = csv.writer(f, lineterminator=nl)
    w.writerows(new)
print("added", len(new))
