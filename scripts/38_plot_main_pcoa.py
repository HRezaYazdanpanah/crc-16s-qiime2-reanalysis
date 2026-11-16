from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiime2 import Artifact
from skbio.stats.ordination import OrdinationResults

ordination = Artifact.load(
    "artifacts/main/braycurtis_14235_pcoa.qza"
).view(OrdinationResults)

coords = ordination.samples.iloc[:, :2].copy()
coords.columns = ["PC1", "PC2"]

metadata = pd.read_csv(
    "reports/main_metadata_audit/audited_metadata.tsv",
    sep="\t", dtype=str
).set_index("sample-id")

assert len(coords) == 80
assert not metadata.index.duplicated().any()
assert set(coords.index) == set(metadata.index)
data = coords.join(metadata[["dx", "Site"]], validate="one_to_one")
assert not data.isna().any().any()

D = pd.read_csv(
    "reports/main_braycurtis_14235/distance-matrix.tsv",
    sep="\t", index_col=0
)
assert set(D.index.astype(str)) == set(data.index.astype(str))
assert list(D.index.astype(str)) == list(D.columns.astype(str))

A = D.to_numpy(dtype=float)**2
B = -0.5 * (
    A - A.mean(axis=0)[None, :]
    - A.mean(axis=1)[:, None] + A.mean()
)
eigenvalues = np.linalg.eigvalsh(B)
negative = eigenvalues[eigenvalues < -1e-10]
positive = eigenvalues[eigenvalues > 1e-10]

print("Negative eigenvalues (tolerance -1e-10):", len(negative))
print("Sum |negative| / sum positive:",
      float(np.abs(negative).sum() / positive.sum()))
print("Most negative eigenvalue:", float(eigenvalues.min()))

proportions = ordination.proportion_explained.iloc[:2].to_numpy()
print("Reported PC1 and PC2 proportions:", proportions)
print("Two-axis reported cumulative proportion:", proportions.sum())

colors = {
    "normal": "#2563eb",
    "cancer": "#d97706",
    "Dana Farber": "#7c3aed",
    "MD Anderson": "#059669",
    "Toronto": "#dc2626",
    "U Michigan": "#475569"
}

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, column in zip(axes, ["dx", "Site"]):
    for label in sorted(data[column].unique()):
        subset = data[data[column].eq(label)]
        ax.scatter(
            subset.PC1, subset.PC2,
            s=35, alpha=0.8, color=colors[label],
            label=f"{label} (n={len(subset)})"
        )
    ax.set_xlabel(f"PC1 ({100*proportions[0]:.2f}%)")
    ax.set_ylabel(f"PC2 ({100*proportions[1]:.2f}%)")
    ax.set_title(f"Colored by {column}")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(frameon=False, fontsize=8)

fig.suptitle(
    "Bray-Curtis PCoA; depth 14235; 80 samples\n"
    "Unadjusted ordination; descriptive visualization"
)
fig.tight_layout()

Path("figures").mkdir(exist_ok=True)
for extension in ("png", "pdf"):
    fig.savefig(
        f"figures/main_braycurtis_pcoa.{extension}",
        dpi=300, bbox_inches="tight"
    )
plt.close(fig)

output = Path("reports/main_braycurtis_pcoa")
output.mkdir(parents=True, exist_ok=True)
data.rename_axis("sample-id").to_csv(
    output / "plot_coordinates.tsv", sep="\t"
)
print("Saved PCoA figures and coordinates; no tests refitted.")
