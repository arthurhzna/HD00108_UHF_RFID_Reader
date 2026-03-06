from feature.rfid_uhf.rf_power_feature import RfPowerFeature
from feature.rfid_uhf.tag_inventory_feature import TagInventoryFeature
from utils.parse_data import parse_data_tag_inventory
from domain.models.rfid import RFIDSummaryData
from datetime import datetime
import core.config as config
from events.device_status_event import DeviceStatusEvent
from events.rfid_summary_event import RFIDSummaryEvent
from events.event_bus import EventBus

class RFIDScannerFeature:

    def __init__(
        self,
        rf_power_feature: RfPowerFeature,
        tag_inventory_feature: TagInventoryFeature,
        event_bus: EventBus,
    ):
        self.tag_inventory_feature = tag_inventory_feature
        self.rf_power_feature = rf_power_feature
        self.rfid_summary_data = RFIDSummaryData()
        self.set_rf_power_state = False
        self.event_bus = event_bus
        self.send_every_minute : set[str] = {
            f"{hour:02d}:{minute:02d}"
            for hour in range(24)
            for minute in range(60)
        }
        self.send_every_hour = self.send_every_minute.copy()
        # self.send_every_hour: set[str] = {
        #     f"{hour:02d}:01" for hour in range(24)
        # }

    def process(self, timestamp: datetime):
        if not self.set_rf_power_state:
            data = self.rf_power_feature.set_all_rf_power_to_max()
            if data:
                print("RF power set to max")
                self.set_rf_power_state = True
            else:
                print("Failed to set RF power to max")
                return None

        data = self.tag_inventory_feature.get_tag_inventory()
        if data:
            print("Tag inventory:")
            
            tags = parse_data_tag_inventory(data)
            print(tags)

            self.rfid_summary_data.cards.update(tags)

            print("Unique tags:")
            print(self.rfid_summary_data.cards)
        else:
            print("Failed to get tag inventory")
            return None

        current_hhmm = timestamp.strftime("%H:%M")

        if current_hhmm in self.send_every_minute:
            device_event = DeviceStatusEvent(
                event_type="DEVICE_STATUS_DETECTED",  
                action="device_status",
                device_id=config.Config.device_id,
                nama="RFID Scanner",
                timestamp=timestamp.isoformat(),
            )
            self.event_bus.publish(event=device_event)

        if current_hhmm in self.send_every_hour:
            summary_event = RFIDSummaryEvent(
                event_type="RFID_SUMMARY_DETECTED", 
                device_id=config.Config.device_id,
                timestamp=timestamp.isoformat(),
                cards=list(self.rfid_summary_data.cards),
            )
            self.event_bus.publish(event=summary_event)
            self.rfid_summary_data.cards.clear()
