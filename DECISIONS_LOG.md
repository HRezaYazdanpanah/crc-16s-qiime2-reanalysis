
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
