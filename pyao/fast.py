"""
A set of small tools to make some simple sounds conveniently.
"""

from pyao._abstract import (
    AOFormat,
    AO
)

playbytes = AO.fast_play
play2file = AO.fast_play_file


class FastPlay:
    @staticmethod
    def sine(fmt: AOFormat, freq: float, volume: float, duration: float):
        pass

    @staticmethod
    def square(fmt: AOFormat, freq: float, volume: float, duration: float):
        pass
