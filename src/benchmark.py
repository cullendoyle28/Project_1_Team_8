# benchmark.py
# Empirically measures the execution time of the mentor pairing algorithms.

from pathlib import Path
from time import perf_counter
import random
import pandas as pd

from methods import (
    MentorPairingBaseline,
    MentorPairingBruteForce,
    MentorPairingGreedy
)

# The matrix baseline stores every (incoming, senior) pair, so its memory
# use grows quadratically (roughly 600 MB at n = 3000). Larger inputs in
# Experiment 2 are skipped for this algorithm.
MAX_BASELINE_SIZE = 3000

# Generated files (the CSV and the plots) are stored in the assets folder
# at the root of the repository, next to src.
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def generate_test_data(size, max_score=1000):
    """
    Generates random senior and incoming experience scores.

    Incoming students receive scores from the lower half of the range,
    while senior students receive scores from the upper half.
    This creates many valid pairings and gives the brute-force algorithm
    a consistently difficult input.
    """
    incoming = [
        random.randint(1, max_score // 2)
        for _ in range(size)
    ]

    senior = [
        random.randint(max_score // 2 + 1, max_score)
        for _ in range(size)
    ]

    return senior, incoming


def benchmark_algo_multi(algo, test_cases, repeat=5):
    times = []

    for senior, incoming in test_cases:
        for trial in range(1, repeat + 1):
            start = perf_counter()
            algo(senior, incoming)
            end = perf_counter()

            times.append(
                (len(senior), end - start, trial)
            )

    return times


def run_benchmarks():
    random.seed(42)

    # Experiment 1:
    # Compare all three algorithms on small inputs.
    comparison_sizes = [2, 3, 4, 5, 6, 7, 8, 9]

    comparison_cases = [
        generate_test_data(size)
        for size in comparison_sizes
    ]

    brute_force_times = benchmark_algo_multi(
        MentorPairingBruteForce,
        comparison_cases,
        repeat=5
    )

    baseline_comparison_times = benchmark_algo_multi(
        MentorPairingBaseline,
        comparison_cases,
        repeat=5
    )

    greedy_comparison_times = benchmark_algo_multi(
        MentorPairingGreedy,
        comparison_cases,
        repeat=5
    )

    df_brute = pd.DataFrame(
        brute_force_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_brute["Algorithm"] = "Brute Force"
    df_brute["Experiment"] = "Comparison"

    df_baseline_comparison = pd.DataFrame(
        baseline_comparison_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_baseline_comparison["Algorithm"] = "Matrix Baseline"
    df_baseline_comparison["Experiment"] = "Comparison"

    df_greedy_comparison = pd.DataFrame(
        greedy_comparison_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_greedy_comparison["Algorithm"] = "Greedy"
    df_greedy_comparison["Experiment"] = "Comparison"

    # Experiment 2:
    # Measure matrix baseline and greedy scalability on much larger inputs.
    # The matrix baseline only runs on sizes up to MAX_BASELINE_SIZE.
    greedy_sizes = [
        100,
        500,
        1000,
        2000,
        3000,
        5000,
        10000,
        20000,
        50000,
        100000
    ]

    greedy_cases = [
        generate_test_data(size)
        for size in greedy_sizes
    ]

    baseline_cases = [
        (senior, incoming)
        for senior, incoming in greedy_cases
        if len(senior) <= MAX_BASELINE_SIZE
    ]

    baseline_scalability_times = benchmark_algo_multi(
        MentorPairingBaseline,
        baseline_cases,
        repeat=5
    )

    greedy_scalability_times = benchmark_algo_multi(
        MentorPairingGreedy,
        greedy_cases,
        repeat=5
    )

    df_baseline_scalability = pd.DataFrame(
        baseline_scalability_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_baseline_scalability["Algorithm"] = "Matrix Baseline"
    df_baseline_scalability["Experiment"] = "Scalability"

    df_greedy_scalability = pd.DataFrame(
        greedy_scalability_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_greedy_scalability["Algorithm"] = "Greedy"
    df_greedy_scalability["Experiment"] = "Scalability"

    # Combine all results.
    df_all = pd.concat(
        [
            df_brute,
            df_baseline_comparison,
            df_greedy_comparison,
            df_baseline_scalability,
            df_greedy_scalability
        ],
        ignore_index=True
    )

    ASSETS_DIR.mkdir(exist_ok=True)
    df_all.to_csv(ASSETS_DIR / "empirical_results.csv", index=False)

    print("All Times:")
    print(df_all)


if __name__ == "__main__":
    run_benchmarks()