"""
pyao test module 05.
"""

import pyao
import wave

pyao.init()

with pyao.AO.open_live(
    pyao.get_default_driver_id(),
    pyao.presets.FMT_B16C2R44100LE
) as player:
    with wave.open("test.wav", "rb") as f:
        for i in range(f.getnframes() // 48 + 1):
            player.play(f.readframes(48))

pyao.shutdown()
