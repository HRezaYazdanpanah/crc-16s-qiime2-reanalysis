# Metadata

## Files in this folder

| File | What it is |
|---|---|
| `main_subset_80.tsv` | The 80 selected samples (sample ID, BioSample, run accession, diagnosis, site, age, gender, BMI). Frozen before download. |
| `main_fastq_report.tsv` | ENA file report for the 80 runs: FTP paths, sizes, MD5 sums. |
| `ena_main_reports/` | The per-run ENA reports that table was built from. |
| `main_manifest.tsv` | QIIME 2 import manifest. It holds absolute paths from my laptop; script 09 rebuilds it. |
| `main_metadata.tsv` | Sample metadata in QIIME 2 format. |
| `main_DA_metadata.tsv` | Same samples, typed for ANCOM-BC2 (numeric age and BMI). |
| `pilot_*.tsv` | The same kinds of files for the 8-sample technical pilot. |

## Source tables (not stored here)

The scripts expect two public tables in `metadata/original/`.
I did not copy them into this repository; they belong to the original authors.

1. `SraRunTable.csv`
   Run table for SRA study SRP062005, downloaded from the NCBI SRA Run Selector.

2. `metadata.tsv`
   Clinical metadata from the original study's repository:
   https://github.com/SchlossLab/Baxter_glne007Modeling_GenomeMed_2015/blob/master/data/metadata.tsv

The original authors' analysis workflow (mothur) is described here:
https://github.com/SchlossLab/Baxter_glne007Modeling_GenomeMed_2015/blob/master/analysis_workflow.md

## Notes

- Diagnosis labels: `cancer` = Cancer; `normal` = Normal or High Risk Normal. Adenoma samples are not used.
- The SRA run table lists the instrument as "454 GS". The paper and the `seq_methods` column both say Illumina MiSeq, and the reads are MiSeq paired-end reads.
- Only BioSamples with exactly one sequencing run were eligible for selection.
