"""
Wave generating library.
"""


import math


def gen_sine(freq: float, duration: float, volume: float = 1.0, rate: int = 44100) -> bytes:
    """
    Generate a sine wave.
    """
    # Convert the frequency to a number of samples.
    samples = int(rate * duration)
    # Generate the wave.
    data = []
    for i in range(samples):
        data.append(int(32767 * volume * math.sin(2 * math.pi * freq * i / rate)))
    return bytes(data)


def gen_square(freq: float, duration: float, volume: float = 1.0, rate: int = 44100) -> bytes:
    """
    Generate a square wave.
    """
    # Convert the frequency to a number of samples.
    samples = int(rate * duration)
    # Generate the wave.
    data = []
    for i in range(samples):
        data.append(int(32767 * volume * (1 if i % (rate // freq) < rate // (2 * freq) else -1)))
    return bytes(data)