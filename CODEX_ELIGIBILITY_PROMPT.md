You are the second independent assessor for stage-2 eligibility in a structured literature review on local, privacy-preserving, hybrid retrieval-augmented generation.

1. Read `eligibility_codebook.md` and apply it exactly.
2. Read `eligibility_input_sample.csv` (300 rows; columns record_id,title,year,venue,abstract).
3. For every row decide eligible yes/no from the title and abstract, list the facets (F1–F6) it addresses, and whether it has evidence (yes/no).
   Boundary conventions: no abstract -> no unless the title alone clearly meets a facet; generic quantization/compression without a stated edge/on-device/CPU deployment setting -> no; pure IR ranking that is not RAG/document QA -> no unless multilingual retrieval is central (F5); domain applications -> yes only if a facet is compared or ablated; surveys -> yes only with an explicit literature-search method.
4. Write `eligibility_codex_sample.csv` with columns record_id,eligible,facets,evidence,note (note under 15 words). One row per input row, same order. Append after each batch of about 50 rows.
5. Judge every record by reading it yourself. Do NOT write keyword, regex, or scoring scripts to decide; scripts may only split input and append rows.
6. Do not open, read, or search any file or folder whose name contains `claude`, `final`, `elig_out`, `eligibility_batches`, `extraction`, `core`, `adjudicated`, or `agreement`. Do not use the web.
7. Keep going through all 300 rows without stopping; if you run out of room, say how far you got. When done, verify 300 rows plus header and print the yes/no counts.
