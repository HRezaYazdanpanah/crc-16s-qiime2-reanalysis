import json
import numpy as np
import pandas as pd
from biom import load_table
from scipy.stats import t

table = load_table("reports/main_genus_DA_export/feature-table.biom")
ids = list(table.ids(axis="sample"))
m = pd.read_csv(
    "reports/main_metadata_audit/audited_metadata.tsv",
    sep="\t", dtype=str
).set_index("sample-id").loc[ids]

numeric = m[["Age", "BMI"]].apply(pd.to_numeric)
categorical = pd.get_dummies(
    m[["dx", "Gender", "Site"]], drop_first=True, dtype=float
)
X = np.column_stack([
    np.ones(len(m)), numeric.to_numpy(), categorical.to_numpy()
])
assert X.shape == (80, 8) and np.linalg.matrix_rank(X) == 8

with open("reports/main_ancombc2/export/W.jsonl") as handle:
    records = [json.loads(line) for line in handle if line.strip()]
W = {r["taxon"]: r["dx::cancer"] for r in records[1:]}

d = pd.read_csv(
    "reports/main_ancombc2/dx_cancer_family_BH.tsv", sep="\t"
)
rows = []
for _, row in d.iterrows():
    positive = table.data(row.taxonomy, axis="observation") > 0
    n = int(positive.sum())
    rank = int(np.linalg.matrix_rank(X[positive]))
    df = n - rank
    w = W[row.taxonomy]
    p_check = (
        2 * t.sf(abs(float(w)), df)
        if df > 0 and w is not None and np.isfinite(float(w))
        else np.nan
    )
    rows.append({
        "taxonomy": row.taxonomy,
        "genus_label": row.genus_label,
        "n_positive": n,
        "nonzero_design_rank": rank,
        "nonzero_residual_df": df,
        "W_exported": w,
        "p_exported": row.p,
        "p_using_nonzero_df": p_check,
        "q_family_BH": row.q_family_BH
    })

a = pd.DataFrame(rows)
a.to_csv("reports/main_ancombc2/nonzero_support_audit.tsv",
         sep="\t", index=False)

print("Groups with nonzero-support residual df <= 0:",
      int((a.nonzero_residual_df <= 0).sum()))
print("\nGroups requiring support review:")
print(a.loc[a.nonzero_residual_df <= 0].drop(
    columns="taxonomy").to_string(index=False))

print("\nTwo BH findings plus Thermanaerosceptrum:")
print(a[a.genus_label.isin(
    ["Parvimonas", "Hallella", "Thermanaerosceptrum"]
)].drop(columns="taxonomy").to_string(index=False))

comparable = (
    np.isfinite(a.p_using_nonzero_df) &
    np.isfinite(a.p_exported)
)
matches = np.isclose(
    a.loc[comparable, "p_using_nonzero_df"],
    a.loc[comparable, "p_exported"],
    rtol=1e-6, atol=1e-9
)
print("\nExported p matches nonzero-support t calculation:",
      int(matches.sum()), "/", int(comparable.sum()))
print("Diagnostic only: original outputs and BH tables unchanged.")
