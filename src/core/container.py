from typing import Dict, Any
from events.event_bus import EventBus
from externals.mqtt_client import MQTTClient
from externals.mqtt_handlers.device_registration_handler import DeviceRegistrationHandler
from core.state_manager import StateManager
import core.config as config
from externals.serial_client import SerialClient

from core.event_handlers import (
    rfid_summary_mqtt_handler, 
    device_status_mqtt_handler
)

class Container:
    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register(self, name: str, instance: Any):
        self._services[name] = instance

    def get(self, name: str) -> Any:
        if name in self._services:
            return self._services[name]
        raise ValueError(f"Service {name} not found")
    
    def setup(self):
        serial_client = SerialClient(
            port="/dev/ttyUSB0",
            baudrate=57600,
        )

        self._services["serial_client"] = serial_client

        state_manager = StateManager()
        self._services["state_manager"] = state_manager

        event_bus = EventBus()
        self._services["event_bus"] = event_bus

        mqtt_client = MQTTClient()
        self._services["mqtt_client"] = mqtt_client
        
        if not mqtt_client.connect():
            print("Warning: MQTT connection failed, continuing without MQTT...")
        
        mqtt_client.register_handler(DeviceRegistrationHandler(state_manager=state_manager))
        mqtt_client.subscribe(f"echoscan/subscribe/{config.Config.device_id}")

        event_bus.subscribe("RFID_SUMMARY_DETECTED", rfid_summary_mqtt_handler(mqtt_client, state_manager))
        event_bus.subscribe("DEVICE_STATUS_DETECTED", device_status_mqtt_handler(mqtt_client, state_manager))