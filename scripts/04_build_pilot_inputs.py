import csv
from pathlib import Path

with open("metadata/pilot_samples.tsv", newline="") as f:
    pilot = list(csv.DictReader(f, delimiter="\t"))

with open("metadata/original/metadata.tsv", newline="") as f:
    original = list(csv.DictReader(f, delimiter="\t"))

lookup = {row["sample"]: row for row in original}
assert len(lookup) == len(original), "Duplicate original sample IDs"
assert len({row["sample"] for row in pilot}) == 8, "Expected 8 unique samples"

manifest = []
metadata = []

for row in pilot:
    sample = row["sample"]
    run = row["Run"]
    source = lookup[sample]
    assert row["dx"] == source["dx"], "Diagnosis mismatch"

    forward = Path(f"data/raw/pilot/{run}_1.fastq.gz").resolve()
    reverse = Path(f"data/raw/pilot/{run}_2.fastq.gz").resolve()
    assert forward.is_file() and reverse.is_file(), f"Missing files: {run}"

    manifest.append({
        "sample-id": sample,
        "forward-absolute-filepath": str(forward),
        "reverse-absolute-filepath": str(reverse),
    })

    metadata.append({
        "sample-id": sample,
        "dx": source["dx"],
        "Site": source["Site"],
        "Age": source["Age"],
        "Gender": source["Gender"],
        "BMI": source["BMI"] or "",
        "Run": run,
    })

for path, rows in [
    ("metadata/pilot_manifest.tsv", manifest),
    ("metadata/pilot_metadata.tsv", metadata),
]:
    with open(path, "x", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(rows[0]), delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} samples: {path}")
