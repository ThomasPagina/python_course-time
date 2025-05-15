import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict

def generate_initial_parameters(dim: int) -> Tuple[np.ndarray, np.ndarray]:
    """Erzeugt den initialen Mittelwert und die Kovarianzmatrix."""
    mean = np.zeros(dim)
    covariance = np.eye(dim)
    return mean, covariance

def sample_multivariate_normal(mean: np.ndarray, covariance: np.ndarray, n_samples: int) -> np.ndarray:
    """Zieht Stichproben aus einer multivariaten Normalverteilung."""
    return np.random.multivariate_normal(mean, covariance, size=n_samples)

def estimate_parameters(samples: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Schätzt den Mittelwert und die Kovarianzmatrix der Stichproben."""
    mean = np.mean(samples, axis=0)
    covariance = np.cov(samples, rowvar=False)
    return mean, covariance

def simulate_generations(
    dim: int,
    n_samples: int,
    n_generations: int,
    sample_indices_to_save: Tuple[int, int, int]
) -> Tuple[list, Dict[int, np.ndarray]]:
    """Simuliert mehrere Generationen und speichert ausgewählte Stichproben."""
    mean, covariance = generate_initial_parameters(dim)
    variances = [np.trace(covariance)]
    saved_samples = {}

    for generation in range(n_generations):
        samples = sample_multivariate_normal(mean, covariance, n_samples)
        mean, covariance = estimate_parameters(samples)
        variances.append(np.trace(covariance))

        if generation in sample_indices_to_save:
            saved_samples[generation] = samples

    return variances, saved_samples

def plot_variance_over_generations(variances: list, ax: plt.Axes) -> None:
    """Zeichnet den Verlauf der Varianz über die Generationen."""
    ax.plot(variances, marker='o')
    ax.set_title('Varianz über Generationen')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Varianz')
    ax.grid(True)

def plot_sample_scatter(samples: np.ndarray, ax: plt.Axes, title: str) -> None:
    """Zeichnet einen Scatter-Plot der Stichproben."""
    ax.scatter(samples[:, 0], samples[:, 1], alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.grid(True)

def getTitles_from_sample_indices(sample_indices: Tuple[int, int, int]) -> Dict[int, str]:
    """Erzeugt Titel für die Scatter-Plots aus den Stichproben-Indizes."""
    return {
        sample_indices[0]: f'Ausgangssample (Generation {sample_indices[0]})',
        sample_indices[1]: f'Mittleres Sample (Generation {sample_indices[1]})',
        sample_indices[2]: f'Endsample (Generation {sample_indices[2]})'
    }

def plot_results(
    variances: list,
    saved_samples: Dict[int, np.ndarray],
    sample_indices_to_save: Tuple[int, int, int]
) -> None:
    """Erstellt ein 2x2-Plot mit Varianzverlauf und ausgewählten Stichproben."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # variances in the first subplot
    plot_variance_over_generations(variances, ax=axes[0, 0])
    # scatter plots in the other subplots
    scatter_samples_with_titles(saved_samples, sample_indices_to_save, axes)

    plt.tight_layout()
    plt.show()

def scatter_samples_with_titles(saved_samples, sample_indices_to_save, axes):
    titles = getTitles_from_sample_indices(sample_indices_to_save)

    positions = [(0, 1), (1, 0), (1, 1)]

    for idx, gen in enumerate(sample_indices_to_save):
        row, col = positions[idx]
        sample = saved_samples.get(gen)
        if sample is not None:
            plot_sample_scatter(sample, ax=axes[row, col], title=titles[gen])

def simulate( n_samples:int, n_generations:int) -> Tuple[list, Dict[int, np.ndarray]]: 
    """Hauptfunktion zur Ausführung der Simulation und Visualisierung."""
    
    sample_indices_to_save = (0, n_generations // 2, n_generations - 1)
    dim=2

    variances, saved_samples = simulate_generations(
        dim, n_samples, n_generations, sample_indices_to_save
    )
    plot_results(variances, saved_samples, sample_indices_to_save)

if __name__ == "__main__":
    simulate(
       
        n_samples=1000, 
        n_generations=100 
        
    )

