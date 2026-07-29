from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Publisher(ABC):

    @abstractmethod
    def publish_device_register(
        self,
        timestamp: str,
    ) -> None:
        pass

    @abstractmethod
    def publish_device_status(
        self,
        timestamp: str,
    ) -> None:
        pass

    @abstractmethod
    def publish_rfid_summary(
        self,
        timestamp: str,
        cards: list[str],
    ) -> None:
        pass