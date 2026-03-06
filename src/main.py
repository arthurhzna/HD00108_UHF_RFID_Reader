from core.container import Container
from core.config import init_config
from core.pipeline import Pipeline
from feature.rfid_scanner_feature import RFIDScannerFeature
from feature.rfid_uhf.rf_power_feature import RfPowerFeature
from feature.rfid_uhf.tag_inventory_feature import TagInventoryFeature

def main():
    init_config() 

    container = Container()
    container.setup()

    serial_client = container.get("serial_client")

    rf_power_feature = RfPowerFeature(serial_client)
    tag_inventory_feature = TagInventoryFeature(serial_client)

    rfid_scanner_feature = RFIDScannerFeature(
        tag_inventory_feature=tag_inventory_feature,
        rf_power_feature=rf_power_feature,
        event_bus=container.get("event_bus"),
    )
    pipeline = Pipeline(
        rfid_scanner_feature=rfid_scanner_feature,
    )
    pipeline.run()


if __name__ == "__main__":
    main()