import numpy as np
import matplotlib.pyplot as plt

# Parameter
dim = 2                 # Dimension der Daten
n_samples = 1000        # Stichprobengröße pro Generation
n_generations = 600      # Anzahl der Generationen

# Initiale Verteilung
mu_0 = np.zeros(dim)
sigma_0 = np.eye(dim)

# Listen zur Speicherung der Ergebnisse
means = [mu_0]
covariances = [sigma_0]
variances = [np.trace(sigma_0)]

# Simulation über Generationen
for gen in range(n_generations):
    # Stichprobe aus der aktuellen Verteilung ziehen
    samples = np.random.multivariate_normal(means[-1], covariances[-1], size=n_samples)
    
    # Neue Parameter schätzen
    mu_new = np.mean(samples, axis=0)
    sigma_new = np.cov(samples, rowvar=False)
    
    # Ergebnisse speichern
    means.append(mu_new)
    covariances.append(sigma_new)
    variances.append(np.trace(sigma_new))

# Plot der Varianz über Generationen
plt.figure(figsize=(10, 6))
plt.plot(variances, marker='o')
plt.title('Varianz (Spur der Kovarianzmatrix) über Generationen')
plt.xlabel('Generation')
plt.ylabel('Varianz')
plt.grid(True)
plt.show()
