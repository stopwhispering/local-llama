from typing import TypedDict, Sequence
import logging
from local_llama import settings

logger = logging.getLogger(__name__)


class Conversation(TypedDict):
    uuid: str
    name: str | None


def get_conversations() -> Sequence[Conversation]:
    logger.info(f"Getting conversations from {settings.save_folder}")
    files = settings.save_folder.glob("*.json")
    conversations = [{"uuid": file.stem, "name": None} for file in files]

    return conversations


def get_previous_conversation() -> Conversation | None:
    logger.info(f"Getting previous conversation from {settings.save_folder}")
    files = list(settings.save_folder.glob("*.json"))
    if not files:
        return None
    latest_file = max(files, key=lambda file: file.stat().st_ctime)
    return {
        "uuid": latest_file.stem,
        "name": None,
    }
