from argparse import Namespace
from argparse import ArgumentParser

from models import available_models, load_model

from dgf_statistics.minimizer.iminuitminimizer import IMinuitMinimizer
import numpy as np
from models import model_17
from statistical_methods import FeldmanCousins_method

def main(opts: Namespace) -> None:
    model = load_model(
        opts.version,
    )
    print(opts.version)

    min_chi2_bf_DATA = IMinuitMinimizer(
        model.storage["outputs.chi2.bf_DATA"],
        [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
    )

    min_chi2_expected_DATA = IMinuitMinimizer(  
        model.storage["outputs.chi2.expected_DATA"],
        [model.storage["parameters.all.background"]],
    )

    min_chi2_bf_MC = IMinuitMinimizer(  
        model.storage["outputs.chi2.bf_MC"],
        [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
    )

    min_chi2_expected_MC = IMinuitMinimizer(
        model.storage["outputs.chi2.expected_MC"],
        [model.storage["parameters.all.background"]],
    )

    mc_node = model.storage["nodes.monte_carlo.H1"]
    parameter_k = model.storage["parameters.all.k"]
    parameter_k2 = model.storage["parameters.all.k2"]
    parameters = [parameter_k, parameter_k2]

    grid1d = np.linspace(0.1, 1, 6)
    grid = np.transpose([np.tile(grid1d, len(grid1d)), 
                            np.repeat(grid1d, len(grid1d))])
    
    print(grid)

if __name__ == "__main__":
    parser = ArgumentParser()

    model = parser.add_argument_group("model", "model related options")
    model.add_argument(
        "--version",
        default = "NeymanFC",
        choices = available_models(),
        help = "model version",
    )

    main(parser.parse_args())