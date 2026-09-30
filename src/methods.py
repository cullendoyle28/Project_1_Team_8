# methods.py
# Implements baseline and proposed solutions for the Mentor Pairing problem.

def MentorPairingBruteForce(senior, incoming):

    n=len(senior)
    k=len(incoming)

    used = [False]*n

    def Search(i, used):
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


