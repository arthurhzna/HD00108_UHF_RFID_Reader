from __future__ import annotations
from dotenv import load_dotenv 
from dataclasses import dataclass
from typing import Optional
import os

load_dotenv() 

@dataclass
class MQTTConfig:
    broker: str
    port: int
    user: Optional[str]
    password: Optional[str]

@dataclass
class AppConfig:
    #Device ID
    device_id: str

    # MQTT
    mqtt: MQTTConfig

Config: AppConfig | None = None


def init_config() -> AppConfig:
    global Config

    mqtt_cfg = MQTTConfig(
        broker=get_env("MQTT_BROKER", "mqtt.com"),
        port=get_env_int("MQTT_PORT", 1883),
        user=get_env("MQTT_USER", ""),
        password=get_env("MQTT_PASS", ""),
    )

    Config = AppConfig(
        device_id=get_env("DEVICE_ID", "default_device"),
        mqtt=mqtt_cfg,
    )

def get_env(key: str, default: str) -> str:
    v = os.getenv(key)
    return v if v not in (None, "") else default


def get_env_int(key: str, default: int) -> int:
    v = os.getenv(key)
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        return default

def get_env_float(key: str, default: float) -> float:
    v = os.getenv(key)
    if not v:
        return default
    try:
        return float(v)
    except ValueError:
        return default