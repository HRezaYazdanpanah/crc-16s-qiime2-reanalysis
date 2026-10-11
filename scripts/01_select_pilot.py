import csv
import random
import sys
from collections import defaultdict

SEED = 20261011
N_PER_GROUP = 4

with open("metadata/original/metadata.tsv", newline="") as f:
    metadata = list(csv.DictReader(f, delimiter="\t"))

with open("metadata/original/SraRunTable.csv", newline="") as f:
    runs = list(csv.DictReader(f))

sample_ids = [row["sample"] for row in metadata]
assert len(sample_ids) == len(set(sample_ids)), "Duplicate sample IDs"

runs_by_sample = defaultdict(list)
for row in runs:
    runs_by_sample[row["Sample Name"]].append(row)

rng = random.Random(SEED)
selected = []

for group in ("cancer", "normal"):
    eligible = sorted(
        [
            row for row in metadata
            if row["dx"] == group
            and len(runs_by_sample[row["sample"]]) == 1
        ],
        key=lambda row: row["sample"],
    )
    assert len(eligible) >= N_PER_GROUP, "Too few eligible samples"

    for row in rng.sample(eligible, N_PER_GROUP):
        run = runs_by_sample[row["sample"]][0]
        assert run["LibraryLayout"] == "PAIRED", "Unexpected layout"
        selected.append({
            "sample": row["sample"],
            "dx": row["dx"],
            "Site": row["Site"],
            "Run": run["Run"],
            "seed": SEED,
            "python_version": sys.version.split()[0],
        })

output = "metadata/pilot_samples.tsv"
with open(output, "x", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=list(selected[0]), delimiter="\t"
    )
    writer.writeheader()
    writer.writerows(selected)

print(f"Saved {len(selected)} samples to {output}")
for row in selected:
    print(row["sample"], row["dx"], row["Site"], row["Run"], sep="\t")
