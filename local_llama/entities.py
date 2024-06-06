from dataclasses import dataclass
from typing import Literal


@dataclass
class Message:
    role: Literal["user", "assistant", "system"]
    content: str
    total_duration: int | None = None  # in milliseconds
    done_reason: str | None = None

    def as_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }

    def format_content(self) -> str:
        if self.role == "assistant":
            return (
                self.content
                + "  \n :blue["
                + f"{self.total_duration / 1_000_000_000 :.2f}"
                + " sec. ]"
            )
        return self.content
