from dataclasses import dataclass, asdict
import json

@dataclass
class RFIDSummary_MQTT_Output:
    action: str
    id: str
    timestamp: str
    cards: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self))