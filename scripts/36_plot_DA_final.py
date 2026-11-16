from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

d = pd.read_csv(
    "reports/main_ancombc2/dx_cancer_final_audited.tsv", sep="\t"
)
valid = d.inference_evaluable.astype(str).str.lower().eq("true")
d = d[valid].copy()
d["ss"] = d.passed_ss.astype(str).str.lower().eq("true")
assert len(d) == 188

fig, (ax, bx) = plt.subplots(1, 2, figsize=(13, 5.8))
order = ["Fusobacterium", "Parvimonas",
         "Peptostreptococcus", "Porphyromonas"]
c = d.set_index("genus_label").loc[order]
assert len(c) == 4

for i, (name, row) in enumerate(c.iterrows()):
    color = "#b45309" if row.q_family_BH < 0.05 else "#64748b"
    marker = "o" if row.ss else "X"
    ax.errorbar(row.lfc, i, xerr=row.se, fmt=marker,
                color=color, capsize=4, markersize=8)
    ax.text(0.98, i + 0.22, f"BH={row.q_family_BH:.4g}",
            transform=ax.get_yaxis_transform(),
            ha="right", fontsize=9)

ax.set_yticks(range(4), order)
ax.set_ylim(3.6, -0.6)
ax.axvline(0, color="grey", linestyle="--", linewidth=1)
ax.set_xlabel("ANCOM-BC2 LFC: cancer versus normal (points ±1 SE)")
ax.set_title("Prespecified hypotheses; BH family n=5")
ax.text(0, -0.23, "Solobacterium: not evaluable (prevalence 7/80)",
        transform=ax.transAxes, fontsize=9)

e = d[d.family.eq("exploratory")].copy()
y = -np.log10(np.maximum(e.q_family_BH.to_numpy(),
                         np.finfo(float).tiny))
for ss, marker in [(True, "o"), (False, "X")]:
    mask = e.ss.eq(ss).to_numpy()
    colors = np.where(e.q_family_BH.to_numpy()[mask] < 0.05,
                      "#b45309", "#64748b")
    bx.scatter(e.lfc.to_numpy()[mask], y[mask],
               c=colors, marker=marker, s=35, alpha=0.8)

bx.axhline(-np.log10(0.05), color="grey", linestyle="--", linewidth=1)
bx.axvline(0, color="grey", linestyle=":", linewidth=1)
for _, row in e[e.q_family_BH < 0.05].iterrows():
    bx.annotate(row.genus_label,
                (row.lfc, -np.log10(max(row.q_family_BH,
                                       np.finfo(float).tiny))),
                xytext=(5, 5), textcoords="offset points", fontsize=9)
bx.set_xlabel("ANCOM-BC2 LFC: cancer versus normal")
bx.set_ylabel("-log10(family BH-adjusted p)")
bx.set_title("Exploratory groups; BH family n=190")
bx.text(0, -0.23, "184 evaluable; 6 not evaluable (5 zero-df, 1 missing estimate)",
        transform=bx.transAxes, fontsize=9)

handles = [
    Line2D([], [], marker="o", color="grey", linestyle="None",
           label="passed_ss=True"),
    Line2D([], [], marker="X", color="grey", linestyle="None",
           label="passed_ss=False"),
    Line2D([], [], marker="s", color="#b45309", linestyle="None",
           label="Family BH < 0.05")
]
fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False)
fig.tight_layout(rect=(0, 0.06, 1, 0.91))
Path("figures").mkdir(exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(f"figures/main_DA_summary_final.{ext}",
                dpi=300, bbox_inches="tight")
plt.close(fig)
print("Saved figures/main_DA_summary_final.png and .pdf")
print("Error bars: ±1 SE, not 95% CI. No models refitted.")
