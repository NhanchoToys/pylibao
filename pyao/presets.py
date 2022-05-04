"""
Presets for pyao.
"""

import re
from pyao._abstract import AOFormat, AO_FMT_LITTLE, AO_FMT_BIG

FMT_B16C2R44100LE = AOFormat(
    bits=16,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B16C2R44100BE = AOFormat(
    bits=16,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B16C2R48000LE = AOFormat(
    bits=16,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B16C2R48000BE = AOFormat(
    bits=16,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B16C2R96000LE = AOFormat(
    bits=16,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B16C2R96000BE = AOFormat(
    bits=16,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B24C2R44100LE = AOFormat(
    bits=24,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B24C2R44100BE = AOFormat(
    bits=24,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B24C2R48000LE = AOFormat(
    bits=24,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B24C2R48000BE = AOFormat(
    bits=24,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B24C2R96000LE = AOFormat(
    bits=24,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B24C2R96000BE = AOFormat(
    bits=24,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B32C2R44100LE = AOFormat(
    bits=32,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B32C2R44100BE = AOFormat(
    bits=32,
    channels=2,
    rate=44100,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B32C2R48000LE = AOFormat(
    bits=32,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B32C2R48000BE = AOFormat(
    bits=32,
    channels=2,
    rate=48000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)
FMT_B32C2R96000LE = AOFormat(
    bits=32,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_LITTLE,
    mat="L,R"
)
FMT_B32C2R96000BE = AOFormat(
    bits=32,
    channels=2,
    rate=96000,
    byte_format=AO_FMT_BIG,
    mat="L,R"
)


def get_format_from_string(s: str, matrix: str = "L,R") -> AOFormat:
    """
    Get AOFormat from string.

    :param s: format string
    :param matrix: channel matrix

    :return: AOFormat
    """
    exp = re.compile(r"^[Bb](?P<bits>\d+)[Cc](?P<channels>\d+)[Rr](?P<rate>\d+)[Ll](?P<byte_format>[LB])E?$")
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