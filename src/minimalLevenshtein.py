import itertools

def levenshtein_words(s1, s2):
    w1 = s1.split()
    w2 = s2.split()
    
    dp = [[0] * (len(w2) + 1) for _ in range(len(w1) + 1)]

    for i in range(len(w1) + 1):
        for j in range(len(w2) + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif w1[i-1] == w2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[-1][-1]

def total_distance(order):
    return sum(levenshtein_words(order[i], order[i+1]) for i in range(len(order)-1))

def find_best_order(sentences):
    best_order = None
    min_distance = float('inf')

    for perm in itertools.permutations(sentences):
        dist = total_distance(perm)
        if dist < min_distance:
            min_distance = dist
            best_order = perm

    return best_order, min_distance

# Beispiel-Sätze (in zufälliger Reihenfolge):
sentences = [
    "Der Hund läuft schnell",
    "Der schwarze Hund läuft schnell",
    "Ein schwarzer Hund läuft schnell",
    "Ein schwarzer Hund läuft sehr schnell",
    "Ein großer schwarzer Hund läuft sehr schnell",
    "Ein großer schwarzer Hund läuft sehr schnell durch den Park",
    "Ein großer schwarzer Hund rennt sehr schnell durch den Park",
    "Ein großer schwarzer Hund rennt blitzschnell durch den Park",
    "Ein großer schwarzer Hund rennt blitzschnell durch den grünen Park",
    "Ein großer schwarzer Hund rennt blitzschnell durch einen grünen Park"
]

best_order, min_dist = find_best_order(sentences)
print("Minimale Gesamtdistanz:", min_dist)
print("Rekonstruierte Reihenfolge:")
for i, s in enumerate(best_order):
    print(f"{i+1}. {s}")
