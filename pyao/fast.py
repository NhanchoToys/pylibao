"""
A set of small tools to make some simple sounds conveniently.
"""

from math import pi, sin

from pyao._abstract import (
    AOFormat,
    AO
)

playbytes = AO.fast_play
play2file = AO.fast_play_file


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
