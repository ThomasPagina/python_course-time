import numpy as np
import matplotlib.pyplot as plt

# Parameter
dim = 2                 # Dimension der Daten
n_samples = 1000        # Stichprobengröße pro Generation
n_generations = 400      # Anzahl der Generationen

# Initiale Verteilung
mu_0 = np.zeros(dim)
sigma_0 = np.eye(dim)

# Listen zur Speicherung der Ergebnisse
means = [mu_0]
covariances = [sigma_0]
variances = [np.trace(sigma_0)]
samples_list = []

# Generationen für die zu speichernden Samples
gen_indices = [0, n_generations // 2, n_generations - 1]
saved_samples = {}

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
    
    # Spezifische Samples speichern
    if gen in gen_indices:
        saved_samples[gen] = samples

# Plot erstellen
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Varianz über Generationen
axs[0, 0].plot(variances, marker='o')
axs[0, 0].set_title('Varianz über Generationen')
axs[0, 0].set_xlabel('Generation')
axs[0, 0].set_ylabel('Varianz')
axs[0, 0].grid(True)

# Scatter-Plots der gespeicherten Samples
titles = {
    gen_indices[0]: 'Ausgangssample (Generation 0)',
    gen_indices[1]: f'Mittleres Sample (Generation {gen_indices[1]})',
    gen_indices[2]: f'Endsample (Generation {gen_indices[2]})'
}

positions = [(0, 1), (1, 0), (1, 1)]

for idx, gen in enumerate(gen_indices):
    row, col = positions[idx]
    sample = saved_samples[gen]
    axs[row, col].scatter(sample[:, 0], sample[:, 1], alpha=0.5)
    axs[row, col].set_title(titles[gen])
    axs[row, col].set_xlabel('X1')
    axs[row, col].set_ylabel('X2')
    axs[row, col].grid(True)

plt.tight_layout()
plt.show()
