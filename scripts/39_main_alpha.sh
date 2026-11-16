#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/qiime2-course/CRC-QIIME2"
mkdir -p work/tmp artifacts/main
export TMPDIR="$PWD/work/tmp"

table="artifacts/main/table_240_200_rarefied_14235.qza"

for metric in observed_features shannon; do
    output="artifacts/main/${metric}_14235.qza"

    if [[ -e "$output" ]]; then
        printf 'Already exists; skipping: %s\n' "$output"
        continue
    fi

    qiime diversity alpha \
        --i-table "$table" \
        --p-metric "$metric" \
        --o-alpha-diversity "$output"
done

printf 'COMPLETE: descriptive alpha metrics; no new rarefaction or tests.\n'
