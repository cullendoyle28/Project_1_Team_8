# methods.py
# Implements baseline and proposed solutions for the Mentor Pairing problem.

def MentorPairingBaseline(senior: list, incoming: list) -> int:
    """
    Find the maximum number of valid mentor pairings using an all-pairs matrix.
 
    A pairing is valid when a senior student's experience score is greater
    than the experience score of the incoming student. Each student can be
    included in at most one pairing.
 
    This function sorts both lists, builds a k x n matrix that stores every
    possible (incoming score, senior score) pair, and then scans the matrix
    row by row with a column pointer that only moves forward. Building the
    matrix dominates the running time and space: O(nk).
 
    Args:
        senior (list): A list of senior students' experience scores.
        incoming (list): A list of incoming students' experience scores.
 
    Returns:
        int: The maximum number of valid mentor pairings.
    """
 
    senior = sorted(senior)
    incoming = sorted(incoming)
 
    n = len(senior)
    k = len(incoming)
 
    matches = 0
 
    # Build the k x n matrix of all (incoming, senior) pairs: O(nk)
    allpairs = []
 
    for i in range(k):
        row = []
        for j in range(n):
            row.append((incoming[i], senior[j]))
        allpairs.append(row)
 
    # The column pointer only moves forward, so each senior is checked once
    column = 0
 
    for i in range(k):
        row_to_check = allpairs[i]
        while column < n:
            pair = row_to_check[column]
            if pair[0] < pair[1]:
                # Valid pair: use this senior and move to the next row
                matches += 1
                column += 1
                break
            else:
                # This senior cannot mentor anyone remaining: skip
                column += 1
 
    return matches

def MentorPairingBruteForce(senior, incoming):
    """
    Find the maximum number of valid mentor pairings using brute force.

    A pairing is valid when a senior student's experience score is greater
    than the experience score of the incoming student. Each senior student
    can be paired with at most one incoming student.

    This function uses recursive backtracking to explore all possible valid
    pairings, including the option of leaving an incoming student unmatched.

    Args:
        senior (list): A list of senior students' experience scores.
        incoming (list): A list of incoming students' experience scores.

    Returns:
        int: The maximum number of valid mentor pairings.
    """

    n=len(senior)
    k=len(incoming)

    used = [False]*n

    def Search(i, used):
        """
        Recursively search for the maximum number of matches.

        Args:
            i (int): The index of the current incoming student.
            used (list): Boolean list indicating which seniors are already used.

        Returns:
            int: The maximum number of additional valid pairings.
        """
        if i == k:
            return 0

        best = Search(i+1, used)

        for j in range(0,n):
            if used[j] == False and senior[j] > incoming[i]:
                used[j] = True
                matches = 1 + Search(i+1, used)
                best = max(best, matches)
                used[j] = False
        return best

    return Search(0, used)

def MentorPairingGreedy(senior: list, incoming: list) -> int:
    """
    Find the maximum number of valid mentor pairings using a greedy algorithm.

    A pairing is valid when a senior student's experience score is greater
    than the experience score of the incoming student. Each student can be
    included in at most one pairing.

    Args:
        senior (list): A list of senior students' experience scores.
        incoming (list): A list of incoming students' experience scores.

    Returns:
        int: The maximum number of valid mentor pairings.
    """

    senior = sorted(senior)
    incoming = sorted(incoming)

    i = 0
    j = 0
    matches = 0

    while i < len(incoming) and j < len(senior):
        if senior[j] > incoming[i]:
            matches += 1
            i += 1
            j += 1
        else:
            j += 1

    return matches
