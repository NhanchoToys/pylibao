"""
pyao test module 02.

Play with context manager.
"""

import pyao

preset = pyao.preset.b16c2r44100L

with pyao.open(pyao.get_default_driver_id(), preset) as live:
    live.play(b"\x00\x00\xff\xff\x00\x00\xff\xff")
