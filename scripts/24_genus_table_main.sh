#!/usr/bin/env bash
set -euo pipefail

mkdir -p work/tmp reports logs
export TMPDIR="$PWD/work/tmp"

output="artifacts/main/table_genus_240_200.qza"

if [[ ! -e "$output" ]]; then
    stage=$(mktemp -d "$PWD/work/genus-main.XXXXXX")
    qiime taxa collapse \
        --i-table artifacts/main/table_240_200.qza \
        --i-taxonomy artifacts/main/taxonomy_240_200.qza \
        --p-level 6 \
        --o-collapsed-table "$stage/genus.qza"
    mv "$stage/genus.qza" "$output"
fi

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_genus_export

python - <<'PY'
import numpy as np
import pandas as pd
from biom import load_table

original = load_table("reports/main_table_export/feature-table.biom")
genus = load_table("reports/main_genus_export/feature-table.biom")

ids = list(original.ids(axis="sample"))
assert len(ids) == 80
assert set(ids) == set(genus.ids(axis="sample"))

before = np.array([original.sum(axis="sample")[original.index(s, axis="sample")]
                   for s in ids])
after = np.array([genus.sum(axis="sample")[genus.index(s, axis="sample")]
                  for s in ids])
assert np.array_equal(before, after), "Per-sample counts changed"
assert int(before.sum()) == 3565583

pd.DataFrame({
    "sample-id": ids,
    "ASV_counts": before.astype(int),
    "genus_counts": after.astype(int)
}).to_csv("reports/main_genus_count_check.tsv", sep="\t", index=False)

print("Samples:", len(ids))
print("Original ASVs:", original.shape[0])
print("Collapsed taxonomy groups:", genus.shape[0])
print("Total counts:", int(after.sum()))
print("Per-sample count conservation: PASS")
print("\nFirst 5 collapsed labels:")
for label in list(genus.ids(axis="observation"))[:5]:
    print(label)
print("\nCOMPLETE: aggregation only; no filter or DA fitted.")
PY
