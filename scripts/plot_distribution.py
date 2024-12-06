from argparse import ArgumentParser, Namespace

import numpy as np

from dgf_statistics.minimizer.iminuitminimizer import IMinuitMinimizer
from models import load_model
from statistical_methods import histogram


def main(opts: Namespace) -> None:
    chi2_types = opts.chi2_types

    ConstantBackgroundModel = load_model(
        "ConstantBackground",
    )
    model = ConstantBackgroundModel()

    mc_H0_node = model.storage["nodes.monte_carlo.H0"]

    settings = {}

    for chi2_type in chi2_types:
        min_H0_chi2 = IMinuitMinimizer(
            model.storage[f"outputs.statistics.stat.H0.chi2_{chi2_type}"],
            [model.storage["parameters.all.background"]],
        )
        settings[chi2_type] = histogram.parameter_histogram(
            min_H0_chi2, mc_H0_node, 30000, 100
        )

    histogram.plot_C_histograms(
        settings, model.storage["parameters.all.background"].value
    )


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--chi2_types",
        default=["Poisson"],
        nargs="+",
        help="chi-squared types to plot",
    )

    main(parser.parse_args())
