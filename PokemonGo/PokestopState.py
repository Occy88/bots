from enum import Enum


class PokestopState(Enum):
    AVAILABLE = 0,
    COOL_DOWN = 1,
    TOO_FAR = 2
