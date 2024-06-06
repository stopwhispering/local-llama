from typing import TypedDict

import ollama


class OllamaModelOverview(TypedDict):
    model: str
    parameter_size: str
    family: str
    size: int  # in bytes
    quanitization_level: str


def get_available_models() -> list[OllamaModelOverview]:
    models_list = ollama.list()
    models = [
        OllamaModelOverview(
            model=m.get("model"),
            size=m.get("size"),
            family=m.get("details", {}).get("family"),
            parameter_size=m.get("details", {}).get("parameter_size"),
            quanitization_level=m.get("details", {}).get("quantization_level"),
        )
        for m in models_list["models"]
        if m.get("details", {}).get("family") != "nomic-bert"
    ]
    return models
