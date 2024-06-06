import json
from typing import TypedDict, Sequence
import logging
from local_llama import settings
from local_llama.util import custom_decode

logger = logging.getLogger(__name__)


class Conversation(TypedDict):
    uuid: str
    model_name: str


def get_conversations() -> Sequence[Conversation]:
    logger.info(f"Getting conversations from {settings.save_folder}")
    files = settings.save_folder.glob("*.json")

    conversations: list[Conversation] = []
    for file in files:
        with open(file, "r") as f:
            state = json.load(f, object_hook=custom_decode)
            conversations.append(
                Conversation(uuid=state["uuid"], model_name=state["model_name"])
            )

    return conversations


def get_previous_conversation() -> Conversation | None:
    files = list(settings.save_folder.glob("*.json"))
    if not files:
        return None
    latest_file = max(files, key=lambda file: file.stat().st_ctime)
    return {
        "uuid": latest_file.stem,
        "name": None,
    }
