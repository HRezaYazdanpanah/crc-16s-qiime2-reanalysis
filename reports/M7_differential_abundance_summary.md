# M7 — Differential abundance: concepts and pilot preparation

Report date: 2026-11-10
Project: CRC stool 16S reanalysis
Environment used: rachis-qiime2-2026.7

## 1. Status and scope

- Conceptual checkpoint: passed, with 4 of 5 answers graded correct.
- Pilot genus aggregation and prevalence filtering: completed.
- ANCOM-BC2 availability: confirmed using its command-line help.
- ANCOM-BC2 model fitting: NOT performed.
- Main-cohort differential abundance analysis: NOT completed.

The pilot was used for technical preparation only.
No diagnosis-stratified differential abundance model, plot, or test was
performed in M7. No CRC-versus-control biological findings are reported.

## 2. Questions addressed

- Why can relative abundance change without a corresponding change
  in absolute abundance?
- Why use an unrarefied count table for the planned ANCOM-BC2 analysis?
- What information is lost through genus-level aggregation?
- What does prevalence filtering remove?
- How do formula and reference-level choices define a comparison?
- How do effect size and statistical significance differ?
- Why are sequencing runs not independent biological replicates?

## 3. Inputs and provenance

Unrarefied ASV count table:
artifacts/pilot/table_240_200.qza

Artifact UUID:
6602aac4-992b-4c44-a8ff-fa9dda671e16

Confirmed semantic type:
FeatureTable[Frequency]

The artifact's action record identifies it as the table output of
dada2 denoise_paired, with trunc_len_f = 240 and trunc_len_r = 200.
It is a post-denoising count table, not raw sequencing data and not
a rarefied table.

Taxonomy:
artifacts/pilot/taxonomy_240_200.qza

Pilot metadata:
metadata/pilot_metadata.tsv

Sample-frequency artifact used for ID and count inspection:
artifacts/pilot/sample_frequencies_240_200.qza

## 4. Metadata and sample identity checks

The eight sample IDs displayed in the sample-frequency visualization
matched the eight IDs in pilot_metadata.tsv.

No duplicate sample-id or Run entries were observed in that metadata file.

The uploaded SRA run table contained examples of multiple runs linked
to the same Sample Name and BioSample. Such runs must not be treated
as independent biological replicates.

These checks do not establish that every distinct sample belongs to
a different participant. Participant-to-sample mapping remains to be
documented. Main-cohort multi-run handling remains unresolved.

Sample counts before prevalence filtering ranged from 15,233 to 65,242.
Counts represent sequence observations, not measured cell numbers.

## 5. Genus-level aggregation

Command executed:

```bash
qiime taxa collapse \
  --i-table artifacts/pilot/table_240_200.qza \
  --i-taxonomy artifacts/pilot/taxonomy_240_200.qza \
  --p-level 6 \
  --o-collapsed-table artifacts/pilot/genus_table_240_200.qza
```

Rationale:
Genus was the planned reporting level for this project. Aggregation
sacrifices ASV-level resolution within each aggregated taxonomic group.

Interpretation limit:
These are features aggregated at taxonomic level 6, not necessarily
69 distinct confidently named genera. Taxonomic uncertainty remains.

## 6. Pilot prevalence-filter decision

Chosen cutoff: 0.2, evaluated across all eight pilot samples together.
Diagnosis labels were not used to define the filter.

Rationale:
Remove features detected in only one sample and retain features
detected in at least two samples.

With eight samples, prevalence cutoffs of 0.2 and 0.25 retain the same
features: presence in at least two samples is required.

Command executed:

```bash
qiime feature-table filter-features \
  --i-table artifacts/pilot/genus_table_240_200.qza \
  --p-min-samples 2 \
  --o-filtered-table artifacts/pilot/genus_table_240_200_prev20.qza
```

This threshold is a pilot technical decision and is not automatically
adopted for the main cohort.

## 7. Observed filtering results

| Metric | Before | After | Removed |
|---|---:|---:|---:|
| Samples | 8 | 8 | 0 |
| Aggregated taxonomic features | 69 | 53 | 16 |
| Total count | 286481 | 286300 | 181 |

Approximately 99.94% of total counts were retained.

Removing 16 features while retaining nearly all counts shows that
feature retention and count retention describe different aspects
of filtering. No samples were lost in this filtering step.

Summary output directories:
- artifacts/pilot/M7_genus_before/
- artifacts/pilot/M7_genus_after/

## 8. Modeling concepts covered — not an executed analysis

- Formula specifies the variables included in the model.
- Reference level defines the baseline for categorical comparisons.
- A positive log-fold change for cancer versus normal indicates a
  higher model-estimated abundance in cancer; a negative value
  indicates a lower model-estimated abundance.
- Effect size describes the magnitude and direction of a difference.
- Statistical significance does not establish biological importance.
- Failure to reach a significance threshold does not prove no difference.
- Adjusted significance measures must be reported together with the
  multiple-testing adjustment method.
- ANCOM-BC2 inference is model-based; it does not directly measure cells.
- DESeq2 was discussed as a negative-binomial count-model framework
  for bulk RNA-seq. Its use for microbiome data requires consideration
  of normalization assumptions and compositionality.

No model formula, reference level, p-value adjustment method, or
significance threshold has been finalized for the main-cohort analysis.

## 9. Checkpoint and learning gaps

| Question | Topic | Grade |
|---|---|---|
| 1 | Compositionality and causal attribution | Partly correct |
| 2 | Prevalence calculation and filtering target | Correct |
| 3 | Log-fold change direction and q-value | Correct |
| 4 | Unrarefied input for ANCOM-BC2 | Correct, wording refined |
| 5 | Filtering-plan changes and transparency | Correct, terminology refined |

Result: 4/5 correct; conceptual checkpoint passed.

Points to retain:
- An indirect effect can still be causal.
- Temporal order alone does not establish causality.
- Unrarefied does not mean unprocessed.
- Group-dependent feature selection is distinct from dependence
  between biological samples.
- Changes to an analysis plan must be dated, justified, and disclosed;
  exploratory analyses must not be presented as prespecified.

## 10. Outstanding work before practical completion of M7

1. Document participant-to-sample relationships.
2. Resolve main-cohort multi-run handling and processing decisions.
3. Confirm suitable processed main-cohort data are available.
4. Audit metadata matching, missingness, covariates, site/batch
   structure, and biological independence.
5. Finalize and log the analysis population, genus-level filtering,
   model formula, reference levels, and multiple-testing strategy.
6. Fit ANCOM-BC2 on the appropriate non-pilot dataset.
7. Inspect model warnings and robustness information.
8. Export and interpret actual estimates and adjusted results.

No differential abundance or causal claims can be drawn from the
technical filtering results reported here.

## 11. Documentation

- QIIME 2 feature-table:
  https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/feature-table/
- QIIME 2 taxa:
  https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/taxa/
- QIIME 2 composition:
  https://amplicon-docs.qiime2.org/en/2026.7/references/plugins/composition/
- ANCOM-BC2 tutorial:
  https://bioconductor.org/packages/release/bioc/vignettes/ANCOMBC/inst/doc/ANCOMBC2.html

## Correction (2026-11-16)

The pilot table in this report was built with `taxa collapse --p-level 6`
and called genus-level. With the SILVA 144 classifier used here, level 6
is family, not genus (ranks: d, k, p, c, o, f, g).
Feature counts in this pilot report therefore refer to family-level groups.
The pilot was a technical exercise and none of its results are findings.
The main analysis uses level 7.
