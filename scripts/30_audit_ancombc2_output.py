import json
from pathlib import Path
import numpy as np
import pandas as pd

root = Path("reports/main_ancombc2")
term = "dx::cancer"
eligibility = pd.read_csv(
    "reports/main_genus_audit/final_eligibility.tsv",
    sep="\t", keep_default_na=False
)
eligible = eligibility[eligibility.DA_eligible].copy()
expected = set(eligible.taxonomy)

def read_stat(name):
    with (root / "export" / f"{name}.jsonl").open() as handle:
        records = [json.loads(line) for line in handle if line.strip()]
    header, rows = records[0], records[1:]
    fields = {field["name"]: field for field in header["fields"]}
    assert fields[term]["extra"]["reference"] == "normal"
    df = pd.DataFrame(rows)
    assert {"taxon", term}.issubset(df.columns), list(df.columns)
    assert len(df) == 194 and not df.taxon.duplicated().any()
    assert set(df.taxon) == expected
    return df.set_index("taxon")[term].rename(name)

stats = pd.concat(
    [read_stat(name) for name in ("lfc", "se", "p", "q", "passed_ss")],
    axis=1
)
for col in ("lfc", "se", "p", "q"):
    stats[col] = pd.to_numeric(stats[col], errors="raise")

stats["valid_estimate"] = (
    np.isfinite(stats["lfc"]) &
    np.isfinite(stats["se"]) &
    (stats["se"] > 0) &
    np.isfinite(stats["p"]) & stats["p"].between(0, 1)
)
result = eligible.merge(
    stats, left_on="taxonomy", right_index=True,
    validate="one_to_one"
)
result.to_csv(root / "dx_cancer_audited_unadjusted.tsv",
              sep="\t", index=False)

print("Rows matched:", len(result))
print("Valid estimates:", int(result.valid_estimate.sum()))
print("Invalid estimates:", int((~result.valid_estimate).sum()))
print("\nMissing values:")
print(stats.isna().sum().to_string())
print("\npassed_ss values:")
print(stats.passed_ss.value_counts(dropna=False).to_string())

same = np.isclose(stats["p"], stats["q"], equal_nan=True)
print("\nRaw p and exported q equal for all rows:", bool(same.all()))
print("\nInvalid-estimate taxonomy labels:")
for label in result.loc[~result.valid_estimate, "taxonomy"]:
    print(label)
print("\nCOMPLETE: audit only; no family-specific BH applied.")
