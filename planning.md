# Planning and Analysis

## Problem Formulation

The objective of the Mentor Pairing problem is to efficiently pair two students based on experience, maximizing the total number of pairs. We are provided with a list of senior students of size $n$ denoted as $Senior = [i_1, i_2, \dots, i_n]$ and another list of incoming students of size $k$ denoted as $Incoming = [j_1, j_2, \dots, j_k]$, with each list containing their programming experience scores. Each student can only be paired one time, and a senior student can only be paired with an incoming student if the senior student has a greater programming experience score than the incoming student. Our goal is to design an algorithm that determines the absolute maximum number of mentor pairings of senior and incoming students, scaling efficiently even when the lists of students are very large.

## Baseline Solution 1

We took a simple approach for our baseline solution: construct every possible incoming-senior pair and systematically select valid pairings. First, we sort both lists. Then our algorithm constructs a k x n matrix (k = number of incoming students, n = number of seniors), where each entry is a tuple of (incoming score, senior score). Across each row, the incoming score is fixed with senior scores ascending left to right. Down each column, the senior score is fixed with incoming scores ascending top to bottom. For example:

```
Senior = [4,5,6]
Incoming = [1,2,3]


                    |(1,4) (1,5) (1,6)|
All Pairs Matrix =  |(2,4) (2,5) (2,6)|
                    |(3,4) (3,5) (3,6)|
```

The algorithm then iterates through each row, comparing scores in each tuple. If the senior's score is greater than the incoming student's, it records the match and moves to the next row. Otherwise, it keeps checking entries until it finds one.

To avoid duplicate pairings and repeated comparisons, we track a column pointer that only moves forward through the senior students. The pointer advances whenever a senior is either used in a valid match or determined to be unable to mentor the current incoming student. Therefore, each senior student is considered at most once. For example, if the first match is found in the second column of the first row, the next row begins checking from the third column because the senior in the second column has already been assigned.

We sort both lists beforehand so that students can be processed from the lowest experience scores to the highest. This allows the algorithm to select the lowest-scoring available senior who can mentor each incoming student. Specifically, each incoming student is paired with the lowest-scoring available senior whose score is strictly greater than the incoming student's score. For instance, if an incoming student scores 4 and two seniors score 6 and 10, that student should pair with the 6. If a later student scores 7, they can then pair with the 10. If the 4 had taken the 10 instead, the 7 would be left unmatched, costing us a match. Because both lists are sorted in ascending order, if a senior cannot mentor the current incoming student, that senior cannot mentor any later incoming student either. Every later incoming student has an experience score greater than or equal to the current student's score. Therefore, permanently skipping such a senior cannot reduce the maximum possible number of matches.

When a valid senior is found, the algorithm selects the lowest-scoring available senior who can mentor the current incoming student. This preserves all higher-scoring seniors for later incoming students who may require a more experienced mentor. Therefore, these decisions do not reduce the maximum achievable number of pairings.

Although this baseline explicitly constructs a matrix containing every possible incoming-senior pair, its matching process effectively behaves like a two-pointer greedy strategy. The row index progresses through the incoming students, while the column variable only moves forward through the senior students. The main inefficiency of this baseline is therefore the unnecessary construction and storage of the full matrix.

### Pseudocode

```text
Algorithm MentorPairingBaseline(Senior, Incoming):

    Input:
        Senior: A list of n senior students' experience scores
        Incoming: A list of k incoming students' experience scores

    Output:
        Maximum number of valid mentor pairings

    Sort Senior in ascending order
    Sort Incoming in ascending order

    matches = 0

    allpairs = []

    for i from 0 to k-1:
        row = []
        for j from 0 to n-1:
            append (Incoming[i],Senior[j]) to row
        append row to allpairs

    column = 0

    for i from 0 to k-1:
        row_to_check = allpairs[i]
        while column < n:
            pair = row_to_check[column]
            if pair[0] < pair[1]:
                matches += 1
                column += 1
                break
            else:
                column += 1

    return matches
```

### Correctness of Baseline Solution 1

Because both lists are sorted, any senior who cannot mentor the current lowest-scoring incoming student cannot mentor any later incoming student either. Therefore, skipping that senior cannot reduce the maximum number of matches. When a valid senior is found, selecting the lowest-scoring available senior preserves all higher-scoring seniors for later incoming students. Repeating these decisions therefore produces the maximum possible number of valid pairings.

## Baseline Solution 2

For our baseline solution, we use an exhaustive brute-force search. The purpose of this approach is to guarantee that we find the maximum possible number of valid mentor pairings, even though the algorithm is inefficient for large inputs.

For each incoming student, the algorithm considers every possible decision. The student may remain unmatched, or they may be paired with any currently unused senior student whose experience score is strictly greater than their score. After making one of these choices, the algorithm recursively considers the next incoming student.

A boolean array, `used`, keeps track of which senior students have already been assigned to a pair. Whenever the algorithm temporarily pairs an incoming student with a senior student, that senior is marked as used before the recursive call and marked as unused afterward. This allows the algorithm to explore every possible matching without assigning the same senior student more than once.

At each recursive call, the algorithm keeps the maximum number of matches obtained from all possible choices.

### Pseudocode

```text
Algorithm MentorPairingBruteForce(Senior, Incoming):

    Input:
        Senior: A list of n senior students' experience scores
        Incoming: A list of n incoming students' experience scores

    Output:
        Maximum number of valid mentor pairings

    used = boolean array of size n, initialized to false

    return Search(0, used)


Function Search(i, used):

    if i == n:
        return 0

    // Option 1: Leave this incoming student unmatched
    best = Search(i + 1, used)

    // Option 2: Pair this incoming student with
    // each valid unused senior
    for j from 0 to n - 1:

        if used[j] == false AND Senior[j] > Incoming[i]:

            used[j] = true

            matches = 1 + Search(i + 1, used)

            best = max(best, matches)

            used[j] = false

    return best
```

### Correctness of the Baseline 2

The brute-force algorithm returns the maximum possible number of valid mentor pairings because it considers every possible valid decision for every incoming student.

For each incoming student, the algorithm explores the possibility of leaving that student unmatched as well as pairing that student with every valid senior student who has not already been used. Therefore, every valid matching between the incoming and senior students corresponds to at least one path through the recursion tree.

Since the algorithm computes the number of matches produced by every possible valid matching and returns the maximum of those values, it must return the maximum possible number of mentor pairings.

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

We find that the proposed greedy algorithm provides a significant improvement in running time compared to both baseline solutions.

For Baseline Solution 1, the algorithm first sorts the senior and incoming student lists, requiring $O(n \log n)$ and $O(k \log k)$ time, respectively. It then constructs a $k \times n$ matrix containing every possible incoming-senior pair. Constructing this matrix requires $O(nk)$ time. After the matrix is constructed, the algorithm scans it using the row index and a column pointer. Because the column pointer only moves forward and never moves backward, each senior student is considered at most once during this scanning process. Therefore, the scan requires $O(n+k)$ time.

Thus, the total running time of Baseline Solution 1 is $T(n,k) = O(n \log n + k \log k + nk + n + k)$.

Since the problem allows us to assume that the two lists have the same length, we can let $n=k$. The running time then becomes $O(n \log n + n^2 + n)$. Using the sum-is-max property, the $n^2$ term dominates. Therefore, the overall running time of Baseline Solution 1 is $O(n^2)$.

For Baseline Solution 2, the brute-force algorithm exhaustively explores the possible matching decisions for every incoming student. For each incoming student, the algorithm may leave the student unmatched or attempt to pair the student with one of the available senior students. With lists of equal size $n$, a simple upper bound gives at most $n+1$ possible choices at each of $n$ recursive levels. This gives $O((n+1)^n)$ possible paths in the recursion tree. In addition, each recursive call may scan up to $n$ senior students. Therefore, a simple worst-case upper bound on the running time is $O(n(n+1)^n)$.

This exponential growth makes the brute-force baseline impractical for large inputs, even though it guarantees that every possible valid matching is considered.

Our proposed greedy algorithm is significantly more efficient. First, the senior and incoming student lists are sorted, requiring $O(n \log n)$ and $O(k \log k)$ time. After sorting, the algorithm uses two pointers to examine the lists. Each pointer only moves forward and never backward, so the two-pointer portion requires $O(n+k)$ time.

Therefore, the total running time is $T(n,k) = O(n \log n + k \log k + n + k)$.

Since the two lists may be assumed to have the same length, this simplifies to $O(n \log n + n)$. The sorting step dominates, so the overall running time of the proposed greedy algorithm is $O(n \log n)$.

The space requirements also differ significantly. Baseline Solution 1 requires $O(nk)$, or $O(n^2)$ when the lists have equal length, to store the matrix of all possible pairs. Baseline Solution 2 requires an $O(n)$ used array and $O(n)$ recursion depth, giving $O(n)$ auxiliary space. Aside from the space required by the sorting algorithm, the proposed greedy algorithm uses only $O(1)$ additional space for its two pointers and match counter. If Merge Sort is used, the sorting process itself requires $O(n)$ auxiliary space.
