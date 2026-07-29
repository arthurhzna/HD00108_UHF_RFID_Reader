from dataclasses import dataclass, field
from presentation.messaging.handler import MessageHandler

@dataclass
class MessageRouter:
    _handlers: dict[
        str,
        MessageHandler,
    ] = field(
        default_factory=dict,
    )

    def register(
        self,
        route: str,
        handler: MessageHandler,
    ) -> None:
        self._handlers[route] = handler

    def dispatch(
        self,
        route: str,
        payload: bytes,
    ) -> None:
        handler = self._handlers.get(route)

        if handler is None:
            return

        handler.handle(
            route,
            payload,
        )