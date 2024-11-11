from dgf_statistics.minimizer.iminuitminimizer import IMinuitMinimizer
import numpy as np
from models import model_17
from statistical_methods import FeldmanCousins_method

model = model_17.Model()

min_chi2_bf_DATA = IMinuitMinimizer(
    model.storage["outputs.chi2_Neyman.bf_DATA"],
    [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
)

min_chi2_expected_DATA = IMinuitMinimizer(
    model.storage["outputs.chi2_Neyman.expected_DATA"],
    [model.storage["parameters.all.background"]],
)

min_chi2_bf_MC = IMinuitMinimizer(
    model.storage["outputs.chi2_Neyman.bf_MC"],
    [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
)

min_chi2_expected_MC = IMinuitMinimizer(
    model.storage["outputs.chi2_Neyman.expected_MC"],
    [model.storage["parameters.all.background"]],
)

mc_node = model.storage["nodes.monte_carlo.H1"]
parameter_k = model.storage["parameters.all.k"]
parameter_k2 = model.storage["parameters.all.k2"]
parameters = [parameter_k, parameter_k2]
grid1d = np.linspace(0.1, 1, 6)#.reshape((11, 1))
grid = np.transpose([np.tile(grid1d, len(grid1d)), 
                            np.repeat(grid1d, len(grid1d))])
print("grid:", grid)
#parameters = [parameter_k]
#grid_1d = np.linspace(0.1, 1, 10)

pvalues_for_grid = FeldmanCousins_method.FC(
    min_chi2_expected_DATA,
    min_chi2_bf_DATA,
    min_chi2_expected_MC,
    min_chi2_bf_MC,
    parameters,
    grid,
    mc_node,
)
print("pvalues_for_grid", pvalues_for_grid)