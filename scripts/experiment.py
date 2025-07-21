"""
experiment.py

Runs ≥100 trials of the PPSP simulation per steal probability
(p ∈ {0.0, 0.1, ..., 1.0}) and writes trial-level plus summary
results to results.csv.
"""

import csv
from typing import List

import numpy as np

from simulator.simulator import run_one


def main() -> None:
    output_file = "results.csv"
    trials_per_p = 100
    probabilities = np.linspace(0.0, 1.0, 11)

    trial_headers = ["steal_prob", "trial", "delivered", "hop_count"]
    summary_headers = ["steal_prob", "success_rate", "avg_hops", "std_hops"]

    trial_rows: List[List] = []
    summary_rows: List[List] = []

    np.random.seed(0)

    for p in probabilities:
        success_list: List[bool] = []
        hop_list: List[int] = []

        print(f"Running {trials_per_p} trials for steal_prob = {p:.1f}")
        for t in range(trials_per_p):
            delivered, hops = run_one(p)
            trial_rows.append([p, t, delivered, hops])
            success_list.append(delivered)
            hop_list.append(hops)

        success_rate = np.mean(success_list)
        avg_hops = np.mean(hop_list)
        std_hops = np.std(hop_list, ddof=1)

        summary_rows.append([p, success_rate, avg_hops, std_hops])

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(trial_headers)
        writer.writerows(trial_rows)

        writer.writerow([])

        writer.writerow(summary_headers)
        writer.writerows(summary_rows)

    print(f"\nResults written to {output_file}")


if __name__ == "__main__":
    main()
