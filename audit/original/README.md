# Reconstructed pre-adjudication coding

These two files are **reconstructions**, not the coders' contemporaneous exports. The coders' own files were overwritten during adjudication and were not kept.

`../archive_original_coding.py` rebuilt them by taking the adjudicated files (`../audit_part1.csv`, `../audit_part2.csv`) and reversing every change logged in `../ADJUDICATION.md`. This restores the coded values, including the initial full-text numeric-inconsistency counts (3 of 24 for part 1, 26 of 30 for part 2).

What is not restored: the log recorded only coded values, not the coders' free-text `inconsistency_detail`. As a result:

- Rows the adjudication changed from `yes` to `no` (R1598, R1667, R1898, R2025, R2783, R2813, R2949) show `yes` with an empty detail.
- R1242, changed from `no` to `yes`, shows `no` with the detail written at adjudication.

Use these files for the coded values only. The adjudicated files in `../` are the ones the paper's statistics come from.
