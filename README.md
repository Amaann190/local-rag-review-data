# Local Hybrid RAG Review: Protocol and Data

Data and scripts for the systematic mapping review *Hybrid Retrieval-Augmented Generation on Local Hardware: A Systematic Mapping Review with Evidence-Based Design Requirements* (Halani, Shaikh, Shaikh, Singh, Shaikh; St. John College of Engineering & Management, 2026).

Everything needed to check or re-run the review is here: search queries and raw results, both screeners' decisions, agreement statistics, eligibility decisions, the data extracted from the core studies, and the scripts behind every number in the paper.

## Pipeline and numbers

| Stage | Records | Files |
|---|---|---|
| Search (OpenAlex + arXiv, 17 Nov 2026, 10 queries, top 200 per query) | 3,693 | `queries.json`, `search.py`, `raw/` |
| Deduplication (DOI, arXiv id, normalized title) | 2,994 unique | `dedup.py`, `records_dedup.json`, `dedup_stats.json` |
| Stage 1: title/abstract screening | 2,354 advanced | `screening_codebook.md`, `screening_input.csv`, `screening_claude.csv`, `screening_codex*.csv` |
| Stage 2: research-question eligibility | 1,259 eligible | `eligibility_codebook.md`, `eligibility_final.csv`, `eligibility_batches/` |
| Core synthesis (local deployment + another facet) | 108 extracted | `extraction_codebook.md`, `extraction.csv`, `extraction/` |

PRISMA counts are in `prisma.json`; facet and year counts in `mapping.json`; figures in `fig_*.pdf`.

## Screening and agreement

Screener A (Claude, Anthropic) screened every record at both stages. Screener B (Codex, OpenAI) worked independently, without access to Screener A's decisions, on random samples:

| Stage | Sample | Agreement | Cohen's κ | Files |
|---|---|---|---|---|
| Title/abstract (pilot, first 110 records) | 110 | 84.5% | 0.58 | `screening_codex.csv` |
| Title/abstract (seeded random) | 500 | 88.4% | 0.66 | `screening_input_sample.csv`, `screening_codex_sample.csv`, `agreement_claude_vs_codex_sample.json` |
| Eligibility (seeded random) | 300 | 82.7% | 0.65 | `eligibility_input_sample.csv`, `eligibility_codex_sample.csv`, `agreement_eligibility_claude_vs_codex.json` |

Disagreements are listed in `disagreements_*.csv`. The prompts given to Screener B are in `CODEX_*_PROMPT.md`. A 150-record human check sample with instructions is in `human_check_sample.csv` and `HUMAN_CHECK_INSTRUCTIONS.md`.

The human authors wrote the protocol and codebooks, reviewed boundary cases, and adjudicated disagreements.

## Other files

- `effect_sizes.csv`: effect sizes quoted in the paper, with the table or section each value was copied from.
- `core_ids.json`: record IDs of the 108 core studies.
- `mapping_stats.py`: produces `prisma.json`, `mapping.json`, and the figures.
- `agreement.py`: computes agreement and κ between any two screening files.
- `make_core_bib.py`: builds the reference entries for the cited core studies.

## Reproducing

Python 3.10+ with `matplotlib`:

```bash
python search.py          # re-runs the search (results will differ as the indexes grow)
python dedup.py
python agreement.py screening_claude.csv screening_codex_sample.csv claude codex_sample
python mapping_stats.py
```

Re-running `search.py` queries live APIs, so it will not return exactly the same records. The saved `raw/` files are the records this review used.

## Limitations

The search covered two databases with top-200 relevance truncation per query. Both screeners are AI models; the second screener covered random samples rather than every record. Half of the core studies were extracted from abstracts only, and their quality scores are conservative. See the paper's Threats to Validity section.

## License

Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts: MIT. Bibliographic metadata comes from OpenAlex (CC0) and arXiv.
