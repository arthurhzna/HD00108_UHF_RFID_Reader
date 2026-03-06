from typing import List, Dict, Any, Optional
from threading import Lock
from dataclasses import dataclass, field


@dataclass
class DeviceState:
    is_registered: bool = False

class StateManager:
    def __init__(self):
        self._lock : Lock = Lock()
        self._device_state : DeviceState = DeviceState()
    
    def update_device_registration(self, is_registered: bool) -> None:
        with self._lock:
            self._device_state.is_registered = is_registered
    
    def get_device_registration_state(self) -> DeviceState:
        with self._lock:
            return self._device_state.is_registered
    
