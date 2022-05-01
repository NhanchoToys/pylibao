"""
pyao test module 02.
"""

import pyao

pyao.pyao_init()

preset = pyao.presets.FMT_B16C2R44100LE

with pyao.AO.open_live(pyao.default_driver_id(), preset) as live:
    live.play(b"\x00\x00\xff\xff\x00\x00\xff\xff")

pyao.pyao_shutdown()
