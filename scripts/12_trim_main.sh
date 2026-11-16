#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp artifacts/main
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/12_trim_$(date +%Y%m%d_%H%M%S).log") 2>&1

date -Is
seqs="artifacts/main/demux_readthrough_trimmed.qza"
stats="artifacts/main/cutadapt_stats.qza"

if [[ -e "$seqs" && -e "$stats" ]]; then
    printf 'SKIP: both Cutadapt outputs exist; review before reuse.\n'
elif [[ -e "$seqs" || -e "$stats" ]]; then
    printf 'STOP: only one Cutadapt output exists; inspect before resuming.\n'
    exit 1
else
    qiime cutadapt trim-paired \
        --i-demultiplexed-sequences artifacts/main/demux.qza \
        --p-adapter-f ATTAGAWACCCBDGTAGTCC \
        --p-adapter-r TTACCGCGGCKGCTGGCAC \
        --p-forward-cut 0 --p-reverse-cut 0 \
        --p-error-rate 0.1 --p-overlap 12 \
        --p-minimum-length 1 --p-pair-filter any \
        --p-no-discard-untrimmed --p-no-discard-trimmed \
        --p-quality-cutoff-5end 0 --p-quality-cutoff-3end 0 \
        --p-cores 2 \
        --o-trimmed-sequences "$seqs" \
        --o-stats "$stats"
fi

if [[ ! -e artifacts/main/demux_readthrough_trimmed_summary.qzv ]]; then
    qiime demux summarize \
        --i-data "$seqs" \
        --p-n 10000 \
        --o-visualization artifacts/main/demux_readthrough_trimmed_summary.qzv
fi

date -Is
printf 'COMPLETE: main Cutadapt and post-trim summary. DADA2 NOT started.\n'
