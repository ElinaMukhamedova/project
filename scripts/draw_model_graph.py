import os
from argparse import ArgumentParser, Namespace

from dagflow.plot.graphviz import savegraph
from models import available_models, load_model


def main(opts: Namespace) -> None:
    modelVersion = opts.version

    Model = load_model(
        modelVersion,
    )
    model = Model()

    scripts_directory_path = os.getcwd()
    project_directory_path = os.path.dirname(scripts_directory_path)

    savegraph(
        model.graph,
        project_directory_path + f"/outputs/plots/{modelVersion}_graph.png",
        show="all",
    )


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "--version",
        default="v0",
        choices=available_models(),
        help="model version",
    )

    main(parser.parse_args())
