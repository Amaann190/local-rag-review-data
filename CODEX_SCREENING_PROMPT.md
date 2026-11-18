# Prompt for the Codex app (second, independent screener)

Open the Codex app on the folder `Review & Result Paper/review-protocol` and paste everything below the line.

---

You are the second independent screener for a structured literature review on local, privacy-preserving, hybrid retrieval-augmented generation.

1. Read `screening_codebook.md`. Apply it exactly.
2. Read `screening_input.csv`. Columns: `record_id, title, year, venue, abstract`.
3. For every row, decide `include`, `exclude`, or `unsure` from the title and abstract only, following the codebook. For `exclude`, give the first reason code that applies (E1–E6). For `include`, give the main inclusion code (I1–I5).
4. Write `screening_codex.csv` with columns `record_id,decision,reason_code,note`. One row per input row, same order, no rows skipped. Keep `note` under 15 words.
5. Do not open, read, or search for any file whose name contains `claude`, `adjudicated`, or `final`. Do not use the web. Decide independently.
6. There are 2,994 rows. Work through them in batches (for example 150 rows at a time), appending to `screening_codex.csv` after each batch so progress is saved. Judge every record by reading its title and abstract yourself. Do NOT write a keyword, regex, or scoring script to make the decisions; scripts may only be used to split the input and append rows.
7. When finished, verify the output has exactly 2,994 rows plus the header, then print the counts of include / exclude / unsure.
