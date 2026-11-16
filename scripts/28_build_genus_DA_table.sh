#!/usr/bin/env bash
set -euo pipefail

mkdir -p work/tmp logs
export TMPDIR="$PWD/work/tmp"
output="artifacts/main/table_genus_level7_DA.qza"

if [[ ! -e "$output" ]]; then
    stage=$(mktemp -d "$PWD/work/genus-DA.XXXXXX")
    qiime feature-table filter-features \
        --i-table artifacts/main/table_genus_level7_240_200.qza \
        --m-metadata-file reports/main_genus_audit/eligible_feature_ids.tsv \
        --o-filtered-table "$stage/table.qza"
    mv "$stage/table.qza" "$output"
fi

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_genus_DA_export

python - <<'PY'
import numpy as np
import pandas as pd
from biom import load_table

source = load_table("reports/main_genus_level7_export/feature-table.biom")
filtered = load_table("reports/main_genus_DA_export/feature-table.biom")
eligible = pd.read_csv(
    "reports/main_genus_audit/eligible_feature_ids.tsv",
    sep="\t"
)["feature-id"].tolist()

assert len(eligible) == 194
assert set(filtered.ids(axis="observation")) == set(eligible)
assert filtered.shape == (194, 80)
assert set(filtered.ids(axis="sample")) == set(source.ids(axis="sample"))

expected = source.filter(eligible, axis="observation", inplace=False)
expected = expected.sort_order(
    list(filtered.ids(axis="observation")), axis="observation"
)
expected = expected.sort_order(
    list(filtered.ids(axis="sample")), axis="sample"
)
assert (expected.matrix_data != filtered.matrix_data).nnz == 0

sizes = np.asarray(filtered.sum(axis="sample")).ravel()
assert np.all(sizes > 0)
print("DA table: 194 groups x 80 samples")
print("Feature IDs and retained counts: PASS")
print("Total retained counts:", int(sizes.sum()))
print("Minimum retained sample count:", int(sizes.min()))
print("COMPLETE: filtering only; no DA fitted.")
PY
