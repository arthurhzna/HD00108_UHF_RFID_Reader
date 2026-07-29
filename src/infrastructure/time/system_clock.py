from __future__ import annotations

import time

from datetime import datetime

from domain.service.clock import Clock


class SystemClock(Clock):

    def now(
        self,
    ) -> str:

        return datetime.now().isoformat()

    def hour(
        self,
    ) -> int:

        return datetime.now().hour

    def minute(
        self,
    ) -> int:

        return datetime.now().minute

    def second(
        self,
    ) -> int:

        return datetime.now().second

    def sleep(
        self,
        seconds: float,
    ) -> None:

        time.sleep(seconds)