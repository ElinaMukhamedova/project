from numpy import linspace, ones

from dagflow.bundles.file_reader import FileReader
from dagflow.bundles.load_parameters import load_parameters
from dagflow.core.graph import Graph
from dagflow.core.storage import NodeStorage
from dagflow.lib.arithmetic import Product, Sum
from dagflow.lib.common import Array
from dagflow.lib.linalg import Cholesky
from dgf_statistics import CNPStat, LogPoisson
from dgf_statistics.Chi2 import Chi2
from dgf_statistics.MonteCarlo import MonteCarlo


class FC_model:

    __slots__ = (
        "storage",
        "graph",
    )

    storage: NodeStorage
    graph: Graph | None

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
            E_max = 17
            N = 18
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
                name="monte_carlo.H1",
                mode="poisson",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "monte_carlo.H1.data"
            )

            Cholesky.replicate(
                name="cholesky.MC_H1",
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value("cholesky.MC_H1")

            MonteCarlo.replicate(
                name="DATA.H1",
                mode="asimov",
            )
            outputs.get_value("observation.H1") >> inputs.get_value("DATA.H1.data")

            Cholesky.replicate(
                name="cholesky.DATA_H1",
            )
            outputs.get_value("DATA.H1") >> inputs.get_value("cholesky.DATA_H1")

            Cholesky.replicate(
                name="cholesky.theory_H0",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "cholesky.theory_H0"
            )

            Cholesky.replicate(
                name="cholesky.theory_H1",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "cholesky.theory_H1"
            )

            #################################################################################

            Chi2.replicate(
                name="chi2_Neyman.bf_MC",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_Neyman.bf_MC.theory"
            )
            outputs.get_value("cholesky.MC_H1") >> inputs.get_value(
                "chi2_Neyman.bf_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_Neyman.bf_MC.data"
            )

            Chi2.replicate(
                name="chi2_Neyman.expected_MC",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_Neyman.expected_MC.theory"
            )
            outputs.get_value("cholesky.MC_H1") >> inputs.get_value(
                "chi2_Neyman.expected_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_Neyman.expected_MC.data"
            )

            Chi2.replicate(
                name="chi2_Neyman.bf_DATA",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_Neyman.bf_DATA.theory"
            )
            outputs.get_value("cholesky.DATA_H1") >> inputs.get_value(
                "chi2_Neyman.bf_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value("chi2_Neyman.bf_DATA.data")

            Chi2.replicate(
                name="chi2_Neyman.expected_DATA",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_Neyman.expected_DATA.theory"
            )
            outputs.get_value("cholesky.DATA_H1") >> inputs.get_value(
                "chi2_Neyman.expected_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "chi2_Neyman.expected_DATA.data"
            )

            #################################################################################

            Chi2.replicate(
                name="chi2_Pearson.bf_MC",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_Pearson.bf_MC.theory"
            )
            outputs.get_value("cholesky.theory_H0") >> inputs.get_value(
                "chi2_Pearson.bf_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_Pearson.bf_MC.data"
            )

            Chi2.replicate(
                name="chi2_Pearson.expected_MC",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_Pearson.expected_MC.theory"
            )
            outputs.get_value("cholesky.theory_H1") >> inputs.get_value(
                "chi2_Pearson.expected_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_Pearson.expected_MC.data"
            )

            Chi2.replicate(
                name="chi2_Pearson.bf_DATA",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_Pearson.bf_DATA.theory"
            )
            outputs.get_value("cholesky.theory_H0") >> inputs.get_value(
                "chi2_Pearson.bf_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "chi2_Pearson.bf_DATA.data"
            )

            Chi2.replicate(
                name="chi2_Pearson.expected_DATA",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_Pearson.expected_DATA.theory"
            )
            outputs.get_value("cholesky.theory_H1") >> inputs.get_value(
                "chi2_Pearson.expected_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "chi2_Pearson.expected_DATA.data"
            )

            #################################################################################

            CNPStat.replicate(name="CNP_bf_MC_denominator")
            outputs.get_value("observation.H0") >> inputs.get_value(
                "CNP_bf_MC_denominator.theory"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "CNP_bf_MC_denominator.data"
            )

            CNPStat.replicate(name="CNP_expected_MC_denominator")
            outputs.get_value("observation.H1") >> inputs.get_value(
                "CNP_expected_MC_denominator.theory"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "CNP_expected_MC_denominator.data"
            )

            CNPStat.replicate(name="CNP_bf_DATA_denominator")
            outputs.get_value("observation.H0") >> inputs.get_value(
                "CNP_bf_DATA_denominator.theory"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "CNP_bf_DATA_denominator.data"
            )

            CNPStat.replicate(name="CNP_expected_DATA_denominator")
            outputs.get_value("observation.H1") >> inputs.get_value(
                "CNP_expected_DATA_denominator.theory"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "CNP_expected_DATA_denominator.data"
            )

            Chi2.replicate(
                name="chi2_CNP.bf_MC",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_CNP.bf_MC.theory"
            )
            outputs.get_value("CNP_bf_MC_denominator") >> inputs.get_value(
                "chi2_CNP.bf_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_CNP.bf_MC.data"
            )

            Chi2.replicate(
                name="chi2_CNP.expected_MC",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_CNP.expected_MC.theory"
            )
            outputs.get_value("CNP_expected_MC_denominator") >> inputs.get_value(
                "chi2_CNP.expected_MC.errors"
            )
            outputs.get_value("monte_carlo.H1") >> inputs.get_value(
                "chi2_CNP.expected_MC.data"
            )

            Chi2.replicate(
                name="chi2_CNP.bf_DATA",
            )
            outputs.get_value("observation.H0") >> inputs.get_value(
                "chi2_CNP.bf_DATA.theory"
            )
            outputs.get_value("CNP_bf_DATA_denominator") >> inputs.get_value(
                "chi2_CNP.bf_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value("chi2_CNP.bf_DATA.data")

            Chi2.replicate(
                name="chi2_CNP.expected_DATA",
            )
            outputs.get_value("observation.H1") >> inputs.get_value(
                "chi2_CNP.expected_DATA.theory"
            )
            outputs.get_value("CNP_expected_DATA_denominator") >> inputs.get_value(
                "chi2_CNP.expected_DATA.errors"
            )
            outputs.get_value("DATA.H1") >> inputs.get_value(
                "chi2_CNP.expected_DATA.data"
            )

            #################################################################################
