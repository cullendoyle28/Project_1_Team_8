# Planning and Analysis

## Problem Formulation

The objective of the Mentor Pairing problem is to efficiently pair two students based on experience, maximizing the total number of pairs. We are provided with a list of senior students of size $n$ denoted as $Senior = [i_1, i_2, \dots, i_n]$ and another list of incoming students of size $k$ denoted as $Incoming = [j_1, j_2, \dots, j_k]$, with each list containing their programming experience scores. Each student can only be paired one time, and a senior student can only be paired with an incoming student if the senior student has a greater programming experience score than the incoming student. Our goal is to design an algorithm that determines the absolute maximum number of mentor pairings of senior and incoming students, scaling efficiently even when the lists of students are very large. 

## Baseline Solution
We took a simple approach for our baseline solution: enumerate every possible combination and find the maximum number of valid pairings. First, we sort both lists. Then our algorithm constructs a k x n matrix (k = number of incoming students, n = number of seniors), where each entry is a tuple of (incoming score, senior score). Across each row, the incoming score is fixed with senior scores ascending left to right. Down each column, the senior score is fixed with incoming scores descending top to bottom. For example:
```
Senior = [4,5,6]
Incoming = [1,2,3]


                    |(1,4) (1,5) (1,6)|
All Pairs Matrix =  |(2,4) (2,5) (2,6)|
                    |(3,4) (3,5) (3,6)|
```
The algorithm then iterates through each row, comparing scores in each tuple. If the senior's score is greater than the incoming student's, it records the match and moves to the next row. Otherwise, it keeps checking entries until it finds one.

To avoid duplicate pairings, we track a column counter that increases with each match, so the same senior is never checked twice. For example, if the first match is found in the second column of row one, the next row starts checking from the third column.

We sort the lists beforehand to maximize the number of matches. Ideally, each student should pair with the senior closest to their score. For instance, if an incoming student scores 4 and two seniors score 6 and 10, that student should pair with the 6. If a later student scores 7, they can then pair with the 10. If the 4 had taken the 10 instead, the 7 would be left unmatched, costing us a match. Working through the sorted matrix from lowest to highest ensures this doesn't happen.
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

We find that the greedy algorithm provides a significant improvement in the running time compared to the baseline solution. The baseline algorithm constructs a matrix containing every possible incoming and senior student pairing, requiring $\mathcal{O}(nk)$ running time to create and search through the possible pairs. 

Specifically, we have $\mathcal{T}(n, k)$ = $\mathcal n \log n + k \log k + nk + n + k + 1$ after dropping constants.
Then, using the sum is max property, we have:
$\mathcal n \log n + k \log k + nk + n + k + 1$ is $\mathcal{O}(nk)$,
since $\mathcal nk$ dominates $\mathcal n \log n$, $\mathcal k \log k$, and $\mathcal n+k$ as $n$ and $k$ grow large.

But, our proposed greedy strategy is more efficient. The first step is sorting both the senior and incoming student lists which take $\mathcal{O}(n \log n)$ and $\mathcal{O}(k \log k)$ running time, respectively, when using an efficient sorting algorithm such as Merge Sort.
After sorting, the algorithm uses two pointers to examine the lists. Each pointer only moves forward and never backward so the two pointer portion takes $\mathcal{O}(n + k)$ running time. Therefore, the running time of the greedy algorithm, after dropping constants (and operations requiring $\mathcal{O}(1)$ running time) and then using the sum is max property, is $\mathcal{O}(n \log n + k \log k)$, with the sorting step being the dominant operation.

The greedy algorithm requires just $\mathcal{O}(n + k)$ additional space beyond the input lists if the sorting algorithm is performed in place. This is a significant improvement over the baseline's $\mathcal{O}(nk)$ space requirement for storing the matrix of all possible pairs.
