from uuid import uuid4
from typing import Sequence
import json
from local_llama import settings
from local_llama.entities import Message
from local_llama.ollama_api.ollama_llm import (
    init_ollama_llm,
    OllamaModel,
    OllamaRequest,
)
from local_llama.util import CustomEncoder, custom_decode


class Assistant:
    def __init__(
        self, messages: list[Message], model_name: str, temperature: float, uuid: str
    ):
        self.messages = messages
        self.model_name = model_name
        self.llm: OllamaModel = init_ollama_llm(model_name)
        self.temperature = temperature
        self.uuid = uuid

    @staticmethod
    def create(system_instructions: str, model_name: str, temperature: float):
        messages: list[Message] = [Message(role="system", content=system_instructions)]
        assistant = Assistant(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            uuid=str(uuid4()),
        )
        assistant.save()
        return assistant

    @staticmethod
    def load(uuid: str):
        with open(settings.save_folder / f"{uuid}.json", "r") as f:
            state = json.load(f, object_hook=custom_decode)
        return Assistant(
            messages=state["messages"],
            model_name=state["model_name"],
            temperature=state["temperature"],
            uuid=state["uuid"],
        )

    def run(self) -> OllamaRequest:
        return OllamaRequest(
            messages=self.messages, temperature=self.temperature, llm=self.llm
        )
        # stream = self.llm.generate_response_stream(messages=self.messages,
        #                                            temperature=self.temperature)
        # chunk: OllamaChunk
        # for chunk in stream:
        #     yield chunk['message']['content']

    def get_messages(self) -> Sequence[Message]:
        return self.messages

    def add_message(self, message: Message):
        self.messages.append(message)
        self.save()

    def save(self):
        state = {
            "uuid": self.uuid,
            "messages": self.messages,
            "model_name": self.model_name,
            "temperature": self.temperature,
        }
        with open(settings.save_folder / f"{self.uuid}.json", "w") as f:
            json.dump(state, f, cls=CustomEncoder)

    def request_response(self) -> OllamaRequest:
        ollama_request = OllamaRequest(
            messages=self.get_messages(), temperature=self.temperature, llm=self.llm
        )
        return ollama_request
