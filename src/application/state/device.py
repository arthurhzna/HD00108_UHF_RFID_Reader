from threading import Lock


class DeviceState:

    def __init__(self) -> None:
        self._registered = False
        self._lock = Lock()

    def is_registered(self) -> bool:

        with self._lock:
            return self._registered

    def register(self) -> None:

        with self._lock:
            self._registered = True

    def unregister(self) -> None:

        with self._lock:
            self._registered = False