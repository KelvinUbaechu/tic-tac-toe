from enum import Enum


class BoardChip(Enum):
    EMPTY = 0
    X = 1
    O = 2

    def __str__(self) -> str:
        if self is BoardChip.EMPTY:
            return ' '
        return self.name