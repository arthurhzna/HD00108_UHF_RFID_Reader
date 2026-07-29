from __future__ import annotations

from domain.service.clock import Clock

from application.scheduler.trigger.base import Trigger


class EverySecond(Trigger):

    def __init__(
        self,
        second: int,
    ) -> None:

        self._second = second

    def should_run(
        self,
        clock: Clock,
    ) -> bool:

        return (
            clock.second()
            == self._second
        )