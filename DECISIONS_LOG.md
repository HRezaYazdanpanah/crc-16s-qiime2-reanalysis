
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
I choose a depth of 15000 so that I can retain and examine
cd /home/reza/qiime2-course/CRC-QIIME2 && \
test -f DECISIONS_LOG.md && \
cat >> DECISIONS_LOG.md <<'EOF'

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
