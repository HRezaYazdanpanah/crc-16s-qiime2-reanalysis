from pathlib import Path
import csv
import biom
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

files = list(Path("reports/main_table_export").glob("*.biom"))
assert len(files) == 1, files
table = biom.load_table(str(files[0]))
ids = list(table.ids(axis="sample"))
counts = np.asarray(table.sum(axis="sample")).ravel()
assert np.all(counts == np.floor(counts))
counts = counts.astype(int)

with open("metadata/main_subset_80.tsv", newline="") as f:
    expected = {r["sample-id"] for r in csv.DictReader(f, delimiter="\t")}
assert set(ids) == expected and len(ids) == 80

df = pd.DataFrame({"sample-id": ids, "counts": counts})
df = df.sort_values(["counts", "sample-id"])
df.to_csv("reports/main_library_sizes.tsv", sep="\t", index=False)

depths = sorted({10000, 14000, int(counts.min()),
                 15000, 20000, 25000, 30000})
rows = []
for depth in depths:
    n = int((counts >= depth).sum())
    rows.append({
        "depth": depth,
        "samples_retained": n,
        "samples_excluded": len(counts) - n,
        "sample_retention_percent": round(100 * n / len(counts), 2),
        "counts_in_rarefied_table": depth * n,
        "percent_of_original_counts_used":
            round(100 * depth * n / counts.sum(), 2),
    })
review = pd.DataFrame(rows)
review.to_csv("reports/main_depth_tradeoffs.tsv", sep="\t", index=False)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(counts, bins=15, edgecolor="black")
axes[0].set(xlabel="Counts per sample", ylabel="Number of samples")
axes[1].plot(df["counts"], np.arange(1, len(df) + 1) / len(df),
             drawstyle="steps-post")
axes[1].set(xlabel="Counts per sample", ylabel="Cumulative fraction")
fig.suptitle("Main subset: pooled library sizes; no diagnosis stratification")
fig.tight_layout()
fig.savefig("figures/main_library_sizes.png", dpi=180)
plt.close(fig)

print("Samples:", len(ids), "ASVs:", table.shape[0])
print("Total counts:", int(counts.sum()))
print("\nLibrary-size summary:\n", df["counts"].describe().to_string())
print("\nDepth trade-offs:\n", review.to_string(index=False))
print("\nSaved pooled plot and TSV reports; no rarefaction performed.")
