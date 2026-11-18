# Data extraction and quality appraisal

One row per included study in `extraction.csv`.

## Extraction fields
| Field | Content |
|---|---|
| `study_id` | Citation key used in the paper |
| `record_id` | Screening record id, or `CHASE` if added by citation chasing |
| `theme` | One of: foundations, retrieval, query, grounding, evaluation, efficiency, security |
| `contribution_type` | method / benchmark / empirical-study / system / survey |
| `retrieval` | none / sparse / dense / learned-sparse / hybrid / rerank / n.a. |
| `local_execution` | yes / partial / no / n.a.: whether everything runs on user hardware in the reported setup |
| `abstention` | yes / partial / no: explicit handling of unanswerable queries |
| `citation` | yes / partial / no: answers attributed to sources |
| `security_privacy` | yes / partial / no |
| `multilingual` | none / multilingual / code-mixed |
| `datasets` | Main evaluation datasets (semicolon-separated) |
| `models` | Main retriever/generator models |
| `hardware` | Reported hardware, or `not reported` |
| `key_result` | One-sentence main quantitative result with its number |
| `peer_reviewed` | yes / no (preprint) |

## Quality score (0–4, one point each)
- **Q1 Method:** the method or system is described well enough to reimplement.
- **Q2 Evaluation:** quantitative evaluation against at least one baseline.
- **Q3 Reproducibility:** code or data released, or exact models/datasets/settings stated.
- **Q4 Limitations:** failure modes or limitations are analysed, not only mentioned.

Surveys are scored on Q1 = explicit search method, Q2 = taxonomy grounded in cited work, Q3 = reference list complete and verifiable, Q4 = open problems discussed.
Score 0–1 = low, 2 = moderate, 3–4 = high. Low-quality studies are kept but flagged, and are never the only support for a claim.
