# M3 checkpoint — 2026-10-21
- Scope: technical QC of 8 pilot samples only; no diagnosis-stratified analysis.
- D03: targeted 3-prime opposite-primer trimming; no fixed 5-prime trimming.
- Cutadapt: 343605 input pairs; 342927 retained; 678 discarded.
- DADA2: truncation 240/200; maxEE 2/2; minimum overlap 12; independent pooling; consensus chimera removal.
- DADA2: 286481 non-chimeric pairs / 342927 input pairs (83.54%); all 8 samples retained.
- Output: 630 ASVs; representative-sequence lengths 252–254 nt; median 253 nt.
- D06: no sample below 50% retention; settings retained for this pilot, not established as optimal.
- Checkpoint: PASS, 4/5 independently correct; Q4 denominator corrected after guidance.
- Main cohort: primer/run coverage, multiple-run handling, and fallback rules remain unresolved.
