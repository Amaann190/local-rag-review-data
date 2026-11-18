# Human spot-check (one co-author, about 60–90 minutes)

This gives the paper a human-vs-AI agreement figure, which reviewers expect when AI tools assist screening.

1. Open `human_check_sample.csv` in Excel or LibreOffice Calc. It holds 150 records drawn at random (seed 20261118) from the 2,994 screened.
2. Read `screening_codebook.md` first.
3. For each row, fill `decision` (include / exclude / unsure) and `reason_code` (I1–I5 or E1–E6), using only the title and abstract.
4. Do not look at `screening_claude.csv`, `screening_codex.csv`, or any `agreement_*` or `disagreements_*` file before you finish.
5. Save as CSV (UTF-8) with the same name and tell Claude it's done. Claude will run:
   `python agreement.py human_check_sample.csv screening_final.csv human final`
   and add the result to the paper.
