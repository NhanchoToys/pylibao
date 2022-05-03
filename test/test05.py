"""
pyao test module 05.
"""

import pyao

pyao.pyao_init()

with pyao.AO.open_live(
    pyao.default_driver_id(),
    pyao.presets.FMT_B16C2R44100LE
) as player:
    with open("test.wav", "rb") as f:
        while True:
            player.play(f.read(128))

pyao.pyao_shutdown()
