from __future__ import annotations

from dataclasses import dataclass

from application.state.card import CardState
from application.state.device import DeviceState


@dataclass(slots=True)
class States:
    device: DeviceState
    card: CardState
    