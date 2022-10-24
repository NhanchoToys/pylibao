"""
An abstract interface for libao.
"""

from ctypes import CDLL, POINTER, Structure, c_char_p, c_int
from ctypes.util import find_library
from dataclasses import dataclass
from pyao._ao_c import (
    pyao_open_live as open_live,
    pyao_close as close,
    pyao_play as play
)

# errno
AO_ENODRIVER = 1
AO_ENOTFILE = 2
AO_ENOTLIVE = 3
AO_EBADOPTION = 4
AO_EOPENDEVICE = 5
AO_EOPENFILE = 6
AO_EFILEEXISTS = 7
AO_EBADFORMAT = 8
AO_EFAIL = 100

# format
AO_FMT_LITTLE = 1
AO_FMT_BIG = 2
AO_FMT_NATIVE = 4

# type
AO_TYPE_LIVE = 1
AO_TYPE_FILE = 2

if (_lib := find_library("ao")) is None:
    raise FileNotFoundError("libao not found.")

libao = CDLL(_lib)


class PlaybackError(Exception):
    """
    Raised when an audio playback error occurs.
    """
    pass


class ao_info(Structure):
    """
    An abstract object to mark ao_info.
    This object is created internally.
    """
    _fields_ = (
        ("type", c_int),
        ("name", c_char_p),
        ("short_name", c_char_p),
        ("comment", c_char_p),
        ("preferred_byte_format", c_int),
        ("priority", c_int),
        ("options", POINTER(c_char_p)),
        ("option_count", c_int)
    )


@dataclass
class ao_sample_format:
    """
    An abstract object to mark ao_sample_format

    :param bits: The number of bits per sample.
    :param rate: The sample rate.
    :param channels: The number of channels.
    :param byte_format: The byte format.
    :param matrix: The matrix for multi-channel audio.
    """
    bits: int
    rate: int
    channels: int
    byte_format: int
    matrix: str


# library initialize/shutdown
initialize = libao.ao_initialize

shutdown = libao.ao_shutdown

# device setup/playback/teardown
append_global_option = libao.ao_append_global_option
append_global_option.argtypes = [c_char_p, c_char_p]

# as ao_open_live doesn't work well with ctypes, it has been moved to `pyao/_ao_c.c`

# driver information
driver_id = libao.ao_driver_id
driver_id.argtypes = [c_char_p]

default_driver_id = libao.ao_default_driver_id

driver_info = libao.ao_driver_info
driver_info.argtypes = [c_int]
driver_info.restype = POINTER(ao_info)

driver_info_list = libao.ao_driver_info_list
driver_info_list.argtypes = [POINTER(c_int)]
driver_info_list.restype = POINTER(POINTER(ao_info))

file_extension = libao.ao_file_extension
file_extension.argtypes = [c_int]
file_extension.restype = c_char_p

# misc
is_big_endian = libao.ao_is_big_endian


def get_default_driver_id() -> int:
    """
    Return the default audio driver ID.
    """
    drvid = default_driver_id()
    if drvid == -1:
        raise RuntimeError(
            "No default audio driver found. "
            "Have you initialized the audio library?"
        )
    return drvid