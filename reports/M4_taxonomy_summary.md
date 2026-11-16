# M4 - Pilot taxonomy summary

Date: 2026-10-26

## Scope
- Technical inspection of 8 pilot samples only.
- No diagnosis-stratified grouping, colouring, filtering or analysis.
- Pilot observations are not main-cohort findings.

## Classifier and decision
- Decision: D07 in DECISIONS_LOG.md.
- Reference database: SILVA 144.
- Training region: V4-515f-806r.
- Weighting: uniform.
- Build version reported in the README: QIIME 2 2026.7.0.
- Local environment: rachis-qiime2-2026.7.
- Local scikit-learn version: 1.7.1.
- Classifier file: artifacts/pilot/SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza
- Classifier UUID: 76237f8f-87e0-4d1e-93b9-970bb7603cf0
- Alternative considered: a full-length classifier.

### My justification
We select the V4 region model so that it matches the data's V4 region,
and choose the uniform model to avoid habitat-specific weighting,
without claiming that all biases are eliminated.
We accept genus as the maximum expected taxonomic detail for this model,
not a guaranteed assignment level for every ASV.
The selected classifier does not provide species-level assignments.

### Download source
https://www.arb-silva.de/fileadmin/silva_databases/current/QIIME2/2026.7/SSU/V4-515f-806r/uniform/SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza

## Checks
- qiime tools peek reported Type: TaxonomicClassifier.
- qiime tools validate reported valid at level=max.
- classify-sklearn completed successfully in the local environment.
- Validation and successful execution do not establish biological accuracy.
- Cryptographic signature verification was not performed.

## Classification settings
- confidence: 0.7
- read-orientation: auto
- n-jobs: 1
- These were initial default settings, not optimised project settings.

## Inputs
- artifacts/pilot/rep_seqs_240_200.qza
- artifacts/pilot/SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza
- artifacts/pilot/table_240_200.qza was additionally used for the taxa barplot.
- No sample metadata was supplied to the taxa barplot.

## Outputs
- artifacts/pilot/taxonomy_240_200.qza
- artifacts/pilot/taxonomy_240_200.qzv
- artifacts/pilot/taxa_barplot_240_200.qzv

## Taxonomy coverage
The exported taxonomy metadata.tsv contains 630 unique ASV IDs.
The #q2:types metadata row was excluded from ASV counts.

| Terminal taxonomic slot | ASV count | Percentage of 630 ASVs |
| --- | ---: | ---: |
| Genus | 540 | 85.71% |
| Family | 86 | 13.65% |
| Order | 4 | 0.63% |

Percentages are rounded and may not sum to exactly 100%.

Of the 540 ASVs with a genus-slot label, 47 were labelled
g__Incertae_Sedis. A genus-slot label therefore does not necessarily
represent a resolved named genus.

These figures describe ASV counts, not read-weighted classification
coverage. Read-weighted genus coverage was not calculated.

Unresolved genus labels were not used as a reason to remove ASVs
or their counts from the feature table.

## Barplot inspection
- The barplot displayed all 8 pilot samples.
- Level 1 displayed domain-level assignments.
- In this taxonomy, ranks follow d__, k__, p__, c__, o__, f__, g__.
- Genus is therefore displayed at Level 7.
- Some displayed lineages remain unresolved below higher ranks.
- In sample 3053650, the displayed Bacteroides relative frequency
  was 49.607%. This is a descriptive pilot observation only.

The denominator of a taxon's relative frequency is the sum of all
feature counts in the same sample in the input feature table.
Multiplication by 100 converts that fraction to a percentage.

## Interpretation limits
- ASVs are sequence features, not species or individual cells.
- Taxonomy labels and sample-specific counts are separate information.
- Classifier confidence is not sequence identity or an independent
  guarantee of biological correctness.
- A full-length reference model does not supply unmeasured regions
  of the samples' V4 sequences.
- Relative read frequencies are not direct cell proportions.
- Relative abundance barplots do not directly measure sequencing depth
  or provide an alpha-diversity calculation.
- No species-level claims, biomarker claims or diagnosis-related
  conclusions were made.
- Main-cohort processing decisions remain separate from pilot decisions.

## What I learned
Relative abundance barplots show the compositional breakdown of samples,
but they do not directly measure alpha diversity (richness or evenness)
or sequencing depth.

## M4 checkpoint
Date: 2026-10-26
Result: PASS, 4/5 independently correct.

- Q1: Correct.
- Q2: Correct, with clarification about justified threshold changes.
- Q3: Partly correct; corrected after guidance.
- Q4: Correct.
- Q5: Correct.

Review point:
Unresolved genus labels do not automatically justify removing ASVs
or their counts from the feature table.

## Next module
M5: phylogeny, alpha diversity and rarefaction.
No rarefaction sampling depth has been selected.
