#!/usr/bin/env bash
set -euo pipefail

mkdir -p work/tmp logs
export TMPDIR="$PWD/work/tmp"
output="artifacts/main/braycurtis_14235_pcoa.qza"

if [[ ! -e "$output" ]]; then
    stage=$(mktemp -d "$PWD/work/pcoa-main.XXXXXX")
    qiime diversity pcoa \
        --i-distance-matrix artifacts/main/braycurtis_14235.qza \
        --o-pcoa "$stage/pcoa.qza"
    mv "$stage/pcoa.qza" "$output"
fi

qiime tools export \
    --input-path "$output" \
    --output-path reports/main_braycurtis_pcoa

printf 'COMPLETE: Bray-Curtis PCoA; no association tests refitted.\n'
