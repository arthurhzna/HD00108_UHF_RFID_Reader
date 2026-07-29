from config.config import Config
from config.mqtt import MQTTConfig

from application.usecase.container import (
    UseCases,
)

from infrastructure.messaging.mqtt.mqtt_client import (
    MqttClient,
)

from presentation.messaging.message_router import (
    MessageRouter,
)

from presentation.messaging.mqtt.handler.device_registration import (
    DeviceRegistrationMessageHandler,
)

from presentation.messaging.mqtt.mqtt_consumer import (
    MqttConsumer,
)


def build_mqtt_client(
    config: MQTTConfig,
) -> MqttClient:
    return MqttClient(
        config=config,
    )


def initialize_mqtt(
    client: MqttClient,
    config: Config,
    usecases: UseCases,
) -> None:
    router = MessageRouter()

    router.register(
        route=config.mqtt.subscribe_topic,
        handler=DeviceRegistrationMessageHandler(
            usecase=usecases.device,
        ),
    )

    consumer = MqttConsumer(
        on_message=router.dispatch,
    )

    client.on_message = consumer.handle

    client.subscribe(
        topics=[
            (
                config.mqtt.subscribe_topic,
                0,
            ),
        ],
    )