from dataclasses import asdict, is_dataclass
from typing import Any
import json


class JsonSerializer:

    @staticmethod
    def dumps(data: Any) -> bytes:

        if is_dataclass(data):
            data = asdict(data)

        return json.dumps(data).encode("utf-8")

    @staticmethod
    def loads(data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))