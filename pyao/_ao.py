"""
An abstract interface for libao.
"""

from ctypes import CDLL, POINTER, Structure, c_char_p, c_int, c_uint32
from ctypes.util import find_library
from typing import NoReturn, Optional, Union

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


class ao_device(Structure):
    """
    An abstract object to mark ao_device.
    This object is always used in pointer.
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


class ao_option(Structure):
    """
    An abstract object to mark ao_option.

    :param key: The key of option.
    :param value: The value of the option.
    :param next: The next pair of key-values
    """
    pass


ao_option._fields_ = (
    ("key", c_char_p),
    ("value", c_char_p),
    ("next", POINTER(ao_option))
)


class ao_sample_format(Structure):
    """
    An abstract object to mark ao_sample_format

    :param bits: The number of bits per sample.
    :param rate: The sample rate.
    :param channels: The number of channels.
    :param byte_format: The byte format.
    :param matrix: The matrix for multi-channel audio.
    """
    _fields_ = (
        ("bits", c_int),
        ("rate", c_int),
        ("channels", c_int),
        ("byte_format", c_int),
        ("matrix", c_char_p)
    )


# library setup/teardown
initialize = libao.ao_initialize

shutdown = libao.ao_shutdown

# device setup/playback/teardown
append_global_option = libao.ao_append_global_option
append_global_option.argtypes = [c_char_p, c_char_p]

open_live = libao.ao_open_live
open_live.argtypes = [c_int, POINTER(ao_sample_format), POINTER(ao_option)]
open_live.restype = POINTER(ao_device)

open_file = libao.ao_open_file
open_file.argtypes = [
    c_int, c_char_p, c_int, POINTER(ao_sample_format), POINTER(ao_option)
]
open_file.restype = POINTER(ao_device)

play = libao.ao_play
play.argtypes = [POINTER(ao_device), c_char_p, c_uint32]

close = libao.ao_close
close.argtypes = [POINTER(ao_device)]

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


def get_default_driver_id() -> Union[int, NoReturn]:
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


def gen_option(**kwargs: str):
    prev: Optional[ao_option] = None
    head: Optional[ao_option] = None
    for k, v in kwargs:
        opt = ao_option(k, v, None)
        if not head:
            head = opt
        if prev:
            prev.next = opt
        else:
            prev = opt
    if head is None:
        head = ao_option()
    return head