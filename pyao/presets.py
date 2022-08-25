"""
Presets for pyao.
"""

import re
from pyao._abstract import AOFormat, AO_FMT_LITTLE, AO_FMT_BIG


def get_format_from_string(s: str, matrix: str = "L,R") -> AOFormat:
    """
    Get AOFormat from string.

    :param s: format string
    :param matrix: channel matrix

    :return: AOFormat
    """
    exp = re.compile(r"^[Bb](?P<bits>\d+)[Cc](?P<channels>\d+)[Rr](?P<rate>\d+)(?P<byte_format>[LB])E?$")
    m = exp.match(s)

    def err_invalid_format():
        raise ValueError(f"Invalid format string: {s}")

    if m is None:
        err_invalid_format()

    return AOFormat(
        bits=int(m.group("bits")),
        channels=int(m.group("channels")),
        rate=int(m.group("rate")),
        byte_format=AO_FMT_LITTLE if m.group("byte_format") == "L" else AO_FMT_BIG if m.group("byte_format") == "B" else err_invalid_format(),
        mat=matrix
    )
