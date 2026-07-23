import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hypothesis_test import welch_ci

plt.rcParams.update({
    'font.size': 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})

COLOUR_TREAT = "#A8DADC"
COLOUR_CONTROL = "#6D597A"

def distribution_plot(df, output_path):
    treat = df[df["group"] == "controlled_hangs"]["gain_kg"]
    control = df[df["group"] == "max_effort_hangs"]["gain_kg"]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bp = ax.boxplot([treat, control], positions = [1,2], widths = 0.4,
                    patch_artist = True, showmeans = True, meanline = True,)
    for patch, colour in zip(bp['boxes'], [COLOUR_TREAT, COLOUR_CONTROL]):
        patch.set_facecolor(colour)
        patch.set_alpha(0.3)

    # Scatter the individual climbers on top of the boxplot with a small amount of horizontal jitter
    rng = np.random.default_rng(0)
    for pos, d, colour in zip([1, 2], [treat, control], [COLOUR_TREAT, COLOUR_CONTROL]):
        jitter = rng.normal(0, 0.05, size=len(d))
        ax.scatter(np.full(len(d), pos) + jitter, d, color=colour,
                   s = 45, zorder = 3, edgecolor = "white", linewidth = 0.5)

    ax.set_xticks([1, 2])
    ax.set_xticklabels([ "Controlled hang protocol","Max-effort protocol",])
    ax.set_ylabel("Gain in crimp strength (kg) after 8 weeks \nover 8 weeks of training")
    ax.set_title("Distribution of strength gains by protocol", fontweight = "bold")
    ax.axhline(0, color = "black", linewidth = 0.6, linestyle = ":")
    plt.tight_layout()
    plt.savefig(output_path, dpi = 150)
    plt.close()

def effect_size_plot(df, output_path):
    treat = df[df["group"] == "controlled_hangs"]["gain_kg"]
    control = df[df["group"] == "max_effort_hangs"]["gain_kg"]

    diff = treat.mean() - control.mean()
    ci_low, ci_high = welch_ci(treat, control)

    fig, ax = plt.subplots(figsize=(7, 2.8))
    ax.errorbar([diff], [0],
                xerr=[[diff - ci_low], [ci_high - diff]],
                fmt="o", color=COLOUR_TREAT, markersize=10,
                capsize=6, capthick=2, elinewidth=2)
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--",
               label="No difference")
    ax.set_yticks([])
    ax.set_xlabel("Difference in mean gain, controlled \u2212 max-effort (kg)")
    ax.set_title("Effect size with 95% confidence interval", fontweight="bold")
    ax.legend(loc="upper right", frameon=False)
    ax.set_ylim(-1, 1)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("data/simulated_climber_data.csv")
    distribution_plot(df, "distribution_plot.png")  
    effect_size_plot(df, "effect_size_plot.png")