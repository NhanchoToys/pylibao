"""
An abstract interface for libao.
"""

from dataclasses import dataclass
from typing import Optional
from pyao import _aointernal


AO_FMT_NATIVE: int = _aointernal.AO_FMT_NATIVE
AO_FMT_LITTLE: int = _aointernal.AO_FMT_LITTLE
AO_FMT_BIG: int = _aointernal.AO_FMT_BIG


def pyao_init():
    """
    Initialize the audio library.
    """
    _aointernal.pyao_init()


def pyao_shutdown():
    """
    Shutdown the audio library.
    """
    _aointernal.pyao_shutdown()


def pyao_default_driver_id() -> int:
    """
    Return the default audio driver ID.
    """
    return _aointernal.pyao_default_driver_id()


def pyao_open_live(
    driver: int,
    bits: int,
    chs: int,
    rate: int,
    bfmt: int,
    matrix: str
) -> bytes:
    """
    Open a live audio stream.
    """
    return _aointernal.pyao_open_live(driver, bits, chs, rate, bfmt, matrix)


def pyao_open_file(
    driver: int,
    file: str,
    bits: int,
    chs: int,
    rate: int,
    bfmt: int,
    matrix: str,
    overwrite: int
) -> bytes:
    """
    Open a file audio stream.
    """
    return _aointernal.pyao_open_file(driver, file, bits, chs, rate, bfmt, matrix, overwrite)


def pyao_close(stream: bytes) -> int:
    """
    Close an audio stream.
    """
    return _aointernal.pyao_close(stream)


def pyao_play(stream: bytes, data: bytes) -> int:
    """
    Play audio data.
    """
    return _aointernal.pyao_play(stream, data)


class AODevice:
    """
    An abstract object to mark ao_device
    """
    def __init__(self, st: bytes):
        self._struct = st

    def __del__(self):
        pyao_close(self._struct)


@dataclass
class AOFormat:
    """
    An abstract object to mark ao_sample_format
    """
    bits: int
    rate: int
    channels: int
    byte_format: int
    mat: str


class AO:
    """
    An abstract interface for libao.
    """
    @staticmethod
    def open_live(
        driver: Optional[int] = None,
        format: Optional[AOFormat] = None
    ) -> AODevice:
        """
        Open a live audio stream.
        """
        if driver is None:
            driver = pyao_default_driver_id()
        if format is None:
            format = AOFormat(16, 44100, 2, AO_FMT_NATIVE, "L,R")
        return AODevice(pyao_open_live(
            driver, format.bits, format.channels, format.rate, format.byte_format, format.mat
        ))