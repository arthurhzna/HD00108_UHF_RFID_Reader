from __future__ import annotations
from datetime import datetime

from application.scheduler.trigger.base import (
    Trigger,
)

from application.state.container import (
    States,
)

from application.usecase.container import (
    UseCases,
)

from domain.service.clock import (
    Clock,
)


class Scheduler:

    _POLL_INTERVAL = 0.1

    def __init__(
        self,
        clock: Clock,
        status_trigger: Trigger,
        send_data_trigger: Trigger,
        states: States,
        usecases: UseCases,
    ) -> None:

        self._clock = clock

        self._status_trigger = status_trigger
        self._send_data_trigger = send_data_trigger

        self._states = states

        self._usecases = usecases

        self._last_second = -1

    def run(
        self,
    ) -> None:

        while True:

            self._usecases.rfid.inventory(publish=False)
            second = self._clock.second()

            if second != self._last_second:
                self._last_second = second

                if self._status_trigger.should_run(
                    self._clock,
                ):
                    print(f"Scheduler send status: {datetime.now().strftime('%H:%M:%S.%f')} - Second: {second}")
                    self._usecases.device.sync()

                if self._send_data_trigger.should_run(
                    self._clock,
                ):
                    self._usecases.rfid.inventory(
                        publish=True,
                    )
                    print(f"Scheduler send data: {datetime.now().strftime('%H:%M:%S.%f')} - Second: {second}")

                    self._states.card.clear()

            self._clock.sleep(
                self._POLL_INTERVAL,
            )