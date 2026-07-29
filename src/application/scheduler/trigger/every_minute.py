from __future__ import annotations

from domain.service.clock import Clock

from application.scheduler.trigger.base import Trigger


class EveryMinute(Trigger):

    def __init__(
        self,
        minute: int,
    ) -> None:

        self._minute = minute

    def should_run(
        self,
        clock: Clock,
    ) -> bool:

        return (
            clock.minute()
            % self._minute
            == 0
            and clock.second() == 0
        )