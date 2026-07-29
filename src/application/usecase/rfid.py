from __future__ import annotations

from application.state.container import States

from domain.service.clock import Clock
from domain.service.publisher import Publisher
from domain.service.rfid import RFID


class RFIDUseCase:

    def __init__(
        self,
        rfid: RFID,
        publisher: Publisher,
        clock: Clock,
        states: States,
    ) -> None:

        self._rfid = rfid
        self._states = states
        self._publisher = publisher
        self._clock = clock

    def inventory(
        self,
        publish: bool = True,
    ) -> list[str]:

        cards = self._rfid.inventory()
        self._states.card.add(cards)

        if publish:

            self._publisher.publish_rfid_summary(
                timestamp=self._clock.now(),
                cards=self._states.card.snapshot(),
            )

        return cards