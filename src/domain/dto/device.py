from dataclasses import dataclass, asdict
import json


@dataclass
class DeviceRegist_MQTT_Output:
    action: str
    id: str
    timestamp: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))



@dataclass
class DeviceStatus_MQTT_Output:
    action: str
    id: str
    timestamp: str
    software_version: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))