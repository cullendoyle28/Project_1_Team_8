# Planning and Analysis

## Problem Formulation

The objective of the Mentor Pairing problem is to efficiently maximize the number of pairs of students between incoming students, each with their own programming experience score, and seniors, each with their own programming experience score.

## Baseline Solution

## Algorithmic Strategy

We propose a greedy algorithm using sorting and two pointers to maximize the number of valid mentor pairings.

The key idea is to match the incoming student with the lowest remaining experience score to the senior student with the lowest remaining score who can mentor that student. By doing so, we preserve more experienced senior students for incoming students who may require them.

First, we sort both lists of experience scores in ascending order. We then initialize two pointers, `i` and `j`, at the beginning of the sorted senior and incoming lists, respectively. We also initialize `matches` to zero.

At each iteration, we compare the experience scores of the students at the two pointers:

1. **If `Senior[i] > Incoming[j]`:** We form a valid pair, increment `matches`, and advance both pointers. Both students have been assigned and cannot be paired again.
2. **Otherwise:** We advance only `i`. Because `Incoming[j]` has the lowest experience score among all remaining incoming students, `Senior[i]` cannot mentor that student or any other remaining incoming student. Therefore, skipping this senior student cannot reduce the maximum possible number of matches.

We repeat this process until either pointer reaches the end of its list. At that point, no additional valid pairs can be formed, and the algorithm returns `matches`.

## Complexity Analysis
