import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict


def generate_initial_parameters(dim: int) -> Tuple[np.ndarray, np.ndarray]:
    """Generate the initial mean and covariance matrix."""
    mean = np.zeros(dim)
    covariance = np.eye(dim)
    return mean, covariance


def sample_multivariate_normal(mean: np.ndarray, covariance: np.ndarray, n_samples: int) -> np.ndarray:
    """Draw samples from a multivariate normal distribution."""
    return np.random.multivariate_normal(mean, covariance, size=n_samples)


def estimate_parameters(samples: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Estimate mean and covariance matrix from samples."""
    mean = np.mean(samples, axis=0)
    covariance = np.cov(samples, rowvar=False)
    return mean, covariance


def simulate_generations(
    dim: int,
    n_samples: int,
    n_generations: int,
    sample_indices_to_save: Tuple[int, int, int]
) -> Tuple[list, Dict[int, np.ndarray]]:
    """Run multiple generations, saving traces of variance and selected samples."""
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
    """Plot the variance trace over generations."""
    ax.plot(variances, marker='o')
    ax.set_title('Variance over Generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Variance')
    ax.grid(True)


def plot_initial_sample(ax: plt.Axes, samples: np.ndarray, generation: int) -> None:
    """Plot the initial sample distribution."""
    ax.scatter(samples[:, 0], samples[:, 1], c='gray', alpha=0.5)
    ax.set_title(f'Initial Sample (Generation {generation})')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.grid(True)


def plot_sample_overlay(
    ax: plt.Axes,
    base_samples: np.ndarray,
    overlay_samples: np.ndarray,
    base_gen: int,
    overlay_gen: int,
    overlay_color: str
) -> None:
    """Overlay base and overlay samples on the same axes."""
    ax.scatter(base_samples[:, 0], base_samples[:, 1], c='gray', alpha=0.3, label=f'Gen {base_gen}')
    ax.scatter(overlay_samples[:, 0], overlay_samples[:, 1], c=overlay_color, alpha=0.5, label=f'Gen {overlay_gen}')
    ax.set_title(f'Comparison: Gen {base_gen} vs Gen {overlay_gen}')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.grid(True)
    ax.legend()


def plot_results(
    variances: list,
    saved_samples: Dict[int, np.ndarray],
    sample_indices_to_save: Tuple[int, int, int]
) -> None:
    """Create a 2x2 figure: variance plot and sample distributions with overlays."""
    initial_gen, mid_gen, last_gen = sample_indices_to_save
    initial_samples = saved_samples[initial_gen]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Top-left: variance trace
    plot_variance_over_generations(variances, ax=axes[0, 0])

    # Top-right: initial sample
    plot_initial_sample(ax=axes[0, 1], samples=initial_samples, generation=initial_gen)

    # Bottom-left: overlay of initial and middle generation
    plot_sample_overlay(
        ax=axes[1, 0],
        base_samples=initial_samples,
        overlay_samples=saved_samples[mid_gen],
        base_gen=initial_gen,
        overlay_gen=mid_gen,
        overlay_color='blue'
    )

    # Bottom-right: overlay of initial and last generation
    plot_sample_overlay(
        ax=axes[1, 1],
        base_samples=initial_samples,
        overlay_samples=saved_samples[last_gen],
        base_gen=initial_gen,
        overlay_gen=last_gen,
        overlay_color='green'
    )

    plt.tight_layout()
    plt.show()


def simulate(n_samples: int, n_generations: int) -> None:
    """Main function to run simulation and plotting."""
    sample_indices_to_save = (0, n_generations // 2, n_generations - 1)
    dim = 2

    variances, saved_samples = simulate_generations(
        dim, n_samples, n_generations, sample_indices_to_save
    )
    plot_results(variances, saved_samples, sample_indices_to_save)


if __name__ == "__main__":
    simulate(
        n_samples=1000,
        n_generations=3000
    )
