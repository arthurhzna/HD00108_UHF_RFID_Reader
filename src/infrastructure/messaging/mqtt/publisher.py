from __future__ import annotations

from config.config import Config

from infrastructure.messaging.mqtt.action import MQTTAction
from infrastructure.messaging.mqtt.messages.device_register import (
    DeviceRegisterMessage,
)
from infrastructure.messaging.mqtt.messages.device_status import (
    DeviceStatusMessage,
)
from infrastructure.messaging.mqtt.messages.rfid_summary import (
    RFIDSummaryMessage,
)
from infrastructure.messaging.mqtt.mqtt_client import MqttClient
from infrastructure.serializer.json_serializer import JsonSerializer


class MqttPublisher:

    def __init__(
        self,
        client: MqttClient,
        config: Config,
    ) -> None:

        self._client = client
        self._serializer = JsonSerializer()
        self._config = config

    def publish_device_register(
        self,
        timestamp: str,
    ) -> None:

        message = DeviceRegisterMessage(
            action=MQTTAction.DEVICE_REGISTER,
            id=self._config.device.device_id,
            timestamp=timestamp,
        )

        self._client.publish(
            topic=self._config.mqtt.device_register_topic,
            payload=self._serializer.dumps(message),
        )

        print(f"Published device register message: {self._serializer.dumps(message)}")

    def publish_device_status(
        self,
        timestamp: str,
    ) -> None:

        message = DeviceStatusMessage(
            action=MQTTAction.DEVICE_STATUS,
            id=self._config.device.device_id,
            timestamp=timestamp,
            firmware_version=self._config.device.software_version,
        )

        self._client.publish(
            topic=self._config.mqtt.publish_data_topic,
            payload=self._serializer.dumps(message),
        )
        print(f"Published device status message: {self._serializer.dumps(message)}")

    def publish_rfid_summary(
        self,
        timestamp: str,
        cards: list[str],
    ) -> None:

        message = RFIDSummaryMessage(
            action=MQTTAction.RFID_SUMMARY,
            id=self._config.device.device_id,
            timestamp=timestamp,
            cards=cards,
        )

        self._client.publish(
            topic=self._config.mqtt.publish_data_topic,
            payload=self._serializer.dumps(message),
        )
        print(f"Published RFID summary message: {self._serializer.dumps(message)}")