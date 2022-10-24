"""
Python libao interface.
"""

__all__ = [
    'PlaybackError',
    'ao_sample_format',
    'init',
    'shutdown',
    'get_default_driver_id',
    'get_driver_id',
    'AO_FMT_NATIVE',
    'AO_FMT_LITTLE',
    'AO_FMT_BIG',
    'AO_TYPE_LIVE',
    'AO_TYPE_FILE'
]

from ctypes import pointer
import re
import pyao._ao as _ao
from pyao._ao import (
    PlaybackError,
    ao_sample_format,
    initialize as init,
    shutdown,
    get_default_driver_id,
    driver_id as _driver_id,
    AO_FMT_NATIVE,
    AO_FMT_LITTLE,
    AO_FMT_BIG,
    AO_TYPE_LIVE,
    AO_TYPE_FILE
)

import atexit

init()
atexit.register(shutdown)


def get_format_from_string(s: str, matrix: str = "L,R") -> ao_sample_format:
    """
    Get ao_sample_format from string.

    :param s: format string
    :param matrix: channel matrix

    :return: ao_sample_format
    """
    exp = re.compile(
        r"^[Bb](?P<bits>\d+)[Cc](?P<channels>\d+)"
        r"[Rr](?P<rate>\d+)(?P<byte_format>[LB])E?$"
    )
    m = exp.match(s)

    def err_invalid_format():
        raise ValueError(f"Invalid format string: {s}")

    if m is None:
        err_invalid_format()

    return ao_sample_format(
        int(m.group("bits")),
        int(m.group("rate")),
        int(m.group("channels")),
        AO_FMT_LITTLE if m.group("byte_format") == "L" else AO_FMT_BIG
        if m.group("byte_format") == "B" else err_invalid_format(),
        matrix
    )


class _preset:
    def __getattribute__(self, __name: str) -> ao_sample_format:
        return get_format_from_string(__name)


preset = _preset()


class Device:
    def __init__(self, device) -> None:
        self.device = device

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    @classmethod
    def open(cls, driver: int, format: ao_sample_format) -> "Device":
        return cls(_ao.open_live(driver, format.bits, format.rate, format.channels, format.byte_format, format.matrix))

    def play(self, data: bytes):
        c = _ao.play(self.device, data, len(data))
        if c == 0:
            raise PlaybackError("Failed to play data.")

    def close(self):
        _ao.close(self.device)
        # if c == 0:
        #     raise PlaybackError("Failed to close device.")


def get_driver_id(name: str) -> int:
    return _driver_id(name.encode())