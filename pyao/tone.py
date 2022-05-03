"""
PyAO note toning tools.
"""

from math import log2

A = 440.0


class Tone:
    """
    A set of toning methods.
    """
    @staticmethod
    def from_cent(freq: float, cents: float) -> float:
        """
        Return the frequency of a note in cents.
        """
        return freq * (2 ** (cents / 1200))

    @staticmethod
    def to_cent(f0: float, freq: float) -> float:
        """
        Return the cents of a note.
        """
        return 1200 * log2(freq / f0)

    @staticmethod
    def from_tet(tet: int) -> float:
        """
        Return the cents between two notes under the given tone equal temperament.
        """
        return 1200 / tet