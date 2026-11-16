# Decisions log

Every analysis decision in this project, in the order it was made.
Entries give my choice, my reasoning and how to check it.
Entries from 2026-11-11 onward also state whether results had been seen.

## D01 — Control group
Date approved: 2026-10-11
Status: Approved

Decision:
The primary comparison is dx = cancer versus dx = normal.
Both Normal and High Risk Normal are included in the control group.

Options:
A. Include both control subgroups.
B. Include only Dx_Bin = Normal.

My choice and justification:
I chose A because it retains a larger sample size and follows the
study's classification of controls as having no colonic lesions.
This does not mean that controls are healthy in every respect.
Absence of colonic lesions is based on the study's assessment.

How to check:
Verify group labels against the original study.
Clarify the definition of High Risk Normal.
Report eligible sample counts before and after QC.

## D02 — Pilot samples and multiple runs
Date approved: 2026-10-11
Status: Approved for pilot only

Decision:
Use samples with a single sequencing run for the pilot.
Do not automatically exclude or merge multiple-run samples
in the main analysis.
Sequencing runs from the same biological sample are not
independent biological replicates.

Options:
A. Start the pilot with single-run samples.
B. Resolve all multiple-run samples before starting the pilot.

My approved rationale:
Start by checking the executable workflow with single-run samples.
Keep the main-analysis rule for multiple-run samples unresolved
until the relevant experimental information has been reviewed.

How to check:
Confirm one Run accession per selected pilot sample.
Review BioSample, Experiment and library information for
multiple-run samples before choosing their processing rule.
Do not report pilot findings as the main study results.

### D03 — 2026-10-21 — pilot only
- Evidence: all 8 pilot samples audited; no anchored expected-primer matches; paired read-through evidence detected.
- Decision: no fixed 5-prime trimming; trim opposite-primer reverse complements at 3-prime ends.
- Parameters: error-rate=0.1; overlap=12; minimum-length=1; pair-filter=any; retain untrimmed pairs; no quality trimming.
- Review per-sample trimming/loss statistics before denoising. Main-cohort handling remains unresolved.

### D04 — 2026-10-21 — pilot only
- Use DADA2 denoise-paired: data-driven error learning, paired-end denoising/merging, and stage-wise retention statistics.
### D05 — 2026-10-21 — initial pilot settings
- trunc-len-f=240; trunc-len-r=200; trim-left-f=0; trim-left-r=0; max-ee-f=2; max-ee-r=2; min-overlap=12; pooling-method=independent; chimera-method=consensus.
- Initial settings based on post-Cutadapt quality plots; not established as optimal. Inspect filtering and merging losses before accepting.
### D06 — 2026-10-21 — pilot review rule
- Flag any sample with non-chimeric pairs / DADA2 input pairs < 0.50 for technical review; no automatic sample exclusion. Input denominator is post-Cutadapt pairs.
- Inspect losses at each stage without diagnosis grouping; report Cutadapt loss separately. Main-cohort settings remain unresolved.

### Pilot review — D04–D06 — 2026-10-21
- Retain 240/200 settings for continued pilot processing; no sample exclusion under D06.
- Non-chimeric pairs: 286481 / 342927 post-Cutadapt input pairs (83.54%); per-sample retention 77.97–87.54%.
- Largest aggregate loss occurred during filtering. Settings are acceptable for this pilot, not established as optimal or approved for the main cohort.

## M5 — 2026-10-31 — Pilot alpha rarefaction and sampling depth

Scope:
Technical pilot only, comprising 8 samples.
No diagnosis-stratified grouping, colouring, filtering or testing.
This decision does not establish a sampling depth for the main cohort.

Inputs:
- Feature table: artifacts/pilot/table_240_200.qza
- Rooted tree: artifacts/pilot/rooted_tree_240_200.qza

Exploratory rarefaction:
- Maximum depth: 65000
- Steps: 10
- Iterations per depth: 10
- Metrics: observed_features, shannon, faith_pd
- Visualization: artifacts/pilot/alpha_rarefaction_240_200_max65000.qzv

My justification for the exploratory maximum:
I chose 65000 to inspect approximately the full range of sample counts.
This maximum is not the final sampling depth.

Evidence reviewed:
- Minimum sample frequency: 15233.
- All 8 samples had results at the tested depth of 14445.
- Only 6 samples had results at the tested depth of 21667.
- Missing results at higher depths were blank in the exported CSV files.
- Apparent drops to zero in the visualization were not interpreted as
  biological losses of diversity.
- Complete saturation of all metrics in all samples was not established.

Final pilot sampling-depth choice:
15000 counts per sample, using rarefaction without replacement.

Alternatives considered:
- 14445: directly evaluated in the exploratory curves; retains all 8 samples.
- 15000: selected; below the minimum sample frequency.
- 20000: would exclude at least the lowest-depth sample.

My justification:
I choose a depth of 15000 so that I can retain and examine all 8 pilot
samples. I accept that counts above this depth in higher-count samples
will not be used in the rarefied table.

Trade-offs and limitations:
- Some low-abundance ASVs may not be observed after subsampling.
- Rarefaction is stochastic.
- The original feature table will remain unchanged.
- A depth of exactly 15000 was not tested in the initial rarefaction grid.
- This choice prioritises sample retention, not proven complete saturation.

How to check:
- Confirm that the rarefied table contains all 8 original sample IDs.
- Confirm that every retained sample has exactly 15000 counts.
- Calculate the selected alpha-diversity metrics on the rarefied table.
- Interpret the results as technical pilot observations only.

Status:
Decision selected before final rarefaction.
Execution and output checks are pending.

## M7 — Pilot genus prevalence threshold

Scope: Technical pilot only; no diagnosis-based testing.

Decision: Use a prevalence cutoff of 0.2.

Options considered: 0.1, 0.2, 0.25.

My choice: 0.2.

My justification: Remove genera detected in only one of the eight
pilot samples and retain genera detected in at least two samples.

How to check: Compare the number of features and total counts
before and after filtering.

Note: With eight samples, cutoffs of 0.2 and 0.25 retain the same
features. This threshold is not automatically adopted for the main cohort.

## Amendment — 2026-11-11 — Activate resource-limited fallback

Biological results viewed: no.
Technical pilot QC has been inspected; diagnosis-stratified biological
results have not been inspected.

Trigger and review:
Activate fallback immediately on 2026-11-11, before main-cohort
download and denoising. Do not attempt the full cohort first.
The library closes in approximately three hours today, and a
40-hour/week job starts on 2026-11-16. The original 2026-11-08
deadline has passed; it is not retrospectively changed.

Population:
Preserve the PLAN.md primary contrast: cancer versus normal.
Controls include Normal and High Risk Normal.
Select 40 Cancer and 40 controls from eligible single-run BioSamples.

Eligibility and selection:
Use metadata only. Count runs per BioSample across the full SRA table.
Require unambiguous Sample Name–BioSample mapping, matching original
metadata diagnosis, and paired-end layout.
Do not filter on covariate completeness, read counts or biological results.
Use Python random.Random(20261111), sampling without replacement
within diagnosis groups from deterministically sorted eligibility lists.
Selection implementation: scripts/05_select_main_fallback.py.
Frozen sample-to-run list: metadata/main_subset_80.tsv.
Commit both before any main-subset download.

Pilot policy:
Pilot samples remain eligible but are not forced into the selection.
Do not add pilot output tables to main outputs.
Process selected pilot samples as part of the main workflow.

Multi-run policy:
Exclude multi-run BioSamples from this fallback eligibility pool.
This does not resolve multi-run processing for a future full-cohort run.
Single-run status does not establish a shared physical sequencing batch.
Distinct-participant correspondence remains unverified.

Analyst justification:
The goal is an educational, reproducible reanalysis that can be
completed and defended before the new job starts. Equal allocation
provides a balanced comparison, but is not claimed to be universally
superior to proportional sampling.

Limitations:
Reduced power, non-proportional sampling, possible selection effects
from the single-run restriction, and unresolved participant mapping.
No causal or independent-validation claim.

Unchanged:
Primary model, covariates, complete-case rules, permutation scheme,
confirmatory genera and separate FDR families remain binding.
Main trimming/truncation, sampling depth and final DA specifications
are not approved by this scope amendment.

## M8 — 2026-11-11 — Main-subset truncation choice

Scope: Frozen 80-sample main subset.
Biological results viewed: no.

My choice:
DADA2 trunc_len_f=240; trunc_len_r=200.

My justification:
The main-subset raw quality plot shows declining reverse-read
quality after approximately position 200.
Analyst-reported hover values:
- Reverse position 237: Q25=14, median Q=26.
- Reverse position 180: Q25=35, median Q=38.
These exact hover values have not yet been archived as a TSV.
Pilot technical results support feasibility, not optimality.

Overlap:
Sufficient overlap is expected but not yet confirmed for main.
With trim_left_f=0 and trim_left_r=0, retained lengths total 440 nt.
A target length no greater than 428 nt is necessary for 12 nt overlap.
Primer handling and post-trim lengths still require review.

Planned checks:
Inspect post-trim lengths/quality and main DADA2 retention by stage.
Report filtering, merging and non-chimeric retention per sample.
Do not interpret this choice as proven optimal.

Deferred technical experiment:
After completing the core project, compare 240/200 versus 240/237
on the same five samples, selected and recorded before that experiment.
Keep all other settings identical.
Report filtered/input, merged/denoised, and non-chimeric/input.
Treat this as exploratory technical work; do not silently replace
the frozen main analysis based on later biological findings.

Status:
Truncation choice recorded before main denoising.
Primer handling, physical sequencing-run/error-learning strategy,
and remaining DADA2 settings are not approved by this entry.

## M8 — 2026-11-11 — Main read-through trimming

Biological results viewed: no.
Decision: retain the pilot read-through trimming strategy.
No fixed 5-prime trimming; no quality trimming.
Forward 3-prime adapter: ATTAGAWACCCBDGTAGTCC
Reverse 3-prime adapter: TTACCGCGGCKGCTGGCAC
error_rate=0.1; overlap=12; minimum_length=1; pair_filter=any.
Retain pairs without adapter matches.
Allow adapter IUPAC wildcards and indels, as in the pilot.

Analyst justification:
The first 1000 reads per file were audited across all 160 FASTQs
(80 samples, two mates). No exact expected-primer matches were found
at the start or anywhere in these reads.
Full opposite-primer reverse complements occurred in 43/80000
forward reads and 37/80000 reverse reads.
This supports no fixed 5-prime trimming and targeted removal of
read-through while maintaining consistency with the technical pilot.

Limitations and checks:
The audit was not exhaustive or randomly sampled.
Absence of matches does not prove absence from all reads.
Cutadapt may trim more reads because it permits partial matches
and errors; negligible loss is an expectation, not an observed result.
Inspect per-sample trimming and pair-loss statistics, post-trim lengths
and quality. Example matching headers alone do not verify all pairing.
DADA2 launch remains pending these checks and the run/batch review.

## Amendment — 2026-11-12 — Main DADA2 error-learning strategy

Biological results viewed: no.
User approved proceeding on 2026-11-12 before main denoising.

Decision:
Process the frozen 80-sample subset in one denoise-paired invocation.
Learn shared forward and reverse error models across this subset.
Physical-run mapping was not recovered from the inspected metadata
and original workflow. Do not assume all samples share one run.

Rationale and limitation:
Proceed as a time-limited educational reanalysis.
This departs from recommended separate error learning by physical run.
Independent sample inference does not remove this limitation.
Report unresolved sequencing-batch effects; Site is not batch.

Execution settings:
trunc_len_f=240; trunc_len_r=200; trim_left_f=0; trim_left_r=0.
max_ee_f=2; max_ee_r=2; trunc_q=2; min_overlap=12.
max_merge_mismatch=0; trim_overhang=false.
pooling_method=independent; chimera_method=consensus.
min_fold_parent_over_abundance=1; allow_one_off=false.
n_reads_learn=1000000; n_threads=2.
hashed_feature_ids=true; retain_all_samples=true; retain_unmerged=false.

QC rule:
Review every sample's stage-wise retention without diagnosis grouping.
Flag non-chimeric/input <0.50 for technical review, not automatic exclusion.
Report Cutadapt losses separately.
No primary biological analysis until QC has been reviewed.

## M8 — 2026-11-12 — Main sampling depth

Biological results viewed: no.
Decision: rarefy the ASV table to 14235 counts per sample.
Selection used pooled library sizes only, without dx stratification.

My justification:
I choose 14235 because it is the highest depth that retains all
80 samples. Preserving the full subset takes priority over increasing
depth at the cost of sample exclusions.

Evidence:
Minimum count=14235; total original counts=3565583.
Expected retained samples=80; expected rarefied total=1138800.
Alternatives: 15000 retains 78; 20000 retains 73 samples.

Implementation:
Sampling without replacement; rarefaction seed=20261112.
Generate one frozen rarefied table for diversity analyses.
Keep the unrarefied table unchanged for differential abundance.

Limitations:
This choice does not establish saturation or complete taxon recovery.
Rare features may be lost during subsampling.
Covariate complete-case selection may later exclude samples.

Checks:
Verify all 80 selected IDs and exactly 14235 counts per sample.

## M8 — 2026-11-12 — PERMDISP implementation

Biological results viewed: yes; primary PERMANOVA has been viewed.
The planned PERMDISP has not yet been run.

Implementation:
vegan::betadisper on the original Bray-Curtis matrix.
Group=dx; spatial median; bias.adjust=FALSE (package default).
No square-root transformation or additive correction.
Use the saved 9999 within-Site permutations in the same sample order.
No pairwise tests; record warnings and negative eigenvalues.
Implementation uses package defaults, not selection among observed results.

Limitation:
This is a group-dispersion assessment, not a covariate-adjusted
dispersion model. Blocking permutations within Site does not adjust
dispersion for Age, Gender or BMI.
Interpret alongside PERMANOVA, not as an automatic gate.

## M8 — 2026-11-12 — Secondary genus-level DA specification

Status:
Approved by the analyst before the first differential-abundance fit.
Community-analysis results have been viewed:
Bray-Curtis PERMANOVA, PERMDISP and Jaccard sensitivity.
Genus-level differential-abundance results have not been viewed.
These DA settings were finalized now, not preregistered on 2026-10-11.

Method and input:
ANCOM-BC2 on genus-level counts aggregated from:
artifacts/main/table_240_200.qza
Taxonomy:
artifacts/main/taxonomy_240_200.qza
Do not use rarefied counts or relative abundances as model input.

Population and model:
Cancer versus normal; retain the frozen eligible 80-sample subset.
Fixed-effects formula: dx + Age + Gender + BMI + Site
No interactions.
Reference level: dx=normal
Target contrast: cancer versus normal.
Use complete cases for these covariates; no BMI imputation.
The completed metadata audit found 80 complete cases.

Eligibility:
Calculate genus prevalence across the pooled eligible DA sample set.
Presence means count > 0.
Retain genera present in at least 10% of eligible samples.
For the current 80-sample set, this means at least 8 samples.
Do not use diagnosis-specific prevalence thresholds.
Structural-zero detection: disabled.
Record any additional software defaults or filters before fitting.

Testing and multiplicity:
Use two-sided coefficient tests for the target dx contrast.
Family 1:
Fusobacterium, Parvimonas, Peptostreptococcus,
Porphyromonas and Solobacterium.
Family 2:
All other eligible genera.
Apply Benjamini-Hochberg correction separately within each family.
Threshold: adjusted p-value < 0.05.
Do not claim combined FDR control across both families.
Report unresolved, filtered or otherwise non-evaluable
prespecified genera explicitly; do not replace them.
Report effect estimates, uncertainty and expected-direction agreement.
Report relative abundances separately from model-based effects.

Analyst-approved rationale:
Keep covariates based on scientific design, not beta-diversity
p-values. Retaining BMI avoids result-driven covariate selection.
The 10% pooled prevalence threshold removes very sparse genera
without requiring presence in both diagnosis groups.
This threshold is a project choice, not a universal standard.

Checks before fitting:
Verify sample IDs, count totals, genus aggregation and label matching.
List prevalence and eligibility for all five prespecified genera.
Verify the installed ANCOM-BC2 interface and remaining settings.
Record defaults, convergence checks and FDR implementation.
Secondary DA reporting is not conditional on primary significance.

## M8 — 2026-11-12 — Correction of taxonomy aggregation depth

The initial level=6 aggregation reached family, not genus.
Inspection of the original taxonomy confirmed:
d__;k__;p__;c__;o__;f__;g__
Therefore genus aggregation must use level=7.

The earlier table_genus_240_200.qza is family-level despite its name.
Retain it as an obsolete intermediate; do not use it for DA.
No differential-abundance model has been fitted.

Corrected genus artifact:
artifacts/main/table_genus_level7_240_200.qza
Check per-sample count conservation before eligibility filtering.
Unresolved taxonomy groups require separate eligibility review.

## M8 — 2026-11-12 — Genus annotation eligibility

Approved after pooled taxonomy/prevalence inspection.
Community-analysis results viewed: yes.
Differential-abundance results viewed: no.

Rules:
Use full taxonomy paths as feature identifiers.
Do not merge distinct paths based only on matching genus labels.
Preserve --other suffixes.
Exclude rows without a nonempty genus label.
Exclude genus label Incertae_Sedis.
Retain other database-defined genus-level groups, including
--other, Candidatus and provisional group labels.
Interpret these as genus-annotation-level taxonomic groups,
not uniformly as definitively identified named genera.
Apply pooled presence in at least 8 of 80 samples.

Analyst justification:
A genus label alone does not establish identical taxonomic identity
across different paths. Preserve taxonomy information; do not create
invented genus names for unresolved groups.

Prespecified hypothesis audit:
Solobacterium is present in 7/80 samples and fails prevalence.
Report it as not evaluable; do not lower the threshold or replace it.

## M8 — 2026-11-12 — ANCOM-BC2 execution settings

Recorded before the first DA fit.
Input: 194 eligible taxonomy groups and 80 complete samples.
Retained counts after feature filtering: 3179890.
Minimum retained sample count: 12644.

Use dedicated metadata with numeric Age/BMI and categorical dx/Gender/Site.
Fixed effects: dx + Age + Gender + BMI + Site
Reference: dx=normal; no random effects.
Internal p-adjust method: none.
Final inference requires separate BH adjustment by the recorded families.
Do not interpret unadjusted output flags as final FDR decisions.

Prevalence cutoff=0.1; structural zeros=false;
asymptotic cutoff=false; alpha=0.05; diff_robust=false.
No claim of passing pseudo-count sensitivity analysis.
One process; other unexposed settings remain package defaults.
No seed parameter is exposed in the installed CLI.
Retain verbose logs and artifact provenance.
Review warnings, available convergence information and missing estimates
before reporting results. Do not silently refit with changed settings.

## M8 — 2026-11-12 — Family-specific BH implementation

Approved after numerical-output audit, before displaying individual
genus-level p-values or applying family-specific BH.

Keep confirmatory family size n=5.
Keep exploratory family size n=190.
Apply stats::p.adjust(method="BH") to valid target-contrast p-values
within each family, with the corresponding fixed n.

Solobacterium failed the prespecified prevalence filter.
S5-A14a has missing LFC and SE and is not evaluable.
Do not report either as evidence of no association.
Leave their reported inferential values unavailable.
Do not substitute an observed p-value for a failed estimate.

Use finite LFC, finite positive SE and finite p in [0,1]
as numerical validity requirements, not proof of convergence.
Report passed_ss separately; do not label it as an FDR result.
No combined FDR-control claim across the two families.

## M8 — 2026-11-12 — Post-fit inference-support audit

Recorded after viewing DA results; this is a diagnostic reporting
amendment, not a change to the model or prevalence threshold.

Backend verified: R ANCOMBC 2.12.0 via q2-composition 2026.7.0.
Installed source calculates t-test p-values using fitted residual df,
then replaces missing p-values with 1.

Nonzero-support diagnostic:
188 exported p-values reproduced using W and positive residual df.
Five groups have zero nonzero-support residual df and exported p=1:
Paludihabitans, Phocea, Thermanaerosceptrum, Eubacterium, Leuconostoc.
These are reported as not evaluable for inference, not null findings.
S5-A14a is separately not evaluable because LFC and SE are missing.

Final inference-evaluable groups: 188 (4 confirmatory, 184 exploratory).
Retain BH family sizes 5 and 190.
Adjusted p-values for all evaluable groups were verified unchanged.
Parvimonas and Hallella remain BH findings; both have passed_ss=False.

Preserve original exports, intermediate tables and original figure.
Create a revised figure from dx_cancer_final_audited.tsv.
Do not refit the model or change eligibility to recover findings.

## M8 — 2026-11-16 — Descriptive main alpha diversity

Timing:
Added after viewing main PERMANOVA, PERMDISP, Jaccard,
ANCOM-BC2 and PCoA results. Not a prespecified confirmatory analysis.

Options:
1. Retain the completed pilot alpha-diversity work only.
2. Add descriptive observed_features and Shannon for the main subset.

My choice:
Option 2.

My justification:
We have not calculated observed_features and Shannon for our 80 samples.

Scope:
Use artifacts/main/table_240_200_rarefied_14235.qza unchanged.
Calculate observed_features and shannon only.
No new rarefaction, group hypothesis tests, p-values or model fitting.
Do not change the frozen primary or differential-abundance analyses.

Checks:
Verify exactly the 80 main sample IDs and finite values for both metrics.
Export per-sample values and descriptive summaries.
Label the addition transparently in the report and README.

Status:
Approved before calculation; execution and verification pending.

### Main alpha execution verified — 2026-11-16

Completed the approved descriptive observed_features and shannon calculations.
Both outputs matched exactly the 80 audited sample IDs.
All values were finite and nonnegative; observed_features were positive integers.
Per-sample values and overall descriptive summaries were exported.
No new rarefaction, group hypothesis tests or model fitting were performed.
Report: reports/M8_main_alpha_diversity_summary.md
Status: Calculation, verification and descriptive reporting completed.

## Corrections and late records — 2026-11-16

Recorded during the pre-publication review.
No analysis was rerun or changed.

1. Duplicate M5 entry removed.
The pilot M5 entry of 2026-10-31 had been pasted twice. The first copy
was cut off mid-sentence and followed by stray shell text. That truncated
copy was deleted; the complete entry is unchanged.

2. The pilot "genus" table was family-level.
In the pilot DA practice (M7), `taxa collapse --p-level 6` was treated
as genus-level. With this SILVA 144 classifier the ranks are
d__;k__;p__;c__;o__;f__;g__, so level 6 is family.
The pilot tables artifacts/pilot/genus_table_240_200*.qza and the counts
in the pilot M7 report (69 to 53 features after the prevalence filter)
therefore describe family-level groups.
The pilot was technical only and no pilot result is reported as a finding.
The main analysis uses level 7 (see the correction of 2026-11-12).

3. Classifier choice (D07) logged late.
D07 was decided on 2026-10-26 (M4) and written up in
reports/M4_taxonomy_summary.md, but never copied into this log.
Choice: SILVA 144 SSURef NR99, V4 515f-806r, uniform weights,
built for QIIME 2 2026.7.
File: SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza
UUID: 76237f8f-87e0-4d1e-93b9-970bb7603cf0
Alternative considered: a full-length classifier.
My justification, as written on 2026-10-26:
"We select the V4 region model so that it matches the data's V4 region,
and choose the uniform model to avoid habitat-specific weighting,
without claiming that all biases are eliminated."
The same classifier (same UUID) was used for the pilot and the main subset.
