"""
Wave generating library.
"""

from pyao._abstract import AOFormat
from pyao._aointernal import pyao_gen_sine, pyao_gen_square
import math


def gen_sine(fmt: AOFormat, freq: float, duration: float, volume: float = 1.0) -> bytes:
    """
    Generate a sine wave.
    """
    return pyao_gen_sine(fmt.bits, fmt.channels, fmt.rate, fmt.byte_format, freq, duration, volume)


def gen_square(fmt: AOFormat, freq: float, duration: float, volume: float = 1.0) -> bytes:
    """
    Generate a square wave.
    """
    return pyao_gen_square(fmt.bits, fmt.channels, fmt.rate, fmt.byte_format, freq, duration, volume)