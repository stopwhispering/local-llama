from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    save_folder: Path = Path("../saves")

    available_models: list[dict] = [
        {"model_id": "llama3", "model_name": "Meta-Llama-3-8B-Instruct"},
        {"model_id": "phi3:mini", "model_name": "Microsoft Phi-3 3B (Mini)"},
        {"model_id": "gemma:7b", "model_name": "Google Gemma 7b"},
        {"model_id": "gemma:2b", "model_name": "Google Gemma 2b"},
    ]
