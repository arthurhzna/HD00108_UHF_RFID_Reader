from dataclasses import dataclass, asdict
from typing import Dict, Any
from events.base_event import BaseEvent
import time
import json

@dataclass
class RFIDSummaryEvent(BaseEvent):
    device_id: str
    timestamp: str
    cards: list[str]
