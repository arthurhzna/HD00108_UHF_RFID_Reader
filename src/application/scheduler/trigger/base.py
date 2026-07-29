from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from domain.service.clock import Clock


class Trigger(ABC):

    @abstractmethod
    def should_run(
        self,
        clock: Clock,
    ) -> bool:
        ...