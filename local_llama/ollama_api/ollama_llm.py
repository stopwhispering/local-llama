from typing import Iterator, Mapping, Any, Sequence, TypedDict, NotRequired

import ollama
from ollama import Message as OllamaMessage

from local_llama.entities import Message


class OllamaModel:
    """
    Meta-Llama-3-8B-Instruct: https://ollama.com/library/llama3 (llama3)
    Microsoft Phi-3 3B (Mini): https://ollama.com/library/phi3 (phi3:mini)
    Google Gemma 7b: https://ollama.com/library/gemma (gemma:7b)
    Google Gemma 2b: https://ollama.com/library/gemma (gemma:2b)
    """

    def __init__(self, model_name: str):
        # self.model_id = model_id
        self.model_name = model_name

    def generate_response_stream(
        self,
        messages: Sequence[Message],
        temperature: float,
    ) -> Iterator[Mapping[str, Any]]:
        stream = ollama.chat(
            model=self.model_name,
            messages=[m.as_dict() for m in messages],
            options={
                "temperature": temperature,
            },
            stream=True,
        )

        return stream


def init_ollama_llm(model_name: str) -> OllamaModel:
    """factory function to initialize OllamaModel from model_name"""
    # model = next(
    #     (
    #         model
    #         for model in settings.available_models
    #         if model["model_name"] == model_name
    #     ),
    #     None,
    # )
    # if not model_name:
    #     raise ValueError(f"Model {model_name} not found in available models")
    return OllamaModel(model_name=model_name)


class OllamaRequest:
    def __init__(
        self,
        messages: Sequence[Message],
        temperature: float,
        llm: OllamaModel,
    ):
        self.messages = messages
        self.temperature = temperature
        self.llm = llm
        self.ongoing_response: str = ""
        self.response: Message | None = None

    def generate(self) -> Iterator[str]:
        stream = self.llm.generate_response_stream(
            messages=self.messages, temperature=self.temperature
        )
        chunk: OllamaChunk
        for chunk in stream:
            self.ongoing_response += chunk["message"]["content"]
            if chunk["done"]:
                self.response = Message(
                    role=chunk["message"]["role"],
                    content=self.ongoing_response,
                    total_duration=chunk.get("total_duration"),
                    done_reason=chunk.get("done_reason"),
                )
            yield chunk["message"]["content"]


class OllamaChunk(TypedDict):
    created_at: str  # eg. '2024-06-06T13:11:40.6237253Z'
    message: OllamaMessage
    done: bool
    done_reason: NotRequired[str]
    total_duration: NotRequired[int]  # in nanoseconds
