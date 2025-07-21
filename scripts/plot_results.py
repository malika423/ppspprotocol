"""
plot_results.py

Reads results.csv and generates three plots:
1. Delivery Success vs Steal Probability
2. Average Hops ± Std Dev
3. Coefficient of Variation (σ / μ)
"""

import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO


def main() -> None:
    # Read raw CSV lines
    with open("results.csv", "r") as f:
        lines = f.readlines()

    # Locate blank line between trial and summary
    blank_index = next(
        i for i, line in enumerate(lines) if line.strip() == ""
    )
    summary_lines = lines[blank_index + 2:]

    # Prepend correct header to summary block
    summary_header = [
        "steal_prob",
        "success_rate",
        "avg_hops",
        "std_hops",
    ]
    summary_str = "".join(
        [",".join(summary_header) + "\n"] + summary_lines
    )
    summary = pd.read_csv(StringIO(summary_str))

    # Plot 1: Delivery Success vs Steal Probability
    plt.figure()
    plt.plot(
        summary["steal_prob"],
        summary["success_rate"],
        marker="o",
    )
    plt.xlabel("Steal Probability (p)")
    plt.ylabel("Delivery Success Rate")
    plt.title("Delivery Success vs Steal Probability")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("success_rate.png", dpi=300)

    # Plot 2: Average Hops ± σ
    plt.figure()
    plt.errorbar(
        summary["steal_prob"],
        summary["avg_hops"],
        yerr=summary["std_hops"],
        fmt="s",
        capsize=5,
    )
    plt.xlabel("Steal Probability (p)")
    plt.ylabel("Average Hops (±σ)")
    plt.title("Average Hops vs Steal Probability")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("avg_hops.png", dpi=300)

    # Plot 3: Coefficient of Variation (σ / μ)
    cv = summary["std_hops"] / summary["avg_hops"]
    plt.figure()
    plt.plot(summary["steal_prob"], cv, marker="^")
    plt.xlabel("Steal Probability (p)")
    plt.ylabel("Coefficient of Variation (σ / μ)")
    plt.title("CV vs Steal Probability")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cv_vs_p.png", dpi=300)

    print("Plots generated: success_rate.png, avg_hops.png, cv_vs_p.png")


if __name__ == "__main__":
    main()
