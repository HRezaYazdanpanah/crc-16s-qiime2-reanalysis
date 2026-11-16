import csv
from pathlib import Path

def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

samples = read("metadata/main_subset_80.tsv")
assert len(samples) == 80
assert len({s["sample-id"] for s in samples}) == 80
assert len({s["Run"] for s in samples}) == 80

manifest, metadata = [], []
for s in samples:
    paths = [(Path("data/raw/main") /
              f"{s['Run']}_{mate}.fastq.gz").resolve() for mate in (1, 2)]
    assert all(p.is_file() for p in paths), s["Run"]
    manifest.append({
        "sample-id": s["sample-id"],
        "forward-absolute-filepath": str(paths[0]),
        "reverse-absolute-filepath": str(paths[1]),
    })
    metadata.append({k: s[k] for k in (
        "sample-id", "dx", "Site", "Age", "Gender", "BMI", "Run", "BioSample"
    )})

for name, rows in (
    ("metadata/main_manifest.tsv", manifest),
    ("metadata/main_metadata.tsv", metadata),
):
    path = Path(name)
    if path.exists():
        assert read(path) == rows, f"Existing file differs: {name}"
        print("UNCHANGED:", name)
    else:
        with path.open("x", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]),
                                    delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        print("CREATED:", name)

print("PASS: 80 samples; no samples excluded or reselected.")
