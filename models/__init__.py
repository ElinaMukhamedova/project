from typing import Mapping
from yaml import Loader, load
from dagflow.tools.logger import logger

from .FeldmanCousins import FC_model
from .ConstantBackground import ConstantBackground_model

_statistics_models = {
    "FeldmanCousins": FC_model,
    "ConstantBackground": ConstantBackground_model,
}

def available_models() -> tuple[str, ...]:
    return tuple(_statistics_models.keys())

def load_model(version):
    try:
        model_to_load = _statistics_models[version]
    except KeyError:
        raise RuntimeError(f"Invalid model version {version}. Available models: {', '.join(sorted(_statistics_models.keys()))}")
    
    return model_to_load