#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp artifacts/main
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/13_dada2_$(date +%Y%m%d_%H%M%S).log") 2>&1

date -Is
test -s artifacts/main/demux_readthrough_trimmed.qza

names=(table_240_200 rep_seqs_240_200 denoising_stats_240_200 base_transition_stats_240_200)
existing=0
for name in "${names[@]}"; do
    if [[ -e "artifacts/main/$name.qza" ]]; then
        existing=$((existing + 1))
    fi
done

if [[ "$existing" -eq 4 ]]; then
    printf 'SKIP: all four DADA2 outputs already exist; review before reuse.\n'
    exit 0
elif [[ "$existing" -ne 0 ]]; then
    printf 'STOP: incomplete output set; inspect before resuming.\n'
    exit 1
fi

stage=$(mktemp -d "$PWD/work/dada2-main.XXXXXX")
printf 'Staging directory: %s\n' "$stage"

qiime dada2 denoise-paired \
    --i-demultiplexed-seqs artifacts/main/demux_readthrough_trimmed.qza \
    --p-trunc-len-f 240 --p-trunc-len-r 200 \
    --p-trim-left-f 0 --p-trim-left-r 0 \
    --p-max-ee-f 2 --p-max-ee-r 2 --p-trunc-q 2 \
    --p-min-overlap 12 --p-max-merge-mismatch 0 \
    --p-no-trim-overhang \
    --p-pooling-method independent --p-chimera-method consensus \
    --p-min-fold-parent-over-abundance 1 --p-no-allow-one-off \
    --p-n-reads-learn 1000000 --p-n-threads 2 \
    --p-hashed-feature-ids --p-retain-all-samples \
    --p-no-retain-unmerged \
    --o-table "$stage/table_240_200.qza" \
    --o-representative-sequences "$stage/rep_seqs_240_200.qza" \
    --o-denoising-stats "$stage/denoising_stats_240_200.qza" \
    --o-base-transition-stats "$stage/base_transition_stats_240_200.qza" \
    --verbose

for name in "${names[@]}"; do
    test -s "$stage/$name.qza"
done
for name in "${names[@]}"; do
    mv "$stage/$name.qza" "artifacts/main/$name.qza"
done

date -Is
printf 'COMPLETE: main DADA2 240/200; four artifacts saved.\n'
