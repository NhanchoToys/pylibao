"""
An abstract interface for libao.
"""

from dataclasses import dataclass
from typing import NoReturn, Optional, Union
from pyao import _aointernal, presets


AO_FMT_NATIVE: int = _aointernal.AO_FMT_NATIVE
AO_FMT_LITTLE: int = _aointernal.AO_FMT_LITTLE
AO_FMT_BIG: int = _aointernal.AO_FMT_BIG


class PlaybackError(Exception):
    """
    Raised when an audio playback error occurs.
    """
    pass


@dataclass(frozen=True)
class AOFormat:
    """
    An abstract object to mark ao_sample_format
    
    :param bits: The number of bits per sample.
    :param rate: The sample rate.
    :param channels: The number of channels.
    :param byte_format: The byte format.
    :param mat: The matrix for multi-channel audio.
    """
    bits: int
    rate: int
    channels: int
    byte_format: int
    mat: str


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
    drvid = _aointernal.pyao_default_driver_id()
    if drvid == -1:
        raise RuntimeError("No default audio driver found. Have you initialized the audio library?")
    return drvid


def pyao_open_live(driver: int, fmt: AOFormat) -> int:
    """
    Open a live audio stream.

    :param driver: The audio driver ID.
    :param fmt: The audio format.

    :return: The audio device descriptor.
    """
    return _aointernal.pyao_open_live(driver, fmt.bits, fmt.channels, fmt.rate, fmt.byte_format, fmt.mat)


def pyao_open_file(driver: int, file: str, fmt: AOFormat, overwrite: bool = False) -> int:
    """
    Open a file audio stream.

    :param driver: The audio driver ID.
    :param file: The file path.
    :param fmt: The audio format.
    :param overwrite: Overwrite the file if it exists.

    :return: The audio device descriptor.
    """
    return _aointernal.pyao_open_file(driver, file, fmt.bits, fmt.channels, fmt.rate, fmt.byte_format, fmt.mat, int(overwrite))


def pyao_close(stream: int) -> Union[None, NoReturn]:
    """
    Close an audio stream.

    :param stream: The audio device descriptor.
    """
    if _aointernal.pyao_close(stream):
        raise PlaybackError("Error closing audio stream.")


def pyao_play(stream: int, data: bytes) -> Union[None, NoReturn]:
    """
    Play audio data.

    :param stream: The audio device descriptor.
    :param data: The audio data.
    """
    if _aointernal.pyao_play(stream, data):
        raise PlaybackError("Error playing audio data.")



class AODevice:
    """
    An abstract object to mark ao_device
    """
    def __init__(self, st: int, fmt: AOFormat):
        """
        :param st: The audio device descriptor.
        :param fmt: The audio format.
        """
        self._struct = st
        self.format = fmt

    def __del__(self):
        self.close()
        super().__del__()  # type: ignore

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def play(self, data: bytes):
        """
        Play audio data.

        :param data: The audio data.

        :return: Status code.
        """
        pyao_play(self._struct, data)

    def close(self):
        """
        Close the audio device.
        """
        # Disabled due to some error.
        # return pyao_close(self._struct)


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

        :param driver: The audio driver ID.
        :param format: The audio format.
        """
        if driver is None:
            driver = pyao_default_driver_id()
        if format is None:
            format = presets.FMT_B16C2R44100LE
        return AODevice(pyao_open_live(driver, format), format)

    @staticmethod
    def open_file(
        driver: Optional[int] = None,
        file: Optional[str] = None,
        format: Optional[AOFormat] = None,
        overwrite: Optional[bool] = False
    ) -> AODevice:
        """
        Open a file audio stream.

        :param driver: The audio driver ID.
        :param file: The file path.
        :param format: The audio format.
        :param overwrite: Whether to overwrite the file if it exists.
        """
        if driver is None:
            driver = pyao_default_driver_id()
        if format is None:
            format = presets.FMT_B16C2R44100LE
        if file is None:
            raise ValueError("No file specified.")
        if overwrite is None:
            overwrite = False
        return AODevice(pyao_open_file(driver, file, format, overwrite), format)