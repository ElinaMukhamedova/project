from dagflow.bundles.file_reader import FileReader
from dagflow.bundles.load_parameters import load_parameters
from dagflow.core.graph import Graph
from dagflow.core.storage import NodeStorage
from dagflow.lib.arithmetic import Product, Sum
from dagflow.lib.linalg import Cholesky

from dgf_statistics.Chi2 import Chi2
from dgf_statistics.MonteCarlo import MonteCarlo
from dgf_statistics import CNPStat

from numpy import linspace, ones
from dagflow.lib.common import Array

class ConstantBackground_model:

    def __init__(
        self,
    ):
        self.storage = NodeStorage()
        self.build()

    def build(self):
        storage = self.storage

        with (
            Graph(close_on_exit=True, strict=True) as graph,
            storage,
            FileReader,
        ):
            self.graph = graph

            load_parameters(
                format="value",
                state="variable",
                parameters={
                    "background": 100,
                    "k": 0,
                    "k2": 0,
                },
                labels={
                    "background": "constant background, number of events in each bin",
                    "k": "slope coefficient",
                    "k2": "quadratic coefficient",
                },
            )

            nodes = storage.child("nodes")
            inputs = storage.child("inputs")
            outputs = storage.child("outputs")
            data = storage.child("data")
            parameters = storage("parameters")

            E_min = 0
            E_max = 13
            N = 14
            edges = linspace(E_min, E_max, N)
            x = (edges[1:] + edges[:-1]) / 2.0
            observation = ones(N - 1)

            node_x, _ = Array.replicate(
                name="observation.energy.x",
                array=x,
            )

            node_x2, _ = Array.replicate(
                name="observation.energy.x2",
                array=x * x,
            )

            node_observation, _ = Array.replicate(
                name="observation.unit",
                array=observation,
            )

            Product.replicate(
                parameters.get_value("all.background"),
                outputs.get_value("observation.unit"),
                name="observation.H0",
            )

            Product.replicate(
                parameters.get_value("all.k"),
                outputs.get_value("observation.energy.x"),
                name="signal.linear",
            )

            Product.replicate(
                parameters.get_value("all.k2"),
                outputs.get_value("observation.energy.x2"),
                name="signal.quadratic",
            )

            Sum.replicate(
                outputs.get_value("observation.H0"),
                outputs.get_value("signal.linear"),
                outputs.get_value("signal.quadratic"),
                name="observation.H1",
            )

            MonteCarlo.replicate(
                name="monte_carlo.H0",
                mode="poisson",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "monte_carlo.H0.data"
            )

            Cholesky.replicate(
                name="cholesky.MC_H0",
            )
            outputs.get_value("monte_carlo.H0") >> inputs.get_value("cholesky.MC_H0")


            Chi2.replicate(
                name="statistics.stat.H0.chi2_Neyman",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Neyman.theory"
            )
            outputs.get_value("monte_carlo.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Neyman.data"
            )
            outputs.get_value("cholesky.MC_H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Neyman.errors"
            )

            Cholesky.replicate(
                name="cholesky.theory_H0",
            )
            outputs.get_value("observation.H0") >> inputs.get_value("cholesky.theory_H0")

            Chi2.replicate(
                name="statistics.stat.H0.chi2_Pearson",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Pearson.theory"
            )
            outputs.get_value("monte_carlo.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Pearson.data"
            )
            outputs.get_value("cholesky.theory_H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_Pearson.errors"
            )

            CNPStat.replicate(
                name = "CNP_denominator"
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "CNP_denominator.theory"
            )
            outputs.get_value("monte_carlo.H0") >> inputs.get_value(
                "CNP_denominator.data"
            )

            Chi2.replicate(
                name="statistics.stat.H0.chi2_CNP",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_CNP.theory"
            )
            outputs.get_value("monte_carlo.H0") >> inputs.get_value(
                "statistics.stat.H0.chi2_CNP.data"
            )
            outputs.get_value("CNP_denominator") >> inputs.get_value(
                "statistics.stat.H0.chi2_CNP.errors"
            )