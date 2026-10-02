# tests.py
# Unit tests verifying the correctness of the mentor pairing algorithms.

import random
import unittest

from methods import (
    MentorPairingBaseline,
    MentorPairingBruteForce,
    MentorPairingGreedy
)


class TestMentorPairingAlgorithms(unittest.TestCase):
    def setUp(self):
        # Format: (senior_list, incoming_list, expected_pair_count)
        self.test_cases = [
            ([4, 5, 6], [1, 2, 3], 3),        # Every senior can mentor
            ([6, 10], [4, 7], 2),             # Lowest valid senior must be used first
            ([10, 6], [7, 4], 2),             # Same scores, unsorted input
            ([5, 1, 9, 3], [4, 8, 2, 6], 3),  # General mixed scores
            ([1, 2, 3], [4, 5, 6], 0),        # No senior can mentor anyone
            ([5, 5, 5], [5, 5, 5], 0),        # Equal scores are not valid pairs
            ([7, 7, 7], [3, 6, 7], 2),        # Duplicate scores
            ([10], [1, 2, 3], 1),             # Fewer seniors than incoming students
            ([3, 8, 9, 2], [7], 1),           # More seniors than incoming students
            ([5], [4], 1),                    # Single valid pair
            ([5], [5], 0),                    # Single pair with a tie
            ([], [], 0),                      # Both lists empty
            ([], [1, 2], 0),                  # No seniors
            ([1, 2], [], 0)                   # No incoming students
        ]

    def check_correctness(self, algorithm):
        for senior, incoming, expected in self.test_cases:
            with self.subTest(senior=senior, incoming=incoming):
                self.assertEqual(algorithm(senior, incoming), expected)

    def test_baseline_correctness(self):
        self.check_correctness(MentorPairingBaseline)

    def test_brute_force_correctness(self):
        self.check_correctness(MentorPairingBruteForce)

    def test_greedy_correctness(self):
        self.check_correctness(MentorPairingGreedy)

    def test_algorithms_agree_on_random_inputs(self):
        # Brute force tries every possible matching, so it is used as the
        # reference answer for the other two algorithms on small inputs.
        rng = random.Random(202)

        for _ in range(200):
            senior = [rng.randint(1, 10) for _ in range(rng.randint(0, 6))]
            incoming = [rng.randint(1, 10) for _ in range(rng.randint(0, 6))]
            expected = MentorPairingBruteForce(senior, incoming)

            with self.subTest(senior=senior, incoming=incoming):
                self.assertEqual(MentorPairingBaseline(senior, incoming), expected)
                self.assertEqual(MentorPairingGreedy(senior, incoming), expected)

    def test_inputs_are_not_modified(self):
        # benchmark.py passes the same lists to every algorithm and trial,
        # so no algorithm may sort or change its inputs in place.
        algorithms = [
            MentorPairingBaseline,
            MentorPairingBruteForce,
            MentorPairingGreedy
        ]

        for algorithm in algorithms:
            senior = [9, 2, 7]
            incoming = [8, 1, 5]

            with self.subTest(algorithm=algorithm.__name__):
                algorithm(senior, incoming)
                self.assertEqual(senior, [9, 2, 7])
                self.assertEqual(incoming, [8, 1, 5])


if __name__ == "__main__":
    unittest.main()