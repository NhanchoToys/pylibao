"""
Python libao interface.
"""

__all__ = [
    'PlaybackError',
    'ao_sample_format',
    'ao_option',
    'init',
    'shutdown',
    'get_default_driver_id',
    'AO_FMT_NATIVE',
    'AO_FMT_LITTLE',
    'AO_FMT_BIG',
    'AO_TYPE_LIVE',
    'AO_TYPE_FILE'
]

from ctypes import byref
import re
import pyao._ao as _ao
from pyao._ao import (
    PlaybackError,
    ao_sample_format,
    ao_option,
    initialize as init,
    shutdown,
    get_default_driver_id,
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
        int(m.group("channels")),
        int(m.group("rate")),
        AO_FMT_LITTLE if m.group("byte_format") == "L" else AO_FMT_BIG
        if m.group("byte_format") == "B" else err_invalid_format(),
        matrix.encode()
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

    @staticmethod
    def live(
        driver: int, format: ao_sample_format, option: ao_option = ao_option()
    ) -> "Device":
        return Device(_ao.open_live(driver, byref(format), byref(option)))

    @staticmethod
    def file(
        driver: int, format: ao_sample_format, fp: str,
        overwrite: bool = False, option: ao_option = ao_option()
    ) -> "Device":
        return Device(
            _ao.open_file(driver, fp, overwrite, byref(format), byref(option))
        )

    def play(self, data: bytes):
        c = _ao.play(self.device, data, len(data))
        if c == 0:
            raise PlaybackError("Failed to play data.")

    def close(self):
        c = _ao.close(self.device)
        if c == 0:
            raise PlaybackError("Failed to close device.")