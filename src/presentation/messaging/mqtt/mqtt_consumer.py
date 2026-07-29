from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass

MessageHandler = Callable[[str, bytes], None]

@dataclass
class MqttConsumer:
    on_message: MessageHandler

    def handle(
        self,
        topic: str,
        payload: bytes,
    ) -> None:
        self.on_message(topic, payload)