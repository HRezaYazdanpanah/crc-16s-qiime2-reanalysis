from pathlib import Path
import numpy as np
import pandas as pd
from biom import load_table

table = load_table(
    "reports/main_genus_level7_export/feature-table.biom"
)
assert table.shape[1] == 80

labels = list(table.ids(axis="observation"))
counts = table.matrix_data.tocsr()
present = counts.copy()
present.data = (present.data > 0).astype(int)
n_present = np.asarray(present.sum(axis=1)).ravel().astype(int)
total = np.asarray(counts.sum(axis=1)).ravel().astype(int)

def genus_label(taxonomy):
    parts = [p.strip() for p in taxonomy.split(";")]
    return next((p[3:].strip() for p in parts if p.startswith("g__")), "")

df = pd.DataFrame({
    "taxonomy": labels,
    "genus_label": [genus_label(t) for t in labels],
    "n_present": n_present,
    "prevalence": n_present / table.shape[1],
    "total_counts": total,
    "passes_prevalence": n_present >= 8
})

out = Path("reports/main_genus_audit")
out.mkdir(parents=True, exist_ok=True)
df.to_csv(out / "pooled_prevalence.tsv", sep="\t", index=False)

print("Taxonomy groups:", len(df))
print("Pass prevalence >=8/80:", int(df.passes_prevalence.sum()))
print("No nonempty g__ label:", int(df.genus_label.eq("").sum()))

duplicates = df[
    df.genus_label.ne("") &
    df.genus_label.duplicated(keep=False)
]
duplicates.to_csv(out / "repeated_genus_labels.tsv", sep="\t", index=False)
print("Rows with repeated nonempty genus labels:", len(duplicates))

targets = [
    "Fusobacterium", "Parvimonas", "Peptostreptococcus",
    "Porphyromonas", "Solobacterium"
]
for name in targets:
    matched = df[df.genus_label.eq(name)]
    print(f"\n===== {name}: exact matches={len(matched)} =====")
    if matched.empty:
        print("NO EXACT MATCH: taxonomy review required; do not substitute.")
    else:
        print(matched.to_string(index=False))

print("\nCOMPLETE: pooled audit only; no filtering or DA fitted.")
