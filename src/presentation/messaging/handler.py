from __future__ import annotations

from typing import Protocol


class MessageHandler(Protocol):

    def handle(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        ...