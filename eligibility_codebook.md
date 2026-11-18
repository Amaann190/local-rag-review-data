# Stage 2: RQ-focus eligibility

Applied to every record that passed title/abstract screening (either screener: include or unsure). Judge from title and abstract.

A record is **eligible** only if BOTH hold:

**F: Core facet.** Its main contribution addresses at least one of:
- **F1 Hybrid/sparse-dense retrieval:** BM25 or other sparse retrieval combined with or compared against dense retrieval, rank/score fusion, or reranking for RAG or document QA.
- **F2 Abstention and grounding:** unanswerable queries, refusal/abstention, evidence sufficiency, citation/attribution, or hallucination detection/mitigation specific to retrieved context.
- **F3 Local or constrained RAG:** RAG or LLM inference run locally, offline, on-device, at the edge, or with small/quantized models, with the deployment constraint as a studied factor.
- **F4 Security/privacy of RAG:** poisoning, prompt injection through retrieved content, data leakage, membership inference, embedding inversion, or defences.
- **F5 Multilingual or code-mixed retrieval:** non-English, cross-lingual, or code-mixed queries/documents in retrieval or RAG.
- **F6 RAG evaluation:** a benchmark, metric, or evaluation framework for RAG systems.

**E: Evidence.** It reports a quantitative evaluation (experiments, benchmark results, user study, or ablation), OR it is a survey/review with an explicit literature-search method.

Output columns: `record_id, eligible (yes/no), facets (e.g. F1;F3), evidence (yes/no), note (≤15 words)`.
Domain applications (e.g. "RAG for agriculture") are eligible only if a facet above is itself studied (for instance an ablation of hybrid vs dense retrieval).
