# CRC Stool Microbiome Reanalysis Plan

Date: 2026-10-11
Status: Baseline before biological results
Deadline: 2026-11-08

## 1. Aim and scope
Build a documented, reproducible educational reanalysis of
one public stool 16S cohort using QIIME 2 and R.

Core: one completed cohort.
Stretch: direction consistency in an independent cohort.
No machine-learning classifier.
No causal or independent-validation claim.

## 2. Dataset, contrast and unit
Study: Baxter et al., 2016
SRA study: SRP062005
Region: V4
Read layout: paired-end

Compare dx = cancer versus dx = normal.
Include Normal and High Risk Normal controls.
Exclude adenoma from the primary contrast.
Controls had no colonic lesions according to the study;
do not describe them as healthy in every respect.
Clarify the exact High Risk Normal definition.

The biological sample is the analysis unit.
Verify correspondence to distinct individuals.
Multiple sequencing runs do not increase biological replication.

## 3. Primary question
Is CRC status associated with overall stool microbial community
structure after adjustment for prespecified covariates?

## 4. Primary community analysis
Resolution: ASV level.
Distance: Bray-Curtis on a rarefied feature table.
Rationale: abundance-sensitive and non-phylogenetic.

Model:
distance ~ dx + Age + Gender + BMI + Site

No interactions.
Use complete cases, without BMI imputation.
Check model estimability and report exclusions.

Export the QIIME 2 distance matrix.
Use vegan::adonis2 in R with by = "margin".
Primary test: marginal dx association.
Alpha: 0.05.
Requested permutations: 9999.
Permutation seed: 20261011.
Restrict permutations within Site.
Record the permutation implementation and effective number.

Report pseudo-F, p-value and marginal R-squared for dx.
Show marginal R-squared for Age, Gender, BMI and Site
from the same model for context.
Marginal R-squared terms are not an additive variance partition.
Do not interpret the Site p-value as a between-Site test
under within-Site permutations.

Assess CRC-versus-control dispersion with PERMDISP.
Document its implementation and permutation scheme.
Interpret it alongside PERMANOVA, not as an automatic gate.

Sensitivity distance: Jaccard on the same retained samples
and rarefied table, using the same model and restrictions.
This is not a second primary test.

Commit these specifications before diagnosis-stratified
biological outputs. Choose depth using QC before inspecting
group separation.

## 5. Secondary genus-level analysis
confirmatory_genera.md contains five literature-guided genera,
expected directions, selection rule and exact source rows.
Commit it with a Git timestamp before any diagnosis-stratified
biological plot, summary or test. Record its commit hash.

Family 1: the five prespecified genera.
Family 2: other genera passing the prespecified filter.
Use two-sided tests and FDR < 0.05 within each family.
Do not claim combined FDR control across both families.
Report agreement with the expected directions.

Calculate prevalence across the pooled eligible DA sample set.
Do not use group-specific prevalence filters or dx labels
to determine eligibility.
Record the numerical threshold before DA testing.

Name and justify the compositionality-aware DA method before
analysis. Record its model and missing-data rules.
Report method-specific effects, uncertainty and adjusted p-values.
Describe relative abundances separately.
Do not gate secondary reporting on primary significance.
Do not replace non-evaluable prespecified genera.

## 6. Covariates and technical factors
Primary covariates: Age, Gender, BMI and Site.
Do not equate Site with sequencing batch.
Investigate technical run/batch information separately.
Do not invent metadata.
Do not include FIT or haemoglobin in the primary model.
Document model amendments before fitting.

## 7. Pilot and multiple runs
Pilot uses single-run samples.
Proposed size: 8 samples, 4 CRC and 4 controls.
Confirm size, selection seed and sample IDs before download.
Select randomly within diagnosis groups.

Inspect technical and QC outputs only.
No diagnosis-stratified biological plots or tests in the pilot.
Pilot findings are not main-study findings.
Metadata eligibility and QC attrition audits by dx are permitted.

Do not automatically exclude or merge multiple-run samples.
Resolve and record their handling before main-cohort denoising.

## 8. Decisions by module
M2:
Eligibility, run mapping, pilot selection, main-cohort size,
multiple-run processing plan and resource-based fallback rule.

M3:
Primer handling, denoiser, trimming/truncation and minimum
post-QC read criteria.

M4:
Database, classifier and genus aggregation.

M5:
Rarefaction depth and diversity sample-retention rules.

M6:
Implement prespecified community model, marginal tests,
permutations and PERMDISP.

M7:
DA method, prevalence threshold and final DA model rules.

All stages:
Record software versions, relevant seeds, commands and
dated decisions before the affected analyses.

## 9. Time and scope guard
By the end of M2, before main-cohort denoising, the project
analyst must record:
- processing review date;
- fallback size and selection rule;
- fallback seed or fixed random selection order.

These are mandatory M2 deliverables.
Pilot QC may inform resource estimates.
Do not start main-cohort denoising until they are recorded.
Record fallback sample IDs before processing them.
Do not choose a fallback to obtain preferred biological results.

If the recorded resource/deadline trigger is reached,
activate fallback and record a dated amendment.

The plan-v1 tag records this baseline requirement.
Commit numerical scope decisions before denoising.
Complete core outputs before stretch work.

## 10. Attrition and BMI sensitivity
After rarefaction, report retained and excluded counts by:
- dx;
- Site;
- dx crossed with Site.

Repeat these counts after complete-case selection.
Report exclusion reasons and BMI missingness.

Assess unavailable or invalid BMI in the post-rarefaction
sample set before complete-case selection.
If this exceeds 5% overall OR 5% in either dx group,
additionally fit:

distance ~ dx + Age + Gender + Site

Use complete cases for these remaining covariates.
Retain the primary distance, marginal tests, alpha and
within-Site permutation scheme.
Report sample sets and attrition for both models.
Do not attribute result changes solely to removing BMI
when sample sets also change.

Keep the BMI-adjusted model primary if estimable.
If not estimable, document an amendment before fitting
a replacement primary model.

The 5% threshold is a project rule, not a universal standard.

## 11. Definition of Done
Required:
- PLAN.md and confirmatory_genera.md;
- DECISIONS_LOG.md and dated amendments;
- final metadata and sample-to-run mapping;
- executable numbered scripts;
- environment and version records;
- QC, denoising statistics, feature table and taxonomy;
- primary community analysis;
- secondary genus analysis or documented scope amendment;
- exported result tables and relevant figures;
- README with actual counts, methods and limitations.

No cross-cohort replication claim without completing it.

## 12. Reporting and amendments
Report sample and read losses.
Distinguish QC from biological-result decisions.
A null result is not proof of no association.

Record amendment date, reason and whether biological results
had been viewed. plan-v1 identifies the baseline but does not
prohibit documented amendments.

## 13. Sources
Baxter et al., 2016:
DOI: 10.1186/s13073-016-0290-3

Wirbel et al., 2019:
DOI: 10.1038/s41591-019-0406-6
Supplementary Table S4, genus-level section.

QIIME 2 amplicon documentation, release 2026.7.
vegan adonis2 documentation.
Record actual installed versions at execution.
