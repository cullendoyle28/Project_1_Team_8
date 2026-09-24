# Planning and Analysis

## Problem Formulation

The objective of the Mentor Pairing problem is to efficiently pair two students based on experience, maximizing the total number of pairs. We are provided with a list of senior students of size $n$ denoted as $Seniors = [i_1, i_2, \dots, i_n]$ and another list of incoming students of size $k$ denoted as $Incoming = [j_1, j_2, \dots, j_n]$, with each list containing their programming experience scores. Each student can only be paired one time. Our goal is to design an algorithm that determines the absolute maximum number of mentor pairings of senior and incoming students, scaling efficiently even when the lists of students are very large. 

## Baseline Solution

## Algorithmic Strategy

We propose a greedy algorithm using sorting and two pointers to maximize the number of valid mentor pairings.
The key idea is to match the incoming student with the lowest remaining experience score to the senior student with the lowest remaining score who can mentor that student. By doing so, we preserve more experienced senior students for incoming students who may require them.

First, we sort both lists of experience scores in ascending order. We then initialize two pointers, `i` and `j`, at the beginning of the sorted senior and incoming lists, respectively. We also initialize `matches` to zero.

At each iteration, we compare the experience scores of the students at the two pointers:

1. **If `Senior[i] > Incoming[j]`:** We form a valid pair, increment `matches`, and advance both pointers. Both students have been assigned and cannot be paired again.
2. **Otherwise:** We advance only `i`. Because `Incoming[j]` has the lowest experience score among all remaining incoming students, `Senior[i]` cannot mentor that student or any other remaining incoming student. Therefore, skipping this senior student cannot reduce the maximum possible number of matches.

We repeat this process until either pointer reaches the end of its list. At that point, no additional valid pairs can be formed, and the algorithm returns `matches`.

### Pseudocode

```text
Algorithm MentorPairingGreedy(Senior, Incoming):

    Input:
        Senior: A list of n senior students' experience scores
        Incoming: A list of k incoming students' experience scores

    Output:
        Maximum number of valid mentor pairings

    Sort Senior in ascending order
    Sort Incoming in ascending order

    i = 0
    j = 0
    matches = 0

    while i < n and j < k:

        if Senior[i] > Incoming[j]:

            matches = matches + 1

            i = i + 1
            j = j + 1

        else:

            i = i + 1

    return matches
```

### Correctness and Optimality

We prove that the greedy algorithm always produces the maximum number of valid pairings.

Let `s` and `a` be the lowest-scoring remaining senior and incoming students, respectively.

**Case 1: `s <= a`**

Since `a` has the lowest score among the remaining incoming students, `s` cannot mentor any of them. Therefore, skipping `s` cannot reduce the maximum number of matches.

**Case 2: `s > a`**

The algorithm pairs `s` with `a`. We show that this choice is consistent with an optimal matching.

Consider any optimal matching:

- If `s` and `a` are already paired, no change is needed.
- If only one is matched, replacing that student's existing pair with `(s, a)` preserves the number of matches.
- If neither is matched, adding `(s, a)` would contradict optimality.
- If both are matched to different students, suppose the original pairs are `(s, a')` and `(s', a)`. We can replace them with `(s, a)` and `(s', a')`. Both new pairs are valid because `s > a` and `s' >= s > a'`.

Thus, an optimal matching containing the greedy pair always exists.

**Conclusion**

In both cases, the greedy decision preserves the maximum achievable number of matches. Applying this reasoning repeatedly to the remaining students proves that the algorithm returns the maximum possible number of valid pairings.

## Complexity Analysis
