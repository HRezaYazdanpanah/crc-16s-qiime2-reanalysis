# M6 - Beta diversity

Report date: 2026-11-10
Environment used: rachis-qiime2-2026.7
Project: CRC stool 16S reanalysis

## 1. Scope

Technical and educational inspection of 8 pilot samples only.

No diagnosis-stratified grouping, colouring, filtering or statistical
testing was performed in M6. No CRC-versus-control findings are reported.

The main-cohort analysis and its outstanding processing decisions remain
separate from this pilot exercise. Completion of M6 does not mean that
the planned main-cohort statistical analysis has been completed.

## 2. Questions addressed

- How different are the microbial compositions of samples?
- How does the definition of dissimilarity change across metrics?
- What changes when abundance and phylogenetic relationships are included?
- What can and cannot be inferred from a PCoA visualization?
- What do PERMANOVA and PERMDISP test?
- How do dependence, confounding and permutation design affect inference?

## 3. Inputs

Feature table:
artifacts/pilot/table_240_200_rarefied_15000.qza

Rooted phylogenetic tree:
artifacts/pilot/rooted_tree_240_200.qza

Non-diagnostic metadata used for Emperor:
artifacts/pilot/observed_features_15000.qza

The rarefied table was created and checked in M5:
- Samples: 8.
- Counts per sample: 15000.
- Total counts: 120000.
- Unique ASVs across the table: 618.
- Rarefaction without replacement.
- Random seed used in M5: 20261031.

M6 reused this same rarefied table for all four metrics.
No additional rarefaction was performed in M6.
The original, unrarefied feature table was not modified.

## 4. Metrics calculated

| Metric | Uses abundance differences? | Uses phylogeny? |
| --- | --- | --- |
| Bray-Curtis | Yes | No |
| Jaccard | No; presence/absence | No |
| Unweighted UniFrac | No; presence/absence | Yes |
| Weighted UniFrac | Yes; relative abundance along branches | Yes |

Bray-Curtis was calculated on the equal-depth count table.

Jaccard compares the sets of ASVs present in samples.

Unweighted UniFrac compares the phylogenetic branch coverage of samples.

Weighted UniFrac incorporates relative abundance differences along
phylogenetic branches.

The selected weighted metric was weighted_unifrac, not
weighted_normalized_unifrac. Its values must not automatically be
assumed to lie between zero and one.

Taxonomic labels were not inputs to these distance calculations.
ASVs were not treated as equivalent to species or strains.

## 5. Workflow performed

Non-phylogenetic metrics:
Feature table -> qiime diversity beta -> DistanceMatrix

Phylogenetic metrics:
Feature table + rooted tree
-> qiime diversity beta-phylogenetic -> DistanceMatrix

For each metric:
DistanceMatrix -> qiime diversity pcoa -> PCoAResults
PCoAResults + non-diagnostic metadata -> qiime emperor plot -> Visualization

PCoA used the previously calculated distance matrix.
It did not recalculate the metric from ASV counts.

Emperor displayed the existing coordinates.
It did not recalculate distances, alter the tree or repeat rarefaction.

## 6. Output inventory

### Bray-Curtis

- artifacts/pilot/bray_curtis_15000.qza
- artifacts/pilot/bray_curtis_pcoa_15000.qza
- artifacts/pilot/bray_curtis_emperor_15000.qzv

### Jaccard

- artifacts/pilot/jaccard_15000.qza
- artifacts/pilot/jaccard_pcoa_15000.qza
- artifacts/pilot/jaccard_emperor_15000.qzv

### Unweighted UniFrac

- artifacts/pilot/unweighted_unifrac_15000.qza
- artifacts/pilot/unweighted_unifrac_pcoa_15000.qza
- artifacts/pilot/unweighted_unifrac_emperor_15000.qzv

### Weighted UniFrac

- artifacts/pilot/weighted_unifrac_15000.qza
- artifacts/pilot/weighted_unifrac_pcoa_15000.qza
- artifacts/pilot/weighted_unifrac_emperor_15000.qzv

Successful creation and visualization of these outputs was documented
during the course conversation. The shell check accompanying this report
checks current file presence and non-zero size only; it is not a QIIME 2
artifact validation or a numerical audit of the distance matrices.

## 7. PCoA results observed

Percentages were transcribed from the submitted Emperor screenshots.
Totals below are sums of the displayed, rounded percentages.

| Metric | Axis 1 (%) | Axis 2 (%) | Axis 3 (%) | Sum of axes 1-3 (%) |
| --- | ---: | ---: | ---: | ---: |
| Bray-Curtis | 23.44 | 20.78 | 15.58 | 59.80 |
| Jaccard | 21.19 | 18.26 | 14.79 | 54.24 |
| Unweighted UniFrac | 25.46 | 19.21 | 14.76 | 59.43 |
| Weighted UniFrac | 45.47 | 25.90 | 10.43 | 81.80 |

Additional exploratory views:
- Bray-Curtis Axis 4: 14.49%; axes 1, 2 and 4 sum to 58.71%.
- Jaccard Axis 4: 13.42%; axes 1, 2 and 4 sum to 52.87%.

Eight of eight samples were visible in the submitted visualizations.

The first three axes represented a larger share of the reported
variation for weighted UniFrac than for the other metrics.

This does not establish that weighted UniFrac is biologically superior.
Each ordination summarizes its own metric-specific distance matrix.

No disease effect, significant group separation or contamination was
inferred from these plots.

## 8. Visualization interpretation and limitations

- A point represents a sample, not an ASV.
- Rotating the plot changes the view, not the original distances.
- Changing displayed axes selects a different projection.
- A three-axis view does not show the complete distance structure.
- Nearby points in a projection do not establish identical composition.
- Axes represent variation in the distance structure, not correlations
  with disease and not percentages of bacteria or ASVs.
- A visually isolated sample is not, by itself, evidence of contamination.
- Sample exclusion requires independent evidence and a documented rule.
- Colours must not be assumed to identify the same samples across plots
  unless the sample IDs and colour settings have been checked.
- No quantitative pairwise-distance comparison, Mantel test or Procrustes
  comparison was performed.
- No robustness analysis across rarefaction seeds or depths was performed.
- Presence/absence metrics can be affected by whether low-abundance ASVs
  are detected in the selected subsample.
- Phylogenetic metrics depend on the inferred tree and its branch lengths.
- No validation of every branch or negative-eigenvalue audit is claimed.

## 9. Statistical concepts covered, not executed on diagnosis groups

### PERMANOVA

PERMANOVA operates on a distance matrix and a statistical design,
rather than only the first three displayed PCoA axes.

The pseudo-F statistic relates between-group and within-group variation.
Permutation testing evaluates the observed statistic against a null
distribution generated using exchanges allowed by the study design.

R-squared describes the share of distance-based variation assigned to
a model term under the specified model and testing approach.

A small p-value does not establish a large effect or biological importance.

### PERMDISP

PERMDISP tests differences in within-group dispersion.

PERMANOVA can be sensitive to both location and dispersion differences.
If PERMDISP is significant, the PERMANOVA result must not be attributed
solely to a shift in group centres.

Significant results from both tests do not quantify how much of the
PERMANOVA result is due to dispersion versus location.

A non-significant PERMDISP result does not prove equal dispersion.

### Dependence and permutation design

Technical sequencing replicates do not increase the number of independent
biological replicates.

Treating dependent observations as independent creates pseudoreplication
and can underestimate uncertainty.

For a simple paired before/after comparison, permitted label exchanges
must preserve subject pairing.

Other repeated-measures or between-subject questions require permutation
designs appropriate to their own hypotheses and sampling structure.

### Confounding and causality

If all cases are processed in one laboratory and all controls in another,
disease and laboratory are completely confounded.

Adding both variables to a model cannot recover separate effects that
the design does not identify.

An association in an observational study does not establish causality.

All statistical p-values and R-squared values discussed in the teaching
examples were hypothetical, not results from this pilot.

No PERMANOVA or PERMDISP was executed in M6.

## 10. M6 checkpoint

Completed: 2026-11-10
Result: PASS - 4 of 5 independently correct.

| Question | Topic | Assessment |
| --- | --- | --- |
| Q1 | Four metrics and question-based metric selection | Correct |
| Q2 | PCoA projections and explained variation | Correct |
| Q3 | R-squared, PERMANOVA, PERMDISP and causality | Partly correct; corrected after guidance |
| Q4 | Pseudoreplication and complete confounding | Correct |
| Q5 | Distance-matrix input and paired permutations | Correct |

Clarifications retained:
- Jointly significant PERMANOVA and PERMDISP do not partition the
  contributions of location and dispersion.
- The magnitude of false-positive inflation from pseudoreplication was
  not calculated in the hypothetical example.
- Using only three axes discards some information, not necessarily most
  of it; the amount depends on the axes retained.

## 11. I can now explain

- Alpha diversity versus beta diversity.
- Count tables, distance matrices, PCoA coordinates and Emperor plots.
- Bray-Curtis versus Jaccard.
- Weighted versus unweighted UniFrac.
- Why UniFrac requires a phylogenetic tree.
- Why metric selection must follow the research question.
- Why a three-dimensional view is incomplete.
- Effect size versus statistical significance.
- The distinct roles and limitations of PERMANOVA and PERMDISP.
- Pseudoreplication and biological versus technical replication.
- Complete confounding and limits of statistical adjustment.
- Why permutations must respect the experimental design.
- Why observational associations do not establish causality.

## 12. Status and next module

M6 educational objectives and checkpoint are complete for the pilot scope.

The main-cohort inferential analysis remains outstanding.
No main-cohort decisions are changed by this report.

Next: M7 - compositionality and differential abundance.
Do not assume that the rarefied diversity table is the appropriate input
for differential abundance; choose the input and method explicitly.

This report does not replace the original commands, artifact provenance,
DECISIONS_LOG.md, or the later reproducibility work in M8.

## 13. Method references

- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/diversity/
- https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/emperor/
- https://scikit.bio/docs/dev/generated/skbio.diversity.beta.unweighted_unifrac.html
- https://scikit.bio/docs/dev/generated/skbio.diversity.beta.weighted_unifrac.html
- https://vegandevs.github.io/vegan/reference/adonis.html
- https://vegandevs.github.io/vegan/reference/permutations.html
- https://scikit.bio/docs/dev/generated/skbio.stats.distance.permdisp.html
