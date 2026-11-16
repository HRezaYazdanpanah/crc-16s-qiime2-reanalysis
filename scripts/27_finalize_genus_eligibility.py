from pathlib import Path
import pandas as pd

out = Path("reports/main_genus_audit")
df = pd.read_csv(out / "pooled_prevalence.tsv",
                 sep="\t", keep_default_na=False)
assert len(df) == 426
assert not df.taxonomy.duplicated().any()

name = df.genus_label.str.strip()
df["has_genus_label"] = name.ne("")
df["incertae_sedis"] = name.str.casefold().eq("incertae_sedis")
df["taxonomy_eligible"] = df.has_genus_label & ~df.incertae_sedis
df["prevalence_eligible"] = df.n_present >= 8
df["DA_eligible"] = df.taxonomy_eligible & df.prevalence_eligible

targets = [
    "Fusobacterium", "Parvimonas", "Peptostreptococcus",
    "Porphyromonas", "Solobacterium"
]
df["family"] = "not_tested"
df.loc[df.DA_eligible, "family"] = "exploratory"
df.loc[df.DA_eligible & name.isin(targets), "family"] = "confirmatory"

df.to_csv(out / "final_eligibility.tsv", sep="\t", index=False)
eligible = df[df.DA_eligible].copy()
assert len(eligible) > 0

pd.DataFrame({"feature-id": eligible.taxonomy}).to_csv(
    out / "eligible_feature_ids.tsv", sep="\t", index=False
)

hypotheses = df[name.isin(targets)].copy()
assert all((name == target).sum() == 1 for target in targets)
hypotheses.to_csv(
    out / "confirmatory_eligibility.tsv", sep="\t", index=False
)

print("Starting taxonomy groups:", len(df))
print("Passing prevalence alone:", int(df.prevalence_eligible.sum()))
print("Passing prevalence but excluded by taxonomy:",
      int((df.prevalence_eligible & ~df.taxonomy_eligible).sum()))
print("Final eligible groups:", len(eligible))
print("\nEligible groups by family:")
print(eligible.family.value_counts().to_string())

print("\nPrespecified hypotheses:")
print(hypotheses[
    ["genus_label", "n_present", "DA_eligible", "family"]
].to_string(index=False))

print("\nCOMPLETE: eligibility files written; no table filtering or DA fitted.")
