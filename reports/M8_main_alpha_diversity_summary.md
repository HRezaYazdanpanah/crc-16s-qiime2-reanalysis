# M8 — Descriptive main-subset alpha diversity

Date: 2026-11-16

## Scope and timing

Descriptive addition approved after viewing main community-analysis,
ANCOM-BC2 and PCoA results.
Not a prespecified confirmatory analysis.
No diagnosis-group hypothesis tests or p-values were calculated.

## Input and methods

Input: artifacts/main/table_240_200_rarefied_14235.qza
Samples: 80
Sampling depth: 14235 counts per sample

Both metrics were calculated with qiime diversity alpha from the same
saved rarefied table. No additional rarefaction was performed.

Metrics:
- observed_features: number of ASVs with nonzero counts per sample.
- shannon: diversity reflecting richness and abundance evenness.

Scripts:
- scripts/39_main_alpha.sh
- scripts/40_check_export_main_alpha.py

## Verification

Both outputs contained exactly the 80 audited metadata sample IDs.
Sample IDs were unique.
All values were finite and nonnegative.
Observed-feature values were positive integers.

## Overall descriptive results

Quartiles below are the 25th, 50th and 75th percentiles.

| Metric | n | Minimum | Q1 | Median | Q3 | Maximum | Mean | SD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| observed_features | 80 | 73 | 149 | 180 | 227.25 | 361 | 191.5125 | 58.3716 |
| shannon | 80 | 4.2589 | 5.3344 | 5.6487 | 6.0368 | 6.7139 | 5.6502 | 0.5608 |

These summaries pool all 80 samples and are not diagnosis-group comparisons.

## Outputs

- artifacts/main/observed_features_14235.qza
- artifacts/main/shannon_14235.qza
- reports/main_alpha_14235/alpha_per_sample.tsv
- reports/main_alpha_14235/alpha_summary_overall.tsv

## Limitations

This addition was selected after other biological results had been viewed.
The summaries do not establish a cancer-versus-normal association.
Equal richness or Shannon values do not imply identical ASV composition.
Observed ASVs are not equivalent to bacterial species counts.
These values do not establish microbiome health or complete diversity recovery.
The original rarefaction limitations remain applicable.
