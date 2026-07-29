from __future__ import annotations

import json

from application.usecase.device import (
    DeviceUseCase,
)

from presentation.messaging.mqtt.action import (
    MQTTAction,
)
from presentation.messaging.handler import MessageHandler


class DeviceRegistrationMessageHandler(MessageHandler):

    def __init__(
        self,
        usecase: DeviceUseCase,
    ) -> None:

        self._usecase = usecase

    def handle(
        self,
        topic: str,
        payload: bytes,
    ) -> None:

        body = json.loads(payload)

        action = body.get(
            "action",
        )
        print(f"Received message on topic '{topic}': {body}")

        if action == MQTTAction.DEVICE_REGISTERED:

            self._usecase.register()

        elif action == MQTTAction.DEVICE_RESET:

            self._usecase.unregister()