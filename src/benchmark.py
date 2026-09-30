# benchmark.py
# Empirically measures the execution time of the mentor pairing algorithms.

from time import perf_counter
import random
import pandas as pd

from methods import MentorPairingBruteForce, MentorPairingGreedy


def generate_test_data(size, max_score):
    """
    Generates random experience scores for senior and incoming students.

    Args:
        size (int): Number of senior and incoming students.
        max_score (int): Maximum possible experience score.

    Returns:
        tuple: Two lists containing senior and incoming experience scores.
    """
    senior = [random.randint(1, max_score) for _ in range(size)]
    incoming = [random.randint(1, max_score) for _ in range(size)]

    return senior, incoming


def benchmark_algo_multi(algo, test_cases, repeat=1):
    """
    Measures the execution time of an algorithm over multiple test cases.

    Args:
        algo (function): The mentor pairing algorithm to benchmark.
        test_cases (list): List of senior and incoming student test cases.
        repeat (int): Number of times to repeat each test case.

    Returns:
        list: Tuples containing input size and execution time.
    """
    times = []

    for senior, incoming in test_cases:
        for _ in range(repeat):
            senior_copy = senior.copy()
            incoming_copy = incoming.copy()

            start = perf_counter()
            algo(senior_copy, incoming_copy)
            end = perf_counter()

            times.append((len(senior), end - start))

    return times


def run_benchmarks():
    """
    Runs benchmarks for the brute-force and greedy mentor pairing algorithms
    and saves the results to a CSV file.
    """
    input_sizes = [2, 4, 6, 8, 10]
    max_score = 100
    repeat = 5

    test_cases = [
        generate_test_data(size, max_score)
        for size in input_sizes
    ]

    brute_force_times = benchmark_algo_multi(
        MentorPairingBruteForce,
        test_cases,
        repeat=repeat
    )

    greedy_times = benchmark_algo_multi(
        MentorPairingGreedy,
        test_cases,
        repeat=repeat
    )

    df_brute_force = pd.DataFrame(
        brute_force_times,
        columns=["Students", "Time"]
    )
    df_brute_force["Algorithm"] = "Brute Force"

    df_greedy = pd.DataFrame(
        greedy_times,
        columns=["Students", "Time"]
    )
    df_greedy["Algorithm"] = "Greedy"

    df_all = pd.concat(
        [df_brute_force, df_greedy],
        ignore_index=True
    )

    df_all.to_csv("empirical_results.csv", index=False)

    print("All Times:")
    print(df_all)


if __name__ == "__main__":
    run_benchmarks()