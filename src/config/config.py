from __future__ import annotations

from dataclasses import dataclass
from dotenv import load_dotenv

from config.device import (
    DeviceConfig,
    load_device_config,
)
from config.mqtt import (
    MQTTConfig,
    load_mqtt_config,
)
from config.serial import (
    SerialConfig,
    load_serial_config,
)

load_dotenv()  

@dataclass(slots=True)
class Config:
    device: DeviceConfig
    mqtt: MQTTConfig
    serial: SerialConfig


def load_config() -> Config:

    return Config(
        device=load_device_config(),
        mqtt=load_mqtt_config(),
        serial=load_serial_config(),
    )