import json

from local_llama.entities import Message


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        return super().default(obj)


def custom_decode(obj):
    """hook to convert dict to Message (or possibly other custom) object"""
    if "role" in obj and "content" in obj and "total_duration" in obj:
        return Message(
            role=obj["role"],
            content=obj["content"],
            total_duration=obj["total_duration"],
        )
    return obj
