from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)


class Clock(ABC):

    @abstractmethod
    def now(
        self,
    ) -> str:
        ...

    @abstractmethod
    def hour(
        self,
    ) -> int:
        ...

    @abstractmethod
    def minute(
        self,
    ) -> int:
        ...

    @abstractmethod
    def second(
        self,
    ) -> int:
        ...

    @abstractmethod
    def sleep(
        self,
        seconds: float,
    ) -> None:
        ...