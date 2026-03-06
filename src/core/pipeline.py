from feature.rfid_scanner_feature import RFIDScannerFeature
from datetime import datetime

class Pipeline:
    def __init__(
        self,
        rfid_scanner_feature: RFIDScannerFeature,
    ) -> None:
        self.rfid_scanner_feature = rfid_scanner_feature

    def run(self):
        while True:
            timestamp = datetime.now()
            self.rfid_scanner_feature.process(timestamp=timestamp)