

































def MentorPairingGreedy(Senior: list, Incoming: list)-> int:
    Senior.sort()
    Incoming.sort()

    i = 0
    j = 0
    match = 0

    while j < len(Senior) and i < len(Incoming):
        if Senior[j] > Incoming[i]:
            match = match + 1

            i = i + 1
            j = j + 1

        else:

            j = j + 1

    return match