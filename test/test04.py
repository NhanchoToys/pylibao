"""
pyao test module 04.
"""

import pyao

pyao.pyao_init()

for _ in range(100):
    pyao.fast.FastPlay.sine(
        pyao.default_driver_id(),
        pyao.AOFormat(
            bits=16,
            rate=44100,
            channels=2,
            byte_format=pyao.AO_FMT_NATIVE,
            mat="L,R"
        ),
        440,
        0.75,
        1
    )

pyao.pyao_shutdown()
