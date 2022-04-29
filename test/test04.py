"""
pyao test module 04.
"""

import pyao

pyao.pyao_init()

for _ in range(1000):
    pyao.AO.fast_play(
        pyao.default_driver_id(),
        pyao.AOFormat(
            bits=16,
            rate=44100,
            channels=2,
            byte_format=pyao.AO_FMT_NATIVE,
            mat="L,R"
        ),
        b"\x00\x00\x00\x00\xff\xff\xff\xff" * 200
    )

pyao.pyao_shutdown()
