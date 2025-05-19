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

def build_distance_cache(sentences):
    cache = {}
    for i, s1 in enumerate(sentences):
        for j, s2 in enumerate(sentences):
            if i < j:
                dist = levenshtein_words(s1, s2)
                cache[(i, j)] = dist
                cache[(j, i)] = dist  # symmetrisch
            elif i == j:
                cache[(i, j)] = 0
    return cache

def total_distance(order_indices, cache):
    return sum(cache[(order_indices[i], order_indices[i+1])] for i in range(len(order_indices) - 1))

def find_best_order(sentences):
    n = len(sentences)
    cache = build_distance_cache(sentences)

    best_order = None
    min_distance = float('inf')

    for perm in itertools.permutations(range(n)):
        dist = total_distance(perm, cache)
        if dist < min_distance:
            min_distance = dist
            best_order = perm

    return [sentences[i] for i in best_order], min_distance

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
