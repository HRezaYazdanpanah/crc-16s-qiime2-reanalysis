# Prespecified Literature-Guided Genus Hypotheses

Date approved: 2026-10-11
Status: Approved before diagnosis-stratified biological results

## Source
Wirbel et al., 2019, Nature Medicine.
DOI: 10.1038/s41591-019-0406-6
Supplementary Table S4, genus-level section.
Source file: 41591_2019_406_MOESM3_ESM.xlsx

## Selection rule
1. Use genus-level rows, not species-level rows.
2. Require p.adj.meta < 0.05.
3. Require positive generalized fold change in all five
   reported cohorts: FR, DE, CN, US and AT.
4. Sort by p.adj.meta ascending, then genus name for ties.
5. Select the first five eligible genera.

## Prespecified hypotheses

| Genus | Expected direction in CRC versus controls |
|---|---|
| Fusobacterium | Higher |
| Parvimonas | Higher |
| Peptostreptococcus | Higher |
| Porphyromonas | Higher |
| Solobacterium | Higher |

## Testing and reporting
These are secondary, literature-guided hypotheses.
Use two-sided tests and report agreement with expected direction.
Apply FDR correction within this prespecified family.
Other eligible genera form a separate exploratory FDR family.
The DA method and eligibility filter must be recorded before
genus-level association testing.

If a listed genus cannot be resolved or fails the eligibility
filter, report it as not evaluable.
Do not replace it after inspecting study results.

## Interpretation
This is an educational reanalysis of Baxter data.
These hypotheses are not mock-community controls.
They do not establish independent validation.
Some related associations were already reported in Baxter.

Generalized fold changes in the source are not ordinary
abundance ratios and are not expected to equal our DA estimates.

## Exact source rows
Worksheet: Supplementary Table S4.
Excel row numbers are 1-based.
Genus labels are in column AI, not in the species table.

| Genus | Expected direction in CRC | Excel row |
|---|---|---|
| Fusobacterium | Higher | 152 |
| Parvimonas | Higher | 118 |
| Peptostreptococcus | Higher | 25 |
| Porphyromonas | Higher | 144 |
| Solobacterium | Higher | 22 |

This file must be committed with a Git timestamp before any
diagnosis-stratified biological plot, summary or test is generated.
Record the commit hash in the project records.
Metadata eligibility and QC attrition audits are not biological
association outputs.
