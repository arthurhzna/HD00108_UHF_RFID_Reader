from abc import ABC, abstractmethod


class RFID(ABC):

    @abstractmethod
    def set_rf_power_to_max(self) -> bool:
        ...

    @abstractmethod
    def inventory(self) -> list[str]:
        ...