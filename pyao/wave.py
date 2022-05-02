"""
Wave generating library.
"""

from pyao._abstract import AOFormat, AO_FMT_BIG
import math


def gen_sine(fmt: AOFormat, freq: float, duration: float, volume: float = 1.0) -> bytes:
    """
    Generate a sine wave.
    """
    samples = int(fmt.bits / 8 * fmt.channels * fmt.rate * duration)
    # Generate the wave.
    export = bytearray(samples)
    for i in range(0, samples, fmt.bits // 8 * fmt.channels):
        data = int(32768 * volume * math.sin(2 * math.pi * freq * i / fmt.rate))
        bits = [data >> (8 * j) & 0xff for j in range(fmt.bits // 8)]
        if fmt.byte_format == AO_FMT_BIG:
            bits.reverse()
        chdata = [bits] * fmt.channels
        for j in range(fmt.bits // 8 * fmt.channels):
            export[i + j] = chdata[j % fmt.channels][j // fmt.channels]
    
    # Convert the wave to bytes.
    return bytes(export)


def gen_square(fmt: AOFormat, freq: float, duration: float, volume: float = 1.0) -> bytes:
    """
    Generate a square wave.
    """
    samples = int(fmt.bits / 8 * fmt.channels * fmt.rate * duration)
    # Generate the wave.
    export = bytearray(samples)
    for i in range(0, samples, fmt.bits // 8 * fmt.channels):
        data = int(32768 * volume * math.sin(2 * math.pi * freq * i / fmt.rate))
        bits = [data >> (8 * j) & 0xff for j in range(fmt.bits // 8)]
        if fmt.byte_format == AO_FMT_BIG:
            bits.reverse()
        chdata = [bits] * fmt.channels
        for j in range(fmt.bits // 8 * fmt.channels):
            export[i + j] = chdata[j % fmt.channels][j // fmt.channels]
    
    # Convert the wave to bytes.
    return bytes(export)