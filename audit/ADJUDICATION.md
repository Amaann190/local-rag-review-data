# Audit adjudication

Two coders coded 54 rows each. Their numeric-inconsistency rates differed sharply (3/24 vs 26/30 full-text rows), so the authors re-applied one strict rule to all 54 full-text rows (see `adjudicate.py`). Changes:

| Record | Column | Coder | Final | Reason |
|---|---|---|---|---|
| R1242 | numeric_inconsistency | no | yes | model-capacity threshold given as 7B and as 3.8B |
| R1598 | numeric_inconsistency | yes | no | 2.49 vs 2.5 is rounding; 'consistently improves' is a claim, not a numeric conflict |
| R1667 | numeric_inconsistency | yes | no | unattributed bound and significance wording are not numeric conflicts |
| R1898 | numeric_inconsistency | yes | no | omitted model run and validity wording are not numeric conflicts |
| R2025 | numeric_inconsistency | yes | no | headline equals best per-table value; identical values are suspicious, not conflicting |
| R2783 | numeric_inconsistency | yes | no | 0.94% is a unit-format slip; 'about seven times' approximates 7.8 |
| R2813 | numeric_inconsistency | yes | no | 'largest gains' is a claim contradicted by numbers, not a numeric conflict |
| R2949 | numeric_inconsistency | yes | no | abstract framing vs table is a claim contradiction |
| R1255 | rag_pipeline | yes | no | notes state no LLM is in the evaluated loop |
| R1642 | judge_location | cloud_llm | cloud_llm | notes state Gemini API judged outputs |

## Round 2: uniform re-check of every full-text 'yes'

All full-text rows coded `yes` (and the `no` rows R1898 and R2025) were re-read against the rule above: `yes` only when the same quantity takes two materially different values, or a stated calculation does not hold; rounding, unit/format slips, naming differences and claim-versus-number contradictions are `no` (see `adjudicate_round2.py`). Changes (Round-1 value = the value after the first pass):

| Record | Column | Round-1 | Final | Reason |
|---|---|---|---|---|
| R2269 | numeric_inconsistency | yes | no | text '21%' matches the tables figure (21.4%) cited for steps; OOD4 5% vs 9% are different conditions (without vs with suggestions) and the rest are claims |
| R2570 | numeric_inconsistency | yes | no | 'additive' gains (0.31+0.21 vs 0.45) is a claim about the numbers, not a stated calculation; prompt-variant scores differ only by a configuration ambiguity |
| R2825 | numeric_inconsistency | yes | no | 4.4 vs 4.53 ms vs about 4.5 ms is rounding; 91-99% vs 0.91-1.00 is a format slip; '2-8 points' is a loose range claim |

Rows kept as `yes` with `inconsistency_detail` trimmed to the qualifying items only (non-qualifying items such as model-name mismatches and claim contradictions removed): R1424, R1642, R1719, R1833, R1895, R2559, R2247.
