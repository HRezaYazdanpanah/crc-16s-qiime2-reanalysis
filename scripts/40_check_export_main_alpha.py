from pathlib import Path
import numpy as np
import pandas as pd
from qiime2 import Artifact, Metadata

metadata = pd.read_csv(
    "reports/main_metadata_audit/audited_metadata.tsv",
    sep="\t", dtype=str
).set_index("sample-id")

assert len(metadata) == 80, "Expected 80 metadata rows"
assert metadata.index.is_unique, "Duplicate metadata IDs"

vectors = {}
for metric in ["observed_features", "shannon"]:
    artifact = Artifact.load(f"artifacts/main/{metric}_14235.qza")
    assert str(artifact.type) == "SampleData[AlphaDiversity]"
    frame = artifact.view(Metadata).to_dataframe()
    assert frame.shape == (80, 1), f"Unexpected shape: {metric}"
    assert frame.index.is_unique, f"Duplicate IDs: {metric}"
    assert set(frame.index) == set(metadata.index), f"ID mismatch: {metric}"

    values = pd.to_numeric(frame.iloc[:, 0], errors="raise")
    assert np.isfinite(values.to_numpy()).all(), f"Invalid values: {metric}"
    assert (values >= 0).all(), f"Negative values: {metric}"
    vectors[metric] = values.reindex(metadata.index)

alpha = pd.DataFrame(vectors)
assert (alpha["observed_features"] > 0).all()
assert np.equal(
    alpha["observed_features"],
    np.floor(alpha["observed_features"])
).all(), "Observed features must be integer counts"
alpha["observed_features"] = alpha["observed_features"].astype(int)

summary = alpha.describe(
    percentiles=[0.25, 0.5, 0.75]
).T[["count", "min", "25%", "50%", "75%", "max", "mean", "std"]]

output = Path("reports/main_alpha_14235")
output.mkdir(parents=True, exist_ok=True)
alpha.rename_axis("sample-id").to_csv(
    output / "alpha_per_sample.tsv", sep="\t"
)
summary.rename_axis("metric").to_csv(
    output / "alpha_summary_overall.tsv", sep="\t"
)

print("PASS: both metrics have exactly the 80 audited sample IDs.")
print("PASS: finite, nonnegative values; observed features are positive integers.")
print(summary.to_string(float_format=lambda x: f"{x:.4f}"))
print("Saved per-sample and overall summary tables; no group tests.")
