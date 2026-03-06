from dataclasses import dataclass, field
from typing import Set

@dataclass
class RFIDSummaryData:
    cards: Set[str] = field(default_factory=set)