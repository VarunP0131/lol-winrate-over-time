import numpy as np
import matplotlib.pyplot as plt

# Define one-trick champions
one_trick_champs = ["Zed", "Shen", "Qiyana", "Evelynn", "Warwick", "Vladimir", "Ezreal"]

# Add a 5-minute time bin column
df["duration_bin"] = (df["game_duration_minutes"] // 5 * 5).astype(int)

# Filter only the one-trick champions
df = df[df["champion"].isin(one_trick_champs)]

# Compute weights (normalize if needed)
df["weight"] = (
    0.2 * df["dragon_takedowns"] +
    0.2 * df["baron_takedowns"] +
    0.2 * df["kill_participation"] +
    0.2 * df["damage_per_min"] +
    0.2 * df["gold_per_min"]
)

# Group and compute weighted win rate
grouped = df.groupby(["champion", "duration_bin"]).apply(
    lambda g: pd.Series({
        "weighted_win_rate": np.average(g["win"], weights=g["weight"])
    })
).reset_index()


# Plot for each champion
for champ in one_trick_champs:
    champ_data = grouped[grouped["champion"] == champ]
    plt.figure(figsize=(8, 5))
    plt.plot(champ_data["duration_bin"], champ_data["weighted_win_rate"], marker='o', linestyle='-', label=champ)
    plt.title(f"{champ} Weighted Win Rate Over Game Time")
    plt.xlabel("Game Time (Minutes, Binned)")
    plt.ylabel("Weighted Win Rate")
    plt.grid(True)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(f"{champ}_weighted_winrate.png")
    plt.close()
