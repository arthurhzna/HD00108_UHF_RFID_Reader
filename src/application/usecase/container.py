from __future__ import annotations

from dataclasses import dataclass

from application.usecase.device import (
    DeviceUseCase,
)

from application.usecase.rfid import (
    RFIDUseCase,
)


@dataclass(slots=True)
class UseCases:

    device: DeviceUseCase

    rfid: RFIDUseCase