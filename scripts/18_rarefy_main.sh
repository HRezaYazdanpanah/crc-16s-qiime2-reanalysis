#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp reports/main_rarefied_export
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/18_rarefy_$(date +%Y%m%d_%H%M%S).log") 2>&1

date -Is
output="artifacts/main/table_240_200_rarefied_14235.qza"

if [[ ! -e "$output" ]]; then
    stage=$(mktemp -d "$PWD/work/rarefy-main.XXXXXX")
    qiime feature-table rarefy \
        --i-table artifacts/main/table_240_200.qza \
        --p-sampling-depth 14235 \
        --p-no-with-replacement \
        --p-random-seed 20261112 \
        --o-rarefied-table "$stage/table.qza"
    mv "$stage/table.qza" "$output"
fi

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_rarefied_export

date -Is
printf 'COMPLETE: rarefaction and export; verification follows separately.\n'
