from application.state.container import States

from domain.service.clock import Clock
from domain.service.publisher import Publisher


class DeviceUseCase:

    def __init__(
        self,
        publisher: Publisher,
        states: States,
        clock: Clock,
    ) -> None:

        self._publisher = publisher
        self._states = states
        self._clock = clock

    def sync(self) -> None:

        timestamp = self._clock.now()

        if not self._states.device.is_registered():

            self._publisher.publish_device_register(
                timestamp=timestamp,
            )

            return

        self._publisher.publish_device_status(
            timestamp=timestamp,
        )

    def register(self) -> None:

        self._states.device.register()

    def unregister(self) -> None:

        self._states.device.unregister()