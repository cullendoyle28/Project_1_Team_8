# Empirical Evaluation

## Overview

We implemented our three algorithms (`methods.py`) that solve the Mentor Pairing problem:

1. **Brute Force Algorithm:** A naive approach that exhaustively explores all possible matching decisions for every incoming student.
2. **Baseline Algorithm:** A less naive approach that sorts the students, creates a matrix that stores every possible pair, and then scans the matrix row by row with a column pointer that only moves forward.
3. **Greedy Algorithm:** An efficient greedy approach that sorts the students from least to most experience, then matches them by shifting the forward moving column/row pointers if a student is matched.

Unit testing (`tests.py`) confirms that the algorithms return the correct maximum pair count across multiple typical and edge cases (empty lists, ties, etc.).

## Benchmarking Results

We compare the performance of our three algorithms on randomly generated arrays with max_score = 1000 (`benchmark.py`), varying input size (n) from 2 to 100,000 students per list. We present the results in the plots below. The left plot shows the execution time on a linear scale. In this plot, once the input size reaches 9 students per list, it takes about 2 seconds for the brute force algorithm to execute. The right plot uses a logarithmic scale for the y axis. The reason for this is to make the graph more readable, as it is impossible to tell where the baseline algorithm is. After switching to a logarithmic scale for the y axis (shown in the right plot), notice that the baseline algorithm is slower than the greedy algorithm because the entirety of the baseline algorithm's line segments, from 2 through 9 students per list, is above the greedy algorithm's line segments.

| ![Comparison Plot (Linear Scale)](assets/comparison_plot.png) | ![Comparison Plot (Log Scale)](assets/comparison_plot_log.png) |
| ------------------------------------------------------------- | -------------------------------------------------------------- |

Next, we compare the performance of the Baseline Algorithm and Greedy Algorithm for more clarity on which one is better at much higher input sizes. The left plot shows the execution time on a linear scale while the right plot uses a logarithmic scale for both axes. Again, we changed to a logarithmic scale to show the difference in execution time more distinctly (shown in the right plot). This shows no clear overlap between the line segments.

| ![Scalability Plot (Linear Scale)](assets/scalability_plot.png) | ![Scalability Plot (Log Scale)](assets/scalability_plot_log.png) |
| --------------------------------------------------------------- | ---------------------------------------------------------------- |

The empirical data aligns with our theoretical complexity analysis (`planning.md`):

- **Brute Force Exponential Scaling**: The brute force algorithm theoretically scales at $\mathcal{O}((n+1)^n)$ due to exhaustively exploring the possible matching decisions for every incoming student.
- **Baseline Quadratic Scaling**: The baseline algorithm theoretically scales at $\mathcal{O}(n^2)$ due to constructing a $k$ by $n$ matrix containing every possible incoming-senior pair. At $n = 9$, the baseline algorithm is unbelievably faster than the brute force algorithm. The baseline algorithm is almost **1,000,000 times faster**, which shows that efficiently organizing data (sorting) before processing drastically outperforms naive continuous searching.
- **Greedy Algorithm Efficiency**: The greedy algorithm scales at $\mathcal{O}(n \log n)$, constrained almost entirely by Python's built-in sorting algorithm. At $n = 3,000$, the greedy algorithm is several orders of magnitude faster than the baseline algorithm. In particular, the greedy algorithm is approximately **800 times faster**.
