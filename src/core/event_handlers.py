from externals.mqtt_client import MQTTClient
from events.rfid_summary_event import RFIDSummaryEvent
from events.device_status_event import DeviceStatusEvent
from typing import Callable
from core.state_manager import StateManager
import core.config as config
from domain.dto.rfid import RFIDSummary_MQTT_Output
from domain.dto.device import DeviceStatus_MQTT_Output
from domain.dto.device import DeviceRegist_MQTT_Output

def rfid_summary_mqtt_handler(
    mqtt_client: MQTTClient,
    state_manager: StateManager
) -> Callable[[RFIDSummaryEvent], None]:
    def handle(event: RFIDSummaryEvent):
        if not state_manager.get_device_registration_state():
            return
        print(f"[RFID_SUMMARY] Sending RFID summary to MQTT for device_id={event.device_id}")
        payload = RFIDSummary_MQTT_Output(
            action="rfid_summary",
            id=event.device_id,
            timestamp=event.timestamp,
            cards=event.cards,
        ).to_json()
        mqtt_client.publish(
            topic=f"echoscan/publish/{config.Config.device_id}",
            payload=payload,
        )
    return handle

def device_status_mqtt_handler(
    mqtt_client: MQTTClient,
    state_manager: StateManager
) -> Callable[[DeviceStatusEvent], None]:
    def handle(event: DeviceStatusEvent):
        print(f"state_manager.get_device_registration_state(): {state_manager.get_device_registration_state()}")
        if not state_manager.get_device_registration_state():
            print(f"[DEVICE_REGIST] Device not registered for device_id={event.device_id}")
            payload = DeviceRegist_MQTT_Output(
                action="device_registered",
                id=event.device_id,
                timestamp=event.timestamp,
            ).to_json()
            mqtt_client.publish(
                topic=f"echoscan/register",
                payload=payload,
            )
            return
        print(f"[DEVICE_STATUS] Device status registered for device_id={event.device_id}")
        payload = DeviceStatus_MQTT_Output(
            action="device_status",
            id=event.device_id,
            timestamp=event.timestamp,
            software_version=event.software_version,
        ).to_json()
        mqtt_client.publish(
            topic=f"echoscan/publish",
            payload=payload,
        )
    return handle