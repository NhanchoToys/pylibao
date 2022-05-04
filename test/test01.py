"""
pyao test module 01.

Basic procedure.
"""

import pyao

pyao.init()

live = pyao.open(
    pyao.get_default_driver_id(),
    pyao.AOFormat(
        bits=16,
        rate=44100,
        channels=2,
        byte_format=pyao.AO_FMT_NATIVE,
        mat="L,R"
    )
)

live.play(b"\x00\x00\xff\xff\x00\x00\xff\xff")

# live.close()

pyao.shutdown()
