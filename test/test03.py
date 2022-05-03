"""
pyao test module 03.
"""

import pyao

pyao.init()

with pyao.AO.open_file(
    pyao.get_default_driver_id(),
    pyao.AOFormat(
        bits=16,
        rate=44100,
        channels=2,
        byte_format=pyao.AO_FMT_NATIVE,
        mat="L,R"
    ),
    "test.wav"
) as file:
    file.play(b"\x00\x00\xff\xff\x00\x00\xff\xff")

pyao.shutdown()