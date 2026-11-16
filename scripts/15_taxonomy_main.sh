#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p logs work/tmp
export TMPDIR="$PWD/work/tmp"
exec > >(tee -a "logs/15_taxonomy_$(date +%Y%m%d_%H%M%S).log") 2>&1
date -Is

classifier="artifacts/pilot/SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza"

python - <<'PY'
from pathlib import Path
from importlib.metadata import version
import re
import zipfile

p = Path("artifacts/pilot/SILVA_144_SSURef_NR99_uniform_classifier_V4-515f-806r.qza")
with zipfile.ZipFile(p) as z:
    roots = {n.split("/")[0] for n in z.namelist()}
    assert len(roots) == 1
    root = roots.pop()
    assert root == "76237f8f-87e0-4d1e-93b9-970bb7603cf0"
    text = z.read(f"{root}/provenance/action/action.yaml").decode()
    match = re.search(r"^\s+scikit-learn:\s*['\"]?([^'\"\s]+)", text, re.M)
    assert match, "Training scikit-learn version not found"
    trained = match.group(1)
    installed = version("scikit-learn")
    print("Classifier training scikit-learn:", trained)
    print("Installed scikit-learn:", installed)
    assert trained == installed, "Version mismatch: stop before classification"
print("PASS: same classifier UUID as pilot; sklearn versions match.")
PY

if [[ ! -e artifacts/main/taxonomy_240_200.qza ]]; then
    stage=$(mktemp -d "$PWD/work/taxonomy-main.XXXXXX")
    qiime feature-classifier classify-sklearn \
        --i-reads artifacts/main/rep_seqs_240_200.qza \
        --i-classifier "$classifier" \
        --p-n-jobs 1 --p-reads-per-batch 1000 \
        --p-pre-dispatch 1 \
        --p-confidence 0.7 --p-read-orientation auto \
        --o-classification "$stage/taxonomy_240_200.qza"
    mv "$stage/taxonomy_240_200.qza" artifacts/main/
else
    printf 'SKIP: taxonomy output already exists; review before reuse.\n'
fi

date -Is
printf 'COMPLETE: main taxonomy.\n'
