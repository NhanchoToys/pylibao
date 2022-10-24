"""
pyao test module 01.

Basic procedure.
"""

import pyao

live = pyao.Device.open(
    pyao.get_default_driver_id(),
    pyao.preset.b16c2r44100L
)

for _ in range(1048576):
    live.play(b"\x00\x00\xff\xff\x00\x00\xff\xff")

live.close()  # commented as it causes an error
