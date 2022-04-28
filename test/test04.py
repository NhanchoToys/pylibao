"""
pyao test module 04.
"""

import pyao

pyao.pyao_init()

pyao.AO.fast_play(
    pyao.default_driver_id(),
    pyao.AOFormat(
        bits=16,
        rate=44100,
        channels=2,
        byte_format=pyao.AO_FMT_NATIVE,
        mat="L,R"
    ),
    b"\x00\x00\xff\xff\x00\x00\xff\xff"
)

pyao.pyao_shutdown()