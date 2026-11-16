# Scripts

Run from the repository root, in number order, inside the conda
environment described in `environment.yml`.
Long steps (download, trimming, DADA2, taxonomy) were started with `nohup`
and write a timestamped log. The shell scripts stop on the first error.

## Pilot (8 samples, technical checks only)

| Script | What it does |
|---|---|
| `01_select_pilot.py` | Picks 4 CRC and 4 control samples at random (seed 20261011) from single-run samples. |
| `02_get_ena_reports.py` | Fetches ENA file reports (FTP path, size, MD5) for the pilot runs. |
| `03_download_pilot.py` | Downloads the FASTQ files and checks size and MD5. |
| `04_build_pilot_inputs.py` | Builds the QIIME 2 manifest and metadata for the pilot. |

The pilot QIIME 2 steps were run by hand while I was learning them.
Their settings are in `DECISIONS_LOG.md` (D03 to D06) and in the pilot logs under `reports/`.

## Main subset (80 samples)

| Script | What it does |
|---|---|
| `05_select_main_fallback.py` | Selects 40 CRC and 40 controls at random (seed 20261111). Output frozen in `metadata/main_subset_80.tsv`. |
| `06_get_main_ena_reports.py` | Fetches ENA file reports for the 80 runs. |
| `07_download_main.py` | Downloads 160 FASTQ files; resumable. |
| `08_verify_main_inputs.py` | Checks every file against ENA size and MD5. |
| `09_build_main_inputs.py` | Builds the import manifest and sample metadata. |
| `10_import_main.sh` | Imports reads into QIIME 2 and makes the quality summary. |
| `11_audit_main_primers.py` | Looks for primers and read-through in the first 1,000 reads of each file. |
| `12_trim_main.sh` | Removes read-through with cutadapt (3' adapters only). |
| `13_dada2_main.sh` | DADA2 `denoise-paired`, truncation 240/200. |
| `14_review_main_dada2.py` | Per-sample read retention through DADA2; flags samples below 50%. |
| `15_taxonomy_main.sh` | Assigns taxonomy with the SILVA 144 V4 classifier. |
| `16_phylogeny_main.sh` | Alignment, masking and tree (MAFFT, FastTree). |
| `17_depth_review.py` | Library sizes and what each rarefaction depth would cost in samples. |
| `18_rarefy_main.sh` | Rarefies to 14,235 reads per sample (seed 20261112). |
| `19_main_distances.sh` | Bray-Curtis and Jaccard distance matrices. |
| `20_audit_main_metadata.R` | Checks covariates, complete cases and model rank before any test. |
| `21_primary_permanova.R` | Primary test: `adonis2`, marginal terms, 9,999 permutations within site. |
| `22_main_permdisp.R` | Group dispersion with `betadisper`, same permutations. |
| `23_jaccard_sensitivity.R` | The primary model again on Jaccard distances. |
| `24_genus_table_main.sh` | **Not used.** Collapsed at level 6, which is family in this taxonomy. Kept as a record of the mistake. |
| `25_genus_level7_main.sh` | Collapses to genus (level 7): 426 groups. |
| `26_audit_genus_prevalence.py` | Prevalence per group across all 80 samples; checks the five prespecified genera. |
| `27_finalize_genus_eligibility.py` | Applies the eligibility rules: 194 groups. |
| `28_build_genus_DA_table.sh` | Builds the 194 x 80 count table for differential abundance. |
| `29_ancombc2_main.sh` | Fits ANCOM-BC2. |
| `30_audit_ancombc2_output.py` | Checks the output for missing or invalid estimates. |
| `31_family_BH.R` | Benjamini-Hochberg correction within the two families (n = 5 and n = 190). |
| `32_plot_DA.py` | **Superseded by 36.** First version of the figure, made before the inference audit. |
| `33_inspect_ANCOMBC_inference.R` | Reads how the installed ANCOMBC computes p-values and degrees of freedom. |
| `34_audit_nonzero_support.py` | Finds groups with too few non-zero samples for the model (zero residual df). |
| `35_finalize_DA_inference_audit.R` | Marks the 6 non-evaluable groups; confirms the other BH values are unchanged. |
| `36_plot_DA_final.py` | Final differential-abundance figure. |
| `37_main_pcoa.sh` | Bray-Curtis PCoA. |
| `38_plot_main_pcoa.py` | PCoA figure, coloured by diagnosis and by site. |
| `39_main_alpha.sh` | Observed features and Shannon diversity on the rarefied table. |
| `40_check_export_main_alpha.py` | Checks and exports the alpha-diversity values. |
