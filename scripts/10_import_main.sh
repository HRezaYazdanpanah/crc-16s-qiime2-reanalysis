#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export TMPDIR="$PWD/work/tmp"
mkdir -p "$TMPDIR" artifacts/main logs
exec > >(tee -a "logs/10_import_$(date +%Y%m%d_%H%M%S).log") 2>&1

date -Is

if [[ ! -e artifacts/main/demux.qza ]]; then
    qiime tools import \
        --type 'SampleData[PairedEndSequencesWithQuality]' \
        --input-path metadata/main_manifest.tsv \
        --input-format PairedEndFastqManifestPhred33V2 \
        --output-path artifacts/main/demux.qza
fi

if [[ ! -e artifacts/main/demux_summary.qzv ]]; then
    qiime demux summarize \
        --i-data artifacts/main/demux.qza \
        --p-n 10000 \
        --o-visualization artifacts/main/demux_summary.qzv
fi

date -Is
printf 'COMPLETE: import and raw-read quality summary.\n'
