from __future__ import annotations
from dataclasses import dataclass

from infrastructure.messaging.mqtt.mqtt_client import (
    MqttClient,
)
from infrastructure.serial.serial_client import (
    SerialClient,
)

from config.config import load_config

from bootstrap.mqtt import (
    build_mqtt_client,
    initialize_mqtt,
)
from bootstrap.rfid import (
    build_uhf_rfid,
)
from bootstrap.serial import (
    build_serial_client,
)

from application.scheduler.scheduler import (
    Scheduler,
)

from application.scheduler.trigger.every_second import (
    EverySecond,
)

from application.state.card import (
    CardState,
)
from application.state.device import (
    DeviceState,
)

from application.state.container import (
    States,
)

from application.usecase.container import (
    UseCases,
)
from application.usecase.device import (
    DeviceUseCase,
)
from application.usecase.rfid import (
    RFIDUseCase,
)

from infrastructure.messaging.mqtt.publisher import (
    MqttPublisher,
)
from infrastructure.serializer.json_serializer import (
    JsonSerializer,
)
from infrastructure.time.system_clock import (
    SystemClock,
)

@dataclass(slots=True)
class App:

    mqtt: MqttClient

    scheduler: Scheduler

    serial: SerialClient


def build_app() -> App:
    config = load_config()

    clock = SystemClock()

    states = States(
        device=DeviceState(),
        card=CardState(),
    )

    serial_client = build_serial_client(
        config=config.serial,
    )

    mqtt_client = build_mqtt_client(
        config=config.mqtt,
    )

    publisher = MqttPublisher(
        client=mqtt_client,
        config=config,
    )

    uhf_rfid = build_uhf_rfid(
        serial=serial_client,
    )

    usecases = UseCases(
        device=DeviceUseCase(
            publisher=publisher,
            states=states,
            clock=clock,
        ),
        rfid=RFIDUseCase(
            rfid=uhf_rfid,
            publisher=publisher,
            clock=clock,
            states=states,
        ),
    )

    initialize_mqtt(
        client=mqtt_client,
        config=config,
        usecases=usecases,
    )

    scheduler = Scheduler(
        clock=clock,
        status_trigger=EverySecond(
            second=1,
        ),
        send_data_trigger=EverySecond(
            second=1,
        ),
        states=states,
        usecases=usecases,
    )

    return App(
        mqtt=mqtt_client,
        scheduler=scheduler,
        serial=serial_client,
    )