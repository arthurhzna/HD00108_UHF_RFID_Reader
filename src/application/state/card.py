from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CardState:

    _cards: set[str] = field(
        default_factory=set,
    )

    def add(
        self,
        cards: list[str],
    ) -> None:

        self._cards.update(cards)

    def snapshot(
        self,
    ) -> list[str]:

        return list(self._cards)

    def clear(
        self,
    ) -> None:

        self._cards.clear()