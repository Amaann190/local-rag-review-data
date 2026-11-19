# Local Hybrid RAG Review: Protocol and Data

Data and scripts for the systematic mapping review *Hybrid Retrieval-Augmented Generation on Local Hardware: A Systematic Mapping Review with Evidence-Based Design Requirements* (Halani, Shaikh, Shaikh, Singh, Shaikh; St. John College of Engineering & Management, 2026).

Everything needed to check or re-run the review is here: the executed queries and the normalized records they returned, both screeners' decisions, agreement statistics, eligibility decisions with exclusion reasons, the data extracted from the core studies, the audit coding, and the scripts behind every number in the paper.

## Pipeline and numbers

| Stage | Records | Files |
|---|---|---|
| Search (OpenAlex + arXiv, 17 Nov 2026, 10 queries, top 200 per query) | 3,693 | `queries.json`, `search.py`, `raw/` |
| Deduplication (DOI, arXiv id, normalized title) | 2,994 unique (698 duplicates + 1 untitled removed) | `dedup.py`, `records_dedup.json`, `dedup_stats.json` |
| Stage 1: title/abstract screening | 2,362 advanced (incl. 8 from the sensitivity re-screen) | `screening_codebook.md`, `screening_input.csv`, `screening_claude.csv`, `screening_codex*.csv`, `audit/sensitivity_*.csv` |
| Stage 2: research-question eligibility | 1,261 eligible | `eligibility_codebook.md`, `eligibility_final.csv` (with `exclusion_reason`), `eligibility_batches/` |
| Core set (local deployment + another facet) | 108 extracted (54 full text, 54 abstract) | `extraction_codebook.md`, `extraction.csv`, `extraction/` |
| Local RAG set (RAG pipeline with a local generator on user-controlled hardware) | 50 (of 73 with a local generator: 8 on hosted GPUs and 15 with no stated execution host set aside; a host needs named hardware or an explicit statement that the tested system ran locally, stored as a verified exact quote in `audit/execution_host.csv`) | `audit_codebook.md`, `audit/`, `core_stats.json` |

PRISMA counts are in `prisma.json`; facet and year counts in `mapping.json`; all core and local-RAG statistics, with the record IDs behind each count, in `core_stats.json`; figures in `fig_*.pdf`.

`raw/records_raw.json` holds the normalized records parsed from the API responses (title, abstract, authors, venue, year, identifiers, query). The original API payloads were not archived.

## Screening and agreement

Screener A (Claude, Anthropic) screened every record at both stages. Screener B (Codex, OpenAI) worked independently, without access to Screener A's decisions, on random samples:

| Stage | Sample | Agreement | Cohen's κ | Files |
|---|---|---|---|---|
| Title/abstract (pilot, first 110 records) | 110 | 84.5% | 0.58 | `screening_codex.csv` |
| Title/abstract (seeded random) | 500 | 88.4% | 0.66 | `screening_input_sample.csv`, `screening_codex_sample.csv`, `agreement_claude_vs_codex_sample.json` |
| Eligibility (seeded random) | 300 | 82.7% | 0.65 | `eligibility_input_sample.csv`, `eligibility_codex_sample.csv`, `agreement_eligibility_claude_vs_codex.json` |

Disagreements are listed in `disagreements_*.csv`. The prompts given to Screener B are in `CODEX_*_PROMPT.md`.

Screeners saw at most 2,500 abstract characters; 98 records had no abstract. The 28 exclusions affected by this were re-screened with the full abstract or title (`sensitivity_prep.py`, `apply_sensitivity.py`): 8 advanced to Stage 2 and 2 were eligible.

## Audit coding of the core set

After an independent review of the manuscript, every core study was coded with explicit variables (`audit_codebook.md`): whether it is a RAG pipeline, where the generator and any judge run, the execution host (user device, own server, hosted service, or not stated; `audit/execution_host.csv`), hybrid and reranker use, named hardware, public benchmark, attack experiment, and (full-text studies only) numeric inconsistency with the specific discrepancy. Two coders coded half each; their numeric-inconsistency rates differed, so the authors re-applied one rule to all full-text studies. Every change is logged in `audit/ADJUDICATION.md` (`audit/adjudicate.py`). The coders' own exports were not kept; `audit/original/` holds reconstructions made by reversing the log, which restore the coded values but not the coders' free-text discrepancy details (see `audit/original/README.md`). `core_stats.py` merges the coding into `extraction.csv` and writes `core_stats.json`.

Other data corrections are scripted and documented: `fix_eligibility_reasons.py` (explicit exclusion reasons, including the authors' own prior version, R2064) and `fix_peer_review.py` (two studies accepted at peer-reviewed venues).

## Other files

- `effect_sizes.csv`: results quoted in the paper, with the table or section each value was copied from.
- `core_ids.json`: record IDs of the 108 core studies.
- `mapping_stats.py`: produces `prisma.json`, `mapping.json`, and the figures.
- `agreement.py`: computes agreement and κ between any two screening files.
- `make_core_bib.py`: drafts reference entries for cited core studies from metadata (entries in the paper were then normalized by hand).

## Reproducing

Python 3.10+ with `matplotlib`:

```bash
python search.py          # re-runs the search (results will differ as the indexes grow)
python dedup.py
python agreement.py screening_claude.csv screening_codex_sample.csv claude codex_sample
python audit/code_execution_host.py
python core_stats.py      # run before mapping_stats.py, which reads core_stats.json
python mapping_stats.py
```

### Building the paper

The paper's LaTeX source sits one folder above this repository and is not part of it. It loads the figures with `\graphicspath{{review-protocol/}{../}{./}}`, so it builds from that parent folder (the folder containing both the `.tex` file and `review-protocol/`) or from any direct subfolder of `review-protocol/`:

```bash
pdflatex DocMind_AI_Review_Paper_v3.tex
pdflatex DocMind_AI_Review_Paper_v3.tex
```

To build elsewhere, copy `fig_facets.pdf` and `fig_years.pdf` next to the `.tex` file.

Re-running `search.py` queries live APIs, so it will not return exactly the same records. The saved `raw/` files are the records this review used.

## Limitations

The search covered two databases with top-200 relevance truncation per query. Both screeners are AI models; the second screener covered random samples rather than every record. Half of the core studies were extracted from abstracts only, and audit variables (including the execution host) were coded from the extraction records rather than re-read from the papers, so the numeric-discrepancy count reflects only what extractors noted. See the paper's Threats to Validity section.

## License

Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts: MIT. Bibliographic metadata comes from OpenAlex (CC0) and arXiv.
