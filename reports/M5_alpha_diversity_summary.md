# M5 - Phylogeny, alpha diversity and rarefaction

Report date: 2026-11-02
Environment: rachis-qiime2-2026.7

## Scope

Technical inspection of 8 pilot samples only.
No diagnosis-stratified grouping, colouring, filtering or statistical testing.
Pilot observations are not main-cohort findings.
The pilot sampling depth is not automatically applicable to the main cohort.

## Input artifacts

- artifacts/pilot/rep_seqs_240_200.qza
- artifacts/pilot/table_240_200.qza

Original feature table:
- Samples: 8
- Unique ASVs across the table: 630
- Total counts: 286481
- Minimum sample count: 15233
- Median sample count: 36538.5
- Maximum sample count: 65242

## Phylogenetic tree

Pipeline: qiime phylogeny align-to-tree-mafft-fasttree

Steps:
1. Multiple sequence alignment with MAFFT.
2. Alignment masking.
3. Unrooted tree inference with FastTree.
4. Midpoint rooting.

Outputs:
- artifacts/pilot/aligned_rep_seqs_240_200.qza
- artifacts/pilot/masked_aligned_rep_seqs_240_200.qza
- artifacts/pilot/unrooted_tree_240_200.qza
- artifacts/pilot/rooted_tree_240_200.qza

All four outputs were successfully saved.
Successful execution does not establish the biological accuracy of every branch.

Taxonomic labels were not required to construct this tree.
Masking filters alignment columns; it does not merge ASV IDs or add their counts.

## Exploratory alpha rarefaction

Action: qiime diversity alpha-rarefaction

Settings:
- Maximum depth: 65000
- Steps: 10
- Iterations per depth: 10
- Metrics: observed_features, shannon, faith_pd
- Rooted tree supplied.
- No sample metadata supplied.

Output:
- artifacts/pilot/alpha_rarefaction_240_200_max65000.qzv

Exported CSV files were inspected for all three metrics.

Sample availability at selected tested depths:
| Depth | Samples with results |
| --- | --- |
| 7223 | 8 |
| 14445 | 8 |
| 21667 | 6 |
| 36111 | 4 |
| 65000 | 1 |

At depths exceeding a sample's available counts, its CSV entries were blank.
Apparent drops to zero in the visualization were not interpreted as
biological losses of diversity.

The exploratory maximum was not the final sampling depth.
A plateau supports stability of a particular metric over the inspected
depth range; it does not prove complete recovery of microbial diversity.

## Final pilot sampling-depth decision

Chosen depth: 15000 counts per sample.

My justification:
I choose a depth of 15000 so that I can retain and examine all 8 pilot
samples. I accept that counts above this depth in higher-count samples
will not be used in the rarefied table.

The decision and alternatives are recorded in DECISIONS_LOG.md.
The exact depth of 15000 was not part of the initial exploratory depth grid.

Action: qiime feature-table rarefy
- sampling-depth: 15000
- with-replacement: false
- random-seed: 20261031

Output:
- artifacts/pilot/table_240_200_rarefied_15000.qza

Verification:
- Samples retained: 8 of 8
- Minimum sample count: 15000
- Maximum sample count: 15000
- Total counts: 120000
- Unique ASVs across the rarefied table: 618

Twelve ASVs present in the original table were not represented by any
nonzero counts in the rarefied table.
This is not evidence that those ASVs were contaminants or sequencing errors.
The original feature table was not modified.

The fixed seed supports reproducibility of this subsampling.
It does not guarantee retention of all genuine ASVs.
Sensitivity to alternative rarefaction seeds was not evaluated.

## Alpha diversity calculations

All three metrics were calculated from the same rarefied table.
No additional rarefaction was performed for individual metrics.

Observed features:
- Action: qiime diversity alpha
- Metric: observed_features
- Counts ASVs with nonzero abundance in each sample.

Shannon:
- Action: qiime diversity alpha
- Metric: shannon
- Reflects both richness and abundance evenness.

Faith PD:
- Action: qiime diversity alpha-phylogenetic
- Metric: faith_pd
- Uses the rooted tree.
- Sums branch lengths connecting the ASVs present to the root.
- Shared branches are counted once.
- Relative abundances do not directly weight this metric.

Outputs:
- artifacts/pilot/observed_features_15000.qza
- artifacts/pilot/shannon_15000.qza
- artifacts/pilot/faith_pd_15000.qza
- artifacts/pilot/alpha_diversity_15000.qzv

## Results

All 8 samples had values for all three metrics.
Values below are rounded to three decimal places, except ASV counts.

| Sample ID | Observed features | Shannon | Faith PD |
| --- | --- | --- | --- |
| 2043650 | 233 | 6.627 | 16.424 |
| 2071650 | 105 | 4.412 | 9.780 |
| 2547670 | 186 | 4.703 | 15.100 |
| 2571650 | 125 | 5.629 | 10.546 |
| 2733650 | 168 | 5.742 | 11.261 |
| 2771670 | 165 | 5.412 | 11.821 |
| 2773651 | 141 | 5.118 | 10.571 |
| 3053650 | 84 | 4.347 | 6.833 |

Sample 2547670 had more observed ASVs than sample 2571650,
but a lower Shannon value.
Richness alone therefore did not determine the Shannon ranking.
The alpha-diversity table alone does not identify a dominant ASV or taxon.

These are descriptive technical-pilot observations only.

## Limitations

- ASVs are not equivalent to species or individual bacterial cells.
- Equal sampling depth does not imply equal richness or evenness.
- Rarefaction can omit low-abundance ASVs.
- Complete saturation was not established for all metrics and samples.
- Faith PD depends on the inferred tree and its branch lengths.
- The short V4 marker does not represent complete genome-wide evolution.
- Alpha diversity alone does not establish microbiome health.
- No CRC-versus-control comparisons or disease conclusions were made.
- A significant association in a future observational analysis would not,
  by itself, establish causation.
- Small sample size alone does not establish zero statistical power
  or prove that a significant result is false.

## What I learned

I can distinguish feature counts, ASV sequences and taxonomic annotations.
I can explain alignment, masking and the role of a rooted phylogenetic tree.
I can distinguish richness, abundance evenness and phylogenetic diversity.
I can justify a sampling-depth choice and describe the information it costs.
I can distinguish missing rarefaction results from zero diversity.
I can distinguish reproducibility from biological validity.
I can explain why diversity alone does not establish health or causality.

## M5 checkpoint

Completed: 2026-11-02
Result: PASS, 4 of 5 independently correct.

- Q1: Correct, with clarification about seeds and stochastic subsampling.
- Q2: Correct, with clarification about branch lengths and taxonomic labels.
- Q3: Partly correct; corrected after guidance.
- Q4: Correct.
- Q5: Correct in both requested core aspects, with statistical clarifications.

Review points:
- max-depth controls actual exploratory rarefaction computations.
- Missing values at unattainable depths are not zero diversity.
- A plateau does not establish complete recovery of all microorganisms.
- Power depends on more than sample size.
- Calling an analysis exploratory does not override the pilot restrictions.

## Next module

M6: beta diversity.

Topics:
- Bray-Curtis and Jaccard
- Weighted and unweighted UniFrac
- PCoA and Emperor
- PERMANOVA and PERMDISP
- Confounding, dispersion and pseudoreplication

Pilot restrictions remain in force.
No diagnosis-stratified analysis will be introduced without resolving
the transition to the main cohort and its outstanding processing decisions.

## Method references

- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/phylogeny/
- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/alignment/
- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/feature-table/
- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/diversity/
- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/metadata/
