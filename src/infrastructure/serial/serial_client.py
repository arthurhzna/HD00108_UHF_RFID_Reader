from __future__ import annotations

import serial

from config.serial import SerialConfig

class SerialClient():

    def __init__(
        self,
        config: SerialConfig,
    ) -> None:

        self._config = config
        self._serial: serial.Serial | None = None

    def connect(self) -> bool:

        if self.is_connected():
            return True

        if not self._config.port:
            return False

        try:
            self._serial = serial.Serial(
                port=self._config.port,
                baudrate=self._config.baudrate,
                timeout=self._config.timeout,
            )

            return self.is_connected()

        except Exception:
            self._serial = None
            return False

    def disconnect(self) -> None:

        if (
            self._serial is not None
            and self._serial.is_open
        ):
            self._serial.close()

        self._serial = None

    def is_connected(self) -> bool:

        return (
            self._serial is not None
            and self._serial.is_open
        )

    def write(
        self,
        data: bytes,
    ) -> bool:

        if not self._ensure_connection():
            return False

        try:
            self._serial.write(data)
            self._serial.flush()
            return True

        except Exception:
            self.disconnect()
            return False

    def readline(
        self,
    ) -> bytes | None:

        if not self._ensure_connection():
            return None

        try:
            data = self._serial.readline()
            return data if data else None

        except Exception:
            self.disconnect()
            return None

    def read(
        self,
        size: int = 1,
    ) -> bytes | None:

        if not self._ensure_connection():
            return None

        try:
            data = self._serial.read(size)
            return data if data else None

        except Exception:
            self.disconnect()
            return None

    def read_bytes(
        self,
        size: int,
    ) -> bytes | None:

        if not self._ensure_connection():
            return None

        try:
            data = self._serial.read(size)
            return data if data else None

        except Exception:
            self.disconnect()
            return None

    def flush(self) -> None:

        if not self.is_connected():
            return

        try:
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()

        except Exception:
            self.disconnect()

    def _ensure_connection(self) -> bool:

        if self.is_connected():
            return True

        if not self._config.reconnect:
            return False

        return self.connect()