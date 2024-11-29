from .FC_Neyman import FC_Neyman_model

_statistics_models = {
    "NeymanFC": FC_Neyman_model,
}

def available_models() -> tuple[str, ...]:
    return tuple(_statistics_models.keys())

def load_model(version):
    try:
        model_to_load = _statistics_models[version]
    except KeyError:
        raise RuntimeError(f"Invalid model version {version}. Available models: {', '.join(sorted(_statistics_models.keys()))}")
    return model_to_load