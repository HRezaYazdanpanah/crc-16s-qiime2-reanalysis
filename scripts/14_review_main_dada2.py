from pathlib import Path
import pandas as pd

files = list(Path("reports/main_dada2_stats").glob("*.tsv"))
assert len(files) == 1, f"Inspect exported files: {files}"
df = pd.read_csv(files[0], sep="\t", dtype=str)
df = df[~df.iloc[:, 0].str.startswith("#", na=False)].copy()
df = df.rename(columns={df.columns[0]: "sample-id"})
print("Columns:", list(df.columns))

required = ["input", "filtered", "denoised", "merged", "non-chimeric"]
assert all(c in df.columns for c in required), "Unexpected stats schema"
for c in required:
    df[c] = pd.to_numeric(df[c], errors="raise")

assert len(df) == 80 and df["sample-id"].nunique() == 80
assert (df["input"] > 0).all()

df["retained_percent"] = 100 * df["non-chimeric"] / df["input"]
df["review_flag_below_50_percent"] = df["retained_percent"] < 50

df.to_csv("reports/main_dada2_per_sample_QC.tsv", sep="\t", index=False)

totals = df[required].sum()
print("\nStage totals:\n", totals.to_string())
print("\nOverall non-chimeric/input (%):",
      round(100 * totals["non-chimeric"] / totals["input"], 2))
print("\nFinal counts per sample:")
print(df["non-chimeric"].describe().to_string())
print("\nZero-count samples:", int((df["non-chimeric"] == 0).sum()))
print("\nSamples flagged for review:")
flagged = df.loc[df["review_flag_below_50_percent"],
                 ["sample-id"] + required + ["retained_percent"]]
print(flagged.to_string(index=False) if len(flagged) else "None")
print("\nPASS: 80 samples audited; no samples automatically excluded.")
