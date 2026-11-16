#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/19_distances_$(date +%Y%m%d_%H%M%S).log") 2>&1

date -Is
table="artifacts/main/table_240_200_rarefied_14235.qza"

for metric in braycurtis jaccard; do
    output="artifacts/main/${metric}_14235.qza"
    if [[ ! -e "$output" ]]; then
        stage=$(mktemp -d "$PWD/work/distance-main.XXXXXX")
        qiime diversity beta \
            --i-table "$table" \
            --p-metric "$metric" \
            --p-n-jobs 1 \
            --o-distance-matrix "$stage/distance.qza"
        mv "$stage/distance.qza" "$output"
    fi
    qiime tools export \
        --input-path "$output" \
        --output-path "reports/main_${metric}_14235"
done

date -Is
printf 'COMPLETE: Bray-Curtis and Jaccard matrices exported; no tests fitted.\n'
