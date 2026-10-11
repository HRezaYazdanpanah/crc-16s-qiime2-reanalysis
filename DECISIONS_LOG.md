
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
