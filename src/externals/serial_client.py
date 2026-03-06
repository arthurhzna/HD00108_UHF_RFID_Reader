import time
from typing import Optional, Union
import serial
import core.config as config

class SerialClient:
    def __init__(
        self,
        port: Optional[str] = None,
        baudrate: Optional[int] = None,
        bytesize: int = serial.EIGHTBITS,
        parity: str = serial.PARITY_NONE,
        stopbits: int = serial.STOPBITS_ONE,
        timeout: float = 1.0,
        reconnect: bool = True,
    ) -> None:
        self.port = port or getattr(getattr(config.Config, "serial", {}), "port", None)
        self.baudrate = baudrate or getattr(
            getattr(config.Config, "serial", {}), "baudrate", 115200
        )

        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.reconnect = reconnect

        self._ser: Optional[serial.Serial] = None
        self._connected = False

    def connect(self) -> bool:
        if not self.port:
            print("Serial connection failed: port is not set")
            self._connected = False
            return False

        try:
            self._ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
            )
            if self._ser.is_open:
                self._connected = True
                print(f"Serial connection successful on {self.port} @ {self.baudrate}")
                return True

            self._connected = False
            print(f"Serial connection failed: port {self.port} is not open")
            return False
        except Exception as e:
            print(f"Serial connection failed: {e}")
            self._connected = False
            self._ser = None
            return False

    def disconnect(self) -> None:
        if self._ser is not None and self._ser.is_open:
            try:
                self._ser.close()
            except Exception as e:
                print(f"Error closing serial port: {e}")
        self._connected = False
        self._ser = None

    def ensure_connection(self) -> bool:
        if self._connected and self._ser and self._ser.is_open:
            return True
        if not self.reconnect:
            return False
        return self.connect()

    @property
    def is_connected(self) -> bool:
        return self._connected and self._ser is not None and self._ser.is_open

    def write(
        self,
        data: Union[bytes, str],
        append_newline: bool = False,
        encoding: str = "utf-8",
    ) -> bool:
        if not self.ensure_connection():
            return False

        if isinstance(data, str):
            if append_newline:
                data = data + "\r\n"
            data = data.encode(encoding)

        try:
            assert self._ser is not None
            self._ser.write(data)
            self._ser.flush()
            return True
        except Exception as e:
            print(f"Serial write error: {e}")
            self._connected = False
            return False

    def read_line(self, encoding: str = "utf-8", strip: bool = True) -> Optional[str]:
        if not self.ensure_connection():
            return None
        try:
            assert self._ser is not None
            raw = self._ser.readline()
            if not raw:
                return None
            text = raw.decode(encoding, errors="ignore")
            return text.strip() if strip else text
        except Exception as e:
            print(f"Serial readline error: {e}")
            self._connected = False
            return None

    def read_bytes(self, size: int = 1) -> Optional[bytes]:
        if not self.ensure_connection():
            return None
        try:
            assert self._ser is not None
            data = self._ser.read(size)
            return data or None
        except Exception as e:
            print(f"Serial read error: {e}")
            self._connected = False
            return None

    def flush_input(self) -> None:
        if self._ser is not None:
            try:
                self._ser.reset_input_buffer()
            except Exception as e:
                print(f"Error flushing input buffer: {e}")

    def flush_output(self) -> None:
        if self._ser is not None:
            try:
                self._ser.reset_output_buffer()
            except Exception as e:
                print(f"Error flushing output buffer: {e}")

    def __enter__(self) -> "SerialClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.disconnect()