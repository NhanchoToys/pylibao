"""
pyao test module 04.
"""

import pyao

pyao.pyao_init()

for _ in range(100):
    pyao.fast.fast_play_sine(
        pyao.default_driver_id(),
        440,
        0.75,
        1
    )

pyao.pyao_shutdown()
