import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

seed = 20261111
destination = Path("metadata/main_subset_80.tsv")
assert not destination.exists(), "Selection already exists; do not overwrite"

with open("metadata/original/SraRunTable.csv", newline="") as f:
    runs = list(csv.DictReader(f))
with open("metadata/original/metadata.tsv", newline="") as f:
    original = list(csv.DictReader(f, delimiter="\t"))

lookup = {r["sample"]: r for r in original}
assert len(lookup) == len(original), "Duplicate metadata sample IDs"
assert len({r["Run"] for r in runs}) == len(runs), "Duplicate Run IDs"

by_biosample = defaultdict(list)
sample_to_bio = defaultdict(set)
bio_to_sample = defaultdict(set)

for r in runs:
    bio, sample = r["BioSample"], r["Sample Name"]
    assert bio and sample, "Missing mapping identifier"
    by_biosample[bio].append(r)
    sample_to_bio[sample].add(bio)
    bio_to_sample[bio].add(sample)

assert all(len(v) == 1 for v in sample_to_bio.values()), "Ambiguous sample mapping"
assert all(len(v) == 1 for v in bio_to_sample.values()), "Ambiguous BioSample mapping"

labels = {
    "Cancer": "cancer",
    "Normal": "normal",
    "High Risk Normal": "normal",
}
eligible = {"cancer": [], "normal": []}
excluded = Counter()

for bio, records in sorted(by_biosample.items()):
    if len(records) != 1:
        excluded["multiple_runs"] += 1
        continue
    r = records[0]
    dx = labels.get(r["diagnosis"])
    if dx is None:
        excluded["outside_primary_contrast"] += 1
        continue
    sample = r["Sample Name"]
    if sample not in lookup:
        excluded["missing_original_metadata"] += 1
        continue
    m = lookup[sample]
    assert m["dx"] == dx, f"Diagnosis mismatch: {sample}"
    assert r["LibraryLayout"].strip().upper() == "PAIRED", (
        f"Unexpected layout: {r['Run']}"
    )
    eligible[dx].append({
        "sample-id": sample,
        "BioSample": bio,
        "Run": r["Run"],
        "dx": dx,
        "control_subgroup": r["diagnosis"] if dx == "normal" else "",
        **{k: m[k] for k in ("Site", "Age", "Gender", "BMI")},
    })

rng = random.Random(seed)
selected = []
for dx in ("cancer", "normal"):
    pool = sorted(eligible[dx], key=lambda r: (r["sample-id"], r["Run"]))
    assert len(pool) >= 40, f"Insufficient eligible samples: {dx}"
    selected.extend(rng.sample(pool, 40))

selected.sort(key=lambda r: r["sample-id"])
assert len({r["BioSample"] for r in selected}) == 80
assert len({r["sample-id"] for r in selected}) == 80

with destination.open("x", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=list(selected[0]), delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(selected)

with open("metadata/pilot_metadata.tsv", newline="") as f:
    pilot_ids = {r["sample-id"] for r in csv.DictReader(f, delimiter="\t")}

print("Eligible:", {k: len(v) for k, v in eligible.items()})
print("Excluded BioSamples:", dict(excluded))
print("Selected:", dict(Counter(r["dx"] for r in selected)))
print("Selected dx × Site:",
      dict(Counter((r["dx"], r["Site"]) for r in selected)))
print("Selected pilot IDs:",
      sorted(pilot_ids & {r["sample-id"] for r in selected}))
print("Saved:", destination)
