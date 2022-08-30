"""
pyao test module 05.

Play test.wav.
"""

import pyao
import wave

with pyao.Device.live(
    pyao.get_default_driver_id(),
    pyao.preset.B16C2R44100LE
) as player:
    with wave.open("test.wav", "rb") as f:
        for i in range(f.getnframes() // 48 + 1):
            player.play(f.readframes(48))
