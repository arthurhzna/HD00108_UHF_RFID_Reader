from dataclasses import dataclass, asdict
from typing import Dict, Any
from events.base_event import BaseEvent
import json

@dataclass
class DeviceStatusEvent(BaseEvent):
    action: str
    device_id: str
    nama: str
    timestamp: str
