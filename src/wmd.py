#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Word Mover’s Distance zwischen drei Sätzen
Visualisierungen in einem 2×2-Grid:
  • Heatmap Wort–Wort-Distanzen (Satz 1 vs. Satz 2)
  • Heatmap Wort–Wort-Distanzen (Satz 1 vs. Satz 3)
  • Balkendiagramm: WMD zwischen allen Satz-Paaren
  • Scatter-Plot der Wort-Embeddings mit Pfeilen (Transport-Approximation)
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import gensim.downloader as api

# 1. Einbettungen laden (z.B. 50d GloVe; ~70 MB)
print("Lade Embeddings…")
wv = api.load("glove-wiki-gigaword-50")

# 2. Sätze definieren
sentences = [
    "Obama speaks to the media in Illinois",
    "The president addresses the press in Chicago",
    "A politician gives a speech to journalists in Springfield"
]

# 3. Tokenisierung & Vokabelfilter
def tokenize(s):
    return [w.lower() for w in s.split() if w.isalpha() and w.lower() in wv]
tokenized = [tokenize(s) for s in sentences]

# 4. Wort–Wort-Distanzmatrix (Euklid) für zwei Sätze
def word_distance_matrix(tokens_a, tokens_b):
    A = np.array([wv[w] for w in tokens_a])
    B = np.array([wv[w] for w in tokens_b])
    # D[i,j] = ||A[i] - B[j]||
    D = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
    return D

D12 = word_distance_matrix(tokenized[0], tokenized[1])
D13 = word_distance_matrix(tokenized[0], tokenized[2])

# 5. Satz–Satz-WMD
print("Berechne WMD…")
wmd12 = wv.wmdistance(tokenized[0], tokenized[1])
wmd13 = wv.wmdistance(tokenized[0], tokenized[2])
wmd23 = wv.wmdistance(tokenized[1], tokenized[2])

# 6. PCA zur 2D-Projektion aller Wörter
all_words = list({w for toks in tokenized for w in toks})
X = np.array([wv[w] for w in all_words])
coords = PCA(n_components=2).fit_transform(X)
# Map Wort → Koordinate
word2coord = {w: coords[i] for i, w in enumerate(all_words)}

# 7. Nächster-Nachbar-Pfeile (Approximation des Transports)
def nearest_arrows(tokens_a, tokens_b, top_k=None):
    D = word_distance_matrix(tokens_a, tokens_b)
    # Für jedes Wort in A den nächsten Nachbarn in B finden
    pairs = []
    for i, wa in enumerate(tokens_a):
        j = np.argmin(D[i])
        pairs.append((wa, tokens_b[j], D[i,j]))
    # Optional nach “stärkstem” (kleinste Distanz) sortieren
    if top_k:
        pairs = sorted(pairs, key=lambda x: x[2])[:top_k]
    return pairs

arrows = nearest_arrows(tokenized[0], tokenized[1], top_k=len(tokenized[0]))

# 8. Plotting
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
sns.heatmap(D12, annot=True, xticklabels=tokenized[1], yticklabels=tokenized[0],
            cmap="viridis", ax=axes[0,0])
axes[0,0].set_title("Heatmap Wort-Distanz: Satz 1 vs. Satz 2")

sns.heatmap(D13, annot=True, xticklabels=tokenized[2], yticklabels=tokenized[0],
            cmap="viridis", ax=axes[0,1])
axes[0,1].set_title("Heatmap Wort-Distanz: Satz 1 vs. Satz 3")

# Balkendiagramm WMD
pairs = ["1–2", "1–3", "2–3"]
vals  = [wmd12,  wmd13,  wmd23]
axes[1,0].bar(pairs, vals)
axes[1,0].set_ylabel("WMD Distance")
axes[1,0].set_title("Word Mover’s Distance zwischen Sätzen")

# Scatter-Plot + Pfeile
ax = axes[1,1]
# Farben pro Satz
colors = {"1": "red", "2": "blue", "3": "green"}
for w in tokenized[0]:
    x, y = word2coord[w]
    ax.scatter(x, y, c=colors["1"], label="Satz 1", s=80)
for w in tokenized[1]:
    x, y = word2coord[w]
    ax.scatter(x, y, c=colors["2"], label="Satz 2", s=80, marker="s")
# Nur wenn Satz 3-Wörter nicht überlagern, kann man sie auch hier plotten:
for w in tokenized[2]:
    x, y = word2coord[w]
    ax.scatter(x, y, c=colors["3"], label="Satz 3", s=80, marker="^")

# Pfeile für Transport-Approximation
for wa, wb, dist in arrows:
    x0, y0 = word2coord[wa]
    x1, y1 = word2coord[wb]
    ax.arrow(x0, y0, x1-x0, y1-y0,
             head_width=0.02, length_includes_head=True, alpha=0.7)

ax.set_title("Word Embeddings + Transport-Pfeile (Satz 1→Satz 2)")
# Legende zusammenfassen
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())
plt.tight_layout()
plt.show()
