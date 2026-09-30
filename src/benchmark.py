# benchmark.py
# Empirically measures the execution time of the mentor pairing algorithms.

from time import perf_counter
import random
import pandas as pd

from methods import MentorPairingBruteForce, MentorPairingGreedy


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
    # Compare brute force and greedy on small inputs.
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

    df_greedy_comparison = pd.DataFrame(
        greedy_comparison_times,
        columns=["InputSize", "Time", "Trial"]
    )
    df_greedy_comparison["Algorithm"] = "Greedy"
    df_greedy_comparison["Experiment"] = "Comparison"

    # Experiment 2:
    # Measure greedy scalability on much larger inputs.
    greedy_sizes = [
        100,
        500,
        1000,
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

    greedy_scalability_times = benchmark_algo_multi(
        MentorPairingGreedy,
        greedy_cases,
        repeat=5
    )

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
            df_greedy_comparison,
            df_greedy_scalability
        ],
        ignore_index=True
    )

    df_all.to_csv("empirical_results.csv", index=False)

    print("All Times:")
    print(df_all)


if __name__ == "__main__":
    run_benchmarks()