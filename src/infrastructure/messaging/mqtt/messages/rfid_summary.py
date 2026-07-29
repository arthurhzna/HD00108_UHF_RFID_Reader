from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RFIDSummaryMessage:
    action: str
    id: str
    timestamp: str
    cards: list[str]