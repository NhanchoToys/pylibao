"""
A set of small tools to make some simple sounds conveniently.
"""

__all__ = [
    'FastPlay',
    'fast_play_init',
    'fast_play',
    'fast_play_close',
    'fast_play_sine',
    'fast_play_square',
]

from math import pi, sin

from pyao._abstract import (
    AOFormat,
)

from pyao._aointernal import (
    pyao_fast_play_init,
    pyao_fast_play,
    pyao_fast_play_sine,
    pyao_fast_play_square,
    pyao_fast_play_close,
)


def fast_play_init(ao_format: AOFormat) -> None:
    """
    Initialize the fast play library.

    :param ao_format: The audio format.
    """
    pyao_fast_play_init(ao_format.bits, ao_format.channels, ao_format.rate, ao_format.byte_format, ao_format.mat)


def fast_play(ao_format: AOFormat, data: bytes) -> int:
    """
    Play the given data.

    :return: Status code.
    """
    return pyao_fast_play(ao_format.bits, ao_format.channels, ao_format.rate, ao_format.byte_format, ao_format.mat, data)


def fast_play_sine(ao_format: AOFormat, freq: float = 440.0, duration: float = 1.0, volume: float = 1.0):
    """
    Play a sine wave with the given frequency, duration and volume.
    """
    return pyao_fast_play_sine(freq=freq, duration=duration, volume=volume)


def fast_play_square(ao_format: AOFormat, freq: float = 440.0, duration: float = 1.0, volume: float = 1.0):
    """
    Play a square wave with the given frequency, duration and volume.
    """
    return pyao_fast_play_square(freq=freq, duration=duration, volume=volume)


def fast_play_close() -> None:
    """
    Close the fast play library.
    """
    pyao_fast_play_close()


class FastPlay:
    """
    Provides a set of methods to play some simple sounds.
    """
    def __init__(self, ao_format: AOFormat):
        """
        Initialize the FastPlay class.

        :param ao_format: The audio format.
        """
        self._ao_format = ao_format

    def __enter__(self):
        """
        Enter the with statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the with statement.
        """
        pass

    def play(self, data: bytes) -> int:
        """
        Play the given data.

        :return: Status code.
        """
        return fast_play(self._ao_format, data)

    def play_sine(self, freq: float = 440.0, duration: float = 1.0, volume: float = 1.0):
        """
        Play a sine wave with the given frequency, duration and volume.
        """
        return fast_play_sine(self._ao_format, freq, duration, volume)

    def play_square(self, freq: float = 440.0, duration: float = 1.0, volume: float = 1.0):
        """
        Play a square wave with the given frequency, duration and volume.
        """
        return fast_play_square(self._ao_format, freq, duration, volume)
