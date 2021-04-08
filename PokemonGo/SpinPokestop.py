from enum import Enum


class Spin(Enum):
    """
    Response codes for effect of spin on pokestop.

    SUCCESS: pokestop spun successfully
    FAIL: pokestop can't be spun (cooldown try again later etc...)
    ERROR: pokestop can't be detected.
    """
    SUCCESS = 1,
    ALREADY_SPUN=2
    FAIL=3,
    ERROR = 3,


def spin():
    """
    Spins a pokestop, assumes it is in the center of the screen,
    Detects the message response, Returns said response.
    :return: CODE for response
    """
