import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Load Data
# ============================================================

df = pd.read_csv("../data/experiment_summary.csv")

# Only experiments with 40 attackers
df = df[df["users"] == 40].copy()

# ============================================================
# Selected attacks
# ============================================================

attack_map = {

    "index: 4,":
        ("Index Flooding", "Naive"),

    "all: 1,":
        ("Entire Application", "Naive"),

    "addToCart: 4, viewCart: 1, emptyCart: 1,":
        ("AddToCart", "Workflow-aware"),

    "checkout: 4,":
        ("Checkout", "Workflow-aware"),

    "setCurrency: 4, browseProduct: 0, browseProductByID: 1,":
        ("Currency", "Dependency-aware")
}

df = df[df["target"].isin(attack_map.keys())].copy()

# ============================================================
# Add attack name and category
# ============================================================

df["AttackName"] = df["target"].apply(lambda x: attack_map[x][0])

df["AttackType"] = df["target"].apply(lambda x: attack_map[x][1])

# ============================================================
# Attack Efficiency
# ============================================================

df["AttackEfficiency"] = (
    df["slo_violation_sum"] /
    df["total_requests"]
)

# ============================================================
# Summary per attack
# ============================================================

summary_attack = (

    df.groupby("AttackName")

    .agg(

        Runs=("AttackEfficiency", "count"),

        MeanEfficiency=("AttackEfficiency", "mean"),

        StdEfficiency=("AttackEfficiency", "std"),

        MeanSLO=("slo_violation_sum", "mean"),

        MeanRequests=("total_requests", "mean"),

        MeanResource=("total_resource_usage", "mean")

    )

    .reset_index()

)

summary_attack["95CI"] = (

    1.96 *

    summary_attack["StdEfficiency"] /

    np.sqrt(summary_attack["Runs"])

)

summary_attack = summary_attack.sort_values(
    "MeanEfficiency",
    ascending=False
)

summary_attack.to_csv(
    "../tables/Individual_Attacks.csv",
    index=False
)

print(summary_attack)

print(summary_attack.to_latex(
    index=False,
    float_format="%.3f"
))

# ============================================================
# Summary per attack category
# ============================================================

summary_type = (

    df.groupby("AttackType")

    .agg(

        Runs=("AttackEfficiency", "count"),

        MeanEfficiency=("AttackEfficiency", "mean"),

        StdEfficiency=("AttackEfficiency", "std"),

        MeanSLO=("slo_violation_sum", "mean"),

        MeanRequests=("total_requests", "mean"),

        MeanResource=("total_resource_usage", "mean")

    )

    .reset_index()

)

summary_type["95CI"] = (

    1.96 *

    summary_type["StdEfficiency"] /

    np.sqrt(summary_type["Runs"])

)

summary_type = summary_type.sort_values(
    "MeanEfficiency",
    ascending=False
)

summary_type.to_csv(
    "../tables/Attack_Summary.csv",
    index=False
)

print(summary_type)

print(summary_type.to_latex(
    index=False,
    float_format="%.3f"
))

# ============================================================
# Figure 1: Attack Efficiency
# ============================================================

order = [
    "Naive",
    "Workflow-aware",
    "Dependency-aware"
]

plt.figure(figsize=(6.5, 3.2))

sns.boxplot(
    data=df,
    x="AttackType",
    y="AttackEfficiency",
    order=order,
    width=0.6,
)

sns.stripplot(
    data=df,
    x="AttackType",
    y="AttackEfficiency",
    order=order,
    color="black",
    size=3,
    alpha=0.5,
)

plt.ylabel("Attack Efficiency", fontsize=12)
plt.xlabel("")
plt.grid(axis="y", alpha=0.3)

plt.xticks(fontsize=12)

ax = plt.gca()

for spine in ax.spines.values():
    spine.set_linewidth(1)
    spine.set_color("black")

plt.tight_layout()

plt.savefig(
    "../figures/AttackEfficiency_Box.pdf",
    dpi=600,
    bbox_inches="tight"
)
plt.show()
plt.close()

# ============================================================
# Figure 2: EDoS Landscape
# ============================================================

plt.figure(figsize=(8.2, 4.8))

sizes = summary_attack["MeanResource"] / 4

plt.scatter(
    summary_attack["MeanRequests"],
    summary_attack["MeanSLO"],
    s=sizes,
    alpha=0.6
)

for _, row in summary_attack.iterrows():
    plt.text(
        row["MeanRequests"] + 300,
        row["MeanSLO"],
        row["AttackName"],
        fontsize=12
    )

plt.xlabel("Average Attack Requests", fontsize=14)
plt.ylabel("Average Accumulated SLO Violation (ms)", fontsize=14)

plt.grid(alpha=0.3)

ax = plt.gca()

for spine in ax.spines.values():
    spine.set_linewidth(1)
    spine.set_color("black")

plt.tight_layout()

plt.savefig(
    "../figures/EDoS_Landscape.pdf",
    dpi=600,
    bbox_inches="tight"
)
plt.show()
plt.close()

print("\nReproduction completed successfully.")