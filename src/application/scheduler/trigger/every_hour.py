from __future__ import annotations

from application.scheduler.trigger.base import (
    Trigger,
)

from domain.service.clock import (
    Clock,
)


class EveryHour(Trigger):

    def __init__(
        self,
        hour: int,
    ) -> None:

        self._hour = hour

    def should_run(
        self,
        clock: Clock,
    ) -> bool:

        return (
            clock.hour() % self._hour == 0
            and clock.minute() == 0
            and clock.second() == 0
        )