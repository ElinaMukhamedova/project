from models import model_13
from dagflow.plot.graphviz import savegraph
import os

scripts_directory_path = os.getcwd()
project_directory_path = os.path.dirname(scripts_directory_path)

model = model_13.Model()
savegraph(model.graph, project_directory_path + "/illustrations/model_13-graph.png", show = "all")