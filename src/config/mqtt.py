from __future__ import annotations

import os
import uuid

from dataclasses import dataclass


@dataclass(slots=True)
class MQTTConfig:
    broker: str
    port: int
    username: str
    password: str
    use_tls: bool
    client_id: str

    subscribe_topic: str

    device_register_topic: str
    publish_data_topic: str



def load_mqtt_config() -> MQTTConfig:

    device_id = os.getenv(
        "DEVICE_ID",
        "unknown",
    )

    return MQTTConfig(
        broker=os.getenv(
            "MQTT_BROKER",
            "localhost",
        ),

        port=int(
            os.getenv(
                "MQTT_PORT",
                "1883",
            )
        ),

        username=os.getenv(
            "MQTT_USERNAME",
            "",
        ),

        password=os.getenv(
            "MQTT_PASSWORD",
            "",
        ),

        use_tls=os.getenv(
            "MQTT_USE_TLS",
            "false",
        ).lower() == "true",

        client_id=f"{uuid.uuid4().hex[:8]}_{device_id}",

        subscribe_topic=f"echoscan/subscribe/{device_id}",

        device_register_topic=f"echoscan/register",
        publish_data_topic=f"echoscan/publish",
    )