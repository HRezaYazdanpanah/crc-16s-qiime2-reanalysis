#!/usr/bin/env bash
set -euo pipefail

mkdir -p work/tmp logs
export TMPDIR="$PWD/work/tmp"
output="artifacts/main/table_genus_level7_240_200.qza"

if [[ ! -e "$output" ]]; then
    stage=$(mktemp -d "$PWD/work/genus-level7.XXXXXX")
    qiime taxa collapse \
        --i-table artifacts/main/table_240_200.qza \
        --i-taxonomy artifacts/main/taxonomy_240_200.qza \
        --p-level 7 \
        --o-collapsed-table "$stage/genus.qza"
    mv "$stage/genus.qza" "$output"
fi

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_genus_level7_export

python - <<'PY'
import numpy as np
import pandas as pd
from biom import load_table

original = load_table("reports/main_table_export/feature-table.biom")
genus = load_table("reports/main_genus_level7_export/feature-table.biom")

def totals(table):
    return pd.Series(
        np.asarray(table.sum(axis="sample")).ravel(),
        index=list(table.ids(axis="sample"))
    )

before = totals(original)
after = totals(genus)
assert len(before) == 80
assert set(before.index) == set(after.index)
after = after.reindex(before.index)
assert np.array_equal(before.values, after.values)
assert int(after.sum()) == 3565583

pd.DataFrame({
    "ASV_counts": before.astype(int),
    "level7_counts": after.astype(int)
}).rename_axis("sample-id").to_csv(
    "reports/main_genus_level7_count_check.tsv", sep="\t"
)

labels = list(genus.ids(axis="observation"))
print("Samples:", len(after))
print("Collapsed level-7 taxonomy groups:", len(labels))
print("Total counts:", int(after.sum()))
print("Per-sample count conservation: PASS")
print("\nFirst 5 labels containing g__:")
examples = [
    label for label in labels
    if any(part.strip().startswith("g__") for part in label.split(";"))
]
for label in examples[:5]:
    print(label)
print("\nCOMPLETE: corrected aggregation; no filtering or DA fitted.")
PY
