from models import model_17
from dagflow.plot.graphviz import savegraph
import os

scripts_directory_path = os.getcwd()
project_directory_path = os.path.dirname(scripts_directory_path)

model = model_17.Model()
savegraph(model.graph, project_directory_path + "/outputs/plots/model_17-graph.png", show = "all")