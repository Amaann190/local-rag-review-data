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
