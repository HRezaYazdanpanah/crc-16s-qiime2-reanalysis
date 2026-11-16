#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/16_tree_$(date +%Y%m%d_%H%M%S).log") 2>&1
date -Is

names=(aligned_240_200 masked_240_200 unrooted_tree_240_200 rooted_tree_240_200)
existing=0
for name in "${names[@]}"; do
    if [[ -e "artifacts/main/$name.qza" ]]; then
        existing=$((existing + 1))
    fi
done

if [[ "$existing" -eq 4 ]]; then
    printf 'SKIP: all four tree outputs already exist; review before reuse.\n'
    exit 0
elif [[ "$existing" -ne 0 ]]; then
    printf 'STOP: incomplete tree output set; inspect before resuming.\n'
    exit 1
fi

stage=$(mktemp -d "$PWD/work/tree-main.XXXXXX")

qiime phylogeny align-to-tree-mafft-fasttree \
    --i-sequences artifacts/main/rep_seqs_240_200.qza \
    --p-n-threads 1 \
    --p-mask-max-gap-frequency 1.0 \
    --p-mask-min-conservation 0.4 \
    --o-alignment "$stage/aligned_240_200.qza" \
    --o-masked-alignment "$stage/masked_240_200.qza" \
    --o-tree "$stage/unrooted_tree_240_200.qza" \
    --o-rooted-tree "$stage/rooted_tree_240_200.qza"

for name in "${names[@]}"; do
    test -s "$stage/$name.qza"
done
for name in "${names[@]}"; do
    mv "$stage/$name.qza" "artifacts/main/$name.qza"
done

date -Is
printf 'COMPLETE: main alignment, masking and rooted/unrooted trees.\n'
