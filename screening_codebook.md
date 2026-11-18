# Title/abstract screening codebook

Screen each record using **only its title and abstract**. Do not look at other screeners' decisions.

## Decision
Give each record exactly one decision:

- `include`: meets at least one inclusion criterion (I1–I5) and no exclusion criterion (E1–E6).
- `exclude`: meets any exclusion criterion. Record the **first** one that applies as the reason.
- `unsure`: the abstract is too vague to decide. Unsure records go to full-text review.

## Inclusion criteria (at least one)
- **I1** Proposes or evaluates a retrieval method (sparse, dense, learned-sparse, hybrid, fusion, reranking) used for document QA or RAG.
- **I2** Proposes or evaluates grounding, citation or attribution, hallucination detection or mitigation, or abstention/unanswerable handling in retrieval-augmented LLMs.
- **I3** Evaluates RAG systems or proposes a RAG benchmark/metric.
- **I4** Targets local, offline, on-device, edge, or resource-constrained LLM or RAG deployment, including quantization or small models evaluated for inference.
- **I5** Analyzes security or privacy of retrieval-augmented LLMs: poisoning, prompt injection via retrieved content, data leakage, embedding inversion.
- Multilingual or code-mixed retrieval counts under I1 if it involves retrieval.

## Exclusion criteria (first that applies)
- **E1** Not about language/text (e.g. image-only retrieval, recommender systems, biology sequences).
- **E2** Uses RAG only as a tool for a domain application, with no method, evaluation, or failure analysis of the RAG component itself (e.g. "a RAG chatbot for tourism").
- **E3** General LLM work with no retrieval component (except I4 inference-efficiency work).
- **E4** Not a research paper: editorial, tutorial, product description, thesis abstract only, non-English.
- **E5** Published before 2019 (foundational works are added by citation chasing, not screening).
- **E6** Duplicate of another record.

## Output columns
`record_id, decision, reason_code, note` (note ≤ 15 words, optional)
