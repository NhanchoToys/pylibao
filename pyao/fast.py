"""
A set of small tools to make some simple sounds conveniently.
"""

__all__ = [
    'FastPlay',
    'playbytes',
    'play2file',
    'fast_play_sine',
]

from math import pi, sin

from pyao._abstract import (
    AOFormat,
    AO
)

from pyao._aointernal import pyao_fast_play_sine

playbytes = AO.fast_play
play2file = AO.fast_play_file


def fast_play_sine(driver: int, format: AOFormat, freq: float = 440.0, duration: float = 1.0, volume: float = 1.0):
    """
    Play a sine wave with the given frequency, duration and volume.
    """
    pyao_fast_play_sine(driver, format.bits, format.channels, format.rate, format.byte_format, format.mat, freq, duration, volume)


class FastPlay:
    """
    Provides a set of methods to play some simple sounds.
    """
    @staticmethod
    def sine(drv: int, fmt: AOFormat, freq: float, volume: float, duration: float):
        """
        Generates a sine wave.
        """
        size = int(fmt.rate * duration)
        buffer = bytearray(size)
        for i in range(size):
            buffer[i] = int(volume * sin(2 * pi * freq * i / fmt.rate))
        return playbytes(drv, fmt, bytes(buffer))

    @staticmethod
    def square(drv: int, fmt: AOFormat, freq: float, volume: float, duration: float):
        """
        Generates a square wave.
        """
        size = int(fmt.rate * duration)
        buffer = bytearray(size)
        for i in range(size):
            buffer[i] = int(volume * (sin(2 * pi * freq * i / fmt.rate) > 0))
        return playbytes(drv, fmt, bytes(buffer))
