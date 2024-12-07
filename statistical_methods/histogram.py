import os

import numpy as np
from matplotlib import pyplot as plt

from dgf_statistics.minimizer.minimizerbase import MinimizerBase
from dgf_statistics.MonteCarlo import MonteCarlo


def parameter_histogram(
    min_chi2: MinimizerBase,
    mc_node: MonteCarlo,
    n_mc_samples: int = 1000,
    n_bins: int = 10,
) -> tuple[np.array, np.array, float]:
    fit_parameters = np.zeros(n_mc_samples)
    for i in range(n_mc_samples):
        mc_node.next_sample()
        fit_the_data = min_chi2.fit()
        min_chi2.push_initial_values()
        fit_parameters[i] = fit_the_data["x"][0]
    hist, bin_edges = np.histogram(fit_parameters, n_bins)
    density_hist = hist / n_mc_samples
    bins = (bin_edges[1:] + bin_edges[:-1]) / 2.0
    mean = np.mean(fit_parameters)
    return density_hist, bins, mean


def plot_C_histograms(
    settings: dict,
    C_true: float,
) -> None:
    scripts_directory_path = os.getcwd()
    project_directory_path = os.path.dirname(scripts_directory_path)
    name = project_directory_path + "/outputs/plots/C_"
    for key in settings.keys():
        hist, bins, mean = settings[key]
        plt.bar(
            bins,
            hist,
            width=bins[1] - bins[0],
            alpha=0.4,
            label="$C_{" + key + "} = $" + str("{:.2f}".format(mean)),
        )
        plt.vlines(mean, 0, hist.max(), colors="r", linestyle="dashed", linewidth=1)
        name += key + "_"
    name += "histograms.png"
    plt.xlabel(r"$C$", loc="right")
    plt.ylabel(r"$\rho$", rotation=0, loc="top")
    plt.title("Model: flat spectrum, y = C; $C_{true}$ = " + str(C_true))
    plt.legend()
    plt.savefig(name)
