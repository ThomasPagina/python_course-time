import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from Levenshtein import distance as levenshtein_distance
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import MultiLabelBinarizer

# Beispiel-Sätze
sentences = [
    "Die Katze sitzt auf der Matte.",
    "Ein Hund liegt auf dem Teppich.",
    "Die Sonne scheint heute hell.",
    "Heute ist ein sonniger Tag.",
    "Der Hund bellt laut.",
    "Ein Vogel fliegt am Himmel.",
    "Die Katze schläft.",
    "Ein Fisch schwimmt im Wasser.",
    "Der Himmel ist blau.",
    "Die Sonne geht unter."
]

labels = [f"Satz {i+1}" for i in range(len(sentences))]

# --- Levenshtein Distanzmatrix ---
lev_matrix = np.array([[levenshtein_distance(a, b) for b in sentences] for a in sentences])

# --- Cosine Distanzmatrix (über TF-IDF) ---
tfidf = TfidfVectorizer().fit_transform(sentences)
cosine_matrix = cosine_distances(tfidf)

# --- Jaccard Distanzmatrix (über Token) ---
token_sets = [set(s.lower().split()) for s in sentences]
mlb = MultiLabelBinarizer()
binary_matrix = mlb.fit_transform(token_sets)
jaccard_matrix = 1 - np.array([
    jaccard_score(binary_matrix[i], binary_matrix[j])
    for i in range(len(sentences)) for j in range(len(sentences))
]).reshape(len(sentences), len(sentences))

# --- Dendrogramm plotten ---
def plot_dendrogram(matrix, method='average', title='Dendrogramm'):
    linked = linkage(matrix, method=method)
    plt.figure(figsize=(10, 5))
    dendrogram(linked, labels=labels, orientation='top', distance_sort='descending')
    plt.title(title)
    plt.tight_layout()
    plt.show()

plot_dendrogram(lev_matrix, title='Dendrogramm (Levenshtein)')
plot_dendrogram(cosine_matrix, title='Dendrogramm (Cosine TF-IDF)')
plot_dendrogram(jaccard_matrix, title='Dendrogramm (Jaccard Token)')
