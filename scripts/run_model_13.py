import os

from dagflow.plot.graphviz import savegraph
from models import model_13

scripts_directory_path = os.getcwd()
project_directory_path = os.path.dirname(scripts_directory_path)

model = model_13.Model()
savegraph(
    model.graph,
    project_directory_path + "/outputs/plots/model_13-graph.png",
    show="all",
)
