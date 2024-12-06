from dgf_statistics.minimizer.minimizerbase import MinimizerBase
from dagflow.parameters import Parameter
from dgf_statistics.MonteCarlo import MonteCarlo
import numpy as np
from scipy import interpolate


def push_grid_values(parameters: list[Parameter], grid_point: np.ndarray):
    for parameter, value in zip(parameters, grid_point):
        parameter.push(value)


def interpolate_pvalue(delta_chi2_MC):
    hist, edges = np.histogram(delta_chi2_MC, "auto")
    centres = (edges[1:] + edges[:-1]) / 2
    cum = np.cumsum(hist / len(delta_chi2_MC))
    f = interpolate.interp1d(centres, 1 - cum, bounds_error=False, fill_value=(1, 0))
    return f


def FC(
    min_chi2_expected_DATA: MinimizerBase,
    min_chi2_bf_DATA: MinimizerBase,
    min_chi2_expected_MC: MinimizerBase,
    min_chi2_bf_MC: MinimizerBase,
    parameters: list[Parameter],
    grid: np.ndarray,
    mc_node: MonteCarlo,
    n_samples: int = 1000,
) -> np.ndarray:

    bf_DATA_chi2 = min_chi2_bf_DATA.fit()["fun"]
    grid_len = grid.shape[0]
    expected_DATA_chi2_values = np.zeros(grid_len)
    pvalues = np.zeros(grid_len)

    for i, grid_point in enumerate(grid):
        push_grid_values(parameters, grid_point)
        min_chi2_expected_DATA.push_initial_values()

        expected_DATA_chi2_values[i] = min_chi2_expected_DATA.fit()["fun"]
        delta_chi2_DATA = expected_DATA_chi2_values[i] - bf_DATA_chi2

        bf_MC_chi2s = np.zeros(n_samples)
        expected_MC_chi2s = np.zeros(n_samples)

        for k in range(n_samples):
            mc_node.next_sample()
            bf_MC_chi2s[k] = min_chi2_bf_MC.fit()["fun"]
            min_chi2_bf_MC.push_initial_values()

            push_grid_values(parameters, grid_point)
            expected_MC_chi2s[k] = min_chi2_expected_MC.fit()["fun"]
            min_chi2_expected_MC.push_initial_values()

        delta_chi2_MC = expected_MC_chi2s - bf_MC_chi2s
        pvalue_func = interpolate_pvalue(delta_chi2_MC)
        pvalues[i] = pvalue_func(delta_chi2_DATA)
    return pvalues
