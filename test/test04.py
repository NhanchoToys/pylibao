"""
pyao test module 04.
"""

import pyao

pyao.pyao_init()

with pyao.fast.FastPlay(
    pyao.AOFormat(
        16,
        2,
        44100,
        pyao.AO_FMT_LITTLE,
        "L,R"
    )
) as fast_play:
    for freq, dura in [
        (261.6, 0.5), # C4
        (261.6, 0.5), # C4
        (392.0, 0.5), # G4
        (392.0, 0.5), # G4
        (440.0, 0.5), # A4
        (440.0, 0.5), # A4
        (392.0, 1.0), # G4

        (349.2, 0.5), # F4
        (349.2, 0.5), # F4
        (329.6, 0.5), # E4
        (329.6, 0.5), # E4
        (293.6, 0.5), # D4
        (293.6, 0.5), # D4
        (261.6, 1.0), # C4

        (392.0, 0.5), # G4
        (392.0, 0.5), # G4
        (349.2, 0.5), # F4
        (349.2, 0.5), # F4
        (329.6, 0.5), # E4
        (329.6, 0.5), # E4
        (293.6, 1.0), # D4

        (392.0, 0.5), # G4
        (392.0, 0.5), # G4
        (349.2, 0.5), # F4
        (349.2, 0.5), # F4
        (329.6, 0.5), # E4
        (329.6, 0.5), # E4
        (293.6, 1.0), # D4

        (261.6, 0.5), # C4
        (261.6, 0.5), # C4
        (392.0, 0.5), # G4
        (392.0, 0.5), # G4
        (440.0, 0.5), # A4
        (440.0, 0.5), # A4
        (392.0, 1.0), # G4

        (349.2, 0.5), # F4
        (349.2, 0.5), # F4
        (329.6, 0.5), # E4
        (329.6, 0.5), # E4
        (293.6, 0.5), # D4
        (293.6, 0.5), # D4
        (261.6, 1.0), # C4
    ]:
        fast_play.play_sine(
            freq,
            0.75,
            dura
        )

pyao.pyao_shutdown()
