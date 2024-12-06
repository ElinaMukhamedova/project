from argparse import ArgumentParser, Namespace

import numpy as np

from dgf_statistics.minimizer.iminuitminimizer import IMinuitMinimizer
from models import load_model
from statistical_methods import FeldmanCousins_method


def main(opts: Namespace) -> None:
    chi2_type = opts.chi2_type

    FCmodel = load_model(
        "FeldmanCousins",
    )
    model = FCmodel()

    min_chi2_bf_DATA = IMinuitMinimizer(
        model.storage[f"outputs.chi2_{chi2_type}.bf_DATA"],
        [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
    )

    min_chi2_expected_DATA = IMinuitMinimizer(
        model.storage[f"outputs.chi2_{chi2_type}.expected_DATA"],
        [model.storage["parameters.all.background"]],
    )

    min_chi2_bf_MC = IMinuitMinimizer(
        model.storage[f"outputs.chi2_{chi2_type}.bf_MC"],
        [model.storage["parameters.all.k"], model.storage["parameters.all.background"]],
    )

    min_chi2_expected_MC = IMinuitMinimizer(
        model.storage[f"outputs.chi2_{chi2_type}.expected_MC"],
        [model.storage["parameters.all.background"]],
    )

    mc_node = model.storage["nodes.monte_carlo.H1"]
    parameter_k = model.storage["parameters.all.k"]
    parameter_k2 = model.storage["parameters.all.k2"]
    parameters = [parameter_k, parameter_k2]

    grid1d = np.linspace(0.1, 1, 6)
    grid = np.transpose([np.tile(grid1d, len(grid1d)), np.repeat(grid1d, len(grid1d))])

    print(grid)

    # pvalues_for_grid = FeldmanCousins_method.FC(
    #    min_chi2_expected_DATA,
    #    min_chi2_bf_DATA,
    #    min_chi2_expected_MC,
    #    min_chi2_bf_MC,
    #    parameters,
    #    grid,
    #    mc_node,
    # )


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--chi2_type",
        default="Poisson",
        choices=["Poisson", "Neyman", "Pearson", "CNP"],
        help="chi-squared type",
    )

    main(parser.parse_args())
