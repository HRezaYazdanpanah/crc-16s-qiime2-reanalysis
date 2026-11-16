#!/usr/bin/env bash
set -euo pipefail

mkdir -p work/tmp logs reports/main_ancombc2
export TMPDIR="$PWD/work/tmp"
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

python - <<'PY'
import pandas as pd
from biom import load_table
from qiime2 import Metadata

m = pd.read_csv(
    "reports/main_metadata_audit/audited_metadata.tsv",
    sep="\t", dtype=str
).set_index("sample-id")

table = load_table("reports/main_genus_DA_export/feature-table.biom")
ids = list(table.ids(axis="sample"))
assert not m.index.duplicated().any()
assert set(ids) == set(m.index)

m = m.loc[ids, ["dx", "Age", "Gender", "BMI", "Site"]]
for col in ["Age", "BMI"]:
    m[col] = pd.to_numeric(m[col], errors="raise")
assert len(m) == 80 and not m.isna().any().any()
assert set(m.dx) == {"normal", "cancer"}

metadata = Metadata(m)
metadata.save("metadata/main_DA_metadata.tsv")
print(metadata.to_dataframe().dtypes)
print("DA metadata: 80 complete samples; PASS")
PY

output="artifacts/main/ancombc2_genus_194.qza"
if [[ -e "$output" ]]; then
    echo "STOP: output already exists; review before rerunning."
    exit 1
fi

date -Is
stage=$(mktemp -d "$PWD/work/ancombc2-main.XXXXXX")

qiime composition ancombc2 \
    --i-table artifacts/main/table_genus_level7_DA.qza \
    --m-metadata-file metadata/main_DA_metadata.tsv \
    --p-fixed-effects-formula 'dx + Age + Gender + BMI + Site' \
    --p-reference-levels dx::normal \
    --p-p-adjust-method none \
    --p-prevalence-cutoff 0.1 \
    --p-no-structural-zeros \
    --p-no-asymptotic-cutoff \
    --p-alpha 0.05 \
    --p-no-diff-robust \
    --p-num-processes 1 \
    --o-ancombc2-output "$stage/result.qza" \
    --verbose

mv "$stage/result.qza" "$output"

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_ancombc2/export

date -Is
find reports/main_ancombc2/export -maxdepth 2 -type f
printf 'COMPLETE: first ANCOM-BC2 fit; family-specific BH still pending.\n'
