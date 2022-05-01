"""
Presets for pyao.
"""

from pyao import AOFormat, AO_FMT_LITTLE, AO_FMT_BIG

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
