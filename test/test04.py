"""
pyao test module 04.

Play Twinkle Twinkle Little Star.
"""

import pyao

with pyao.Device.open(
    pyao.get_default_driver_id(),
    pyao.preset.B16C2R44100LE
) as player:
    for freq, dura in [
        (261.6, 0.5),  # C4
        (261.6, 0.5),  # C4
        (392.0, 0.5),  # G4
        (392.0, 0.5),  # G4
        (440.0, 0.5),  # A4
        (440.0, 0.5),  # A4
        (392.0, 1.0),  # G4

        (349.2, 0.5),  # F4
        (349.2, 0.5),  # F4
        (329.6, 0.5),  # E4
        (329.6, 0.5),  # E4
        (293.6, 0.5),  # D4
        (293.6, 0.5),  # D4
        (261.6, 1.0),  # C4

        (392.0, 0.5),  # G4
        (392.0, 0.5),  # G4
        (349.2, 0.5),  # F4
        (349.2, 0.5),  # F4
        (329.6, 0.5),  # E4
        (329.6, 0.5),  # E4
        (293.6, 1.0),  # D4

        (392.0, 0.5),  # G4
        (392.0, 0.5),  # G4
        (349.2, 0.5),  # F4
        (349.2, 0.5),  # F4
        (329.6, 0.5),  # E4
        (329.6, 0.5),  # E4
        (293.6, 1.0),  # D4

        (261.6, 0.5),  # C4
        (261.6, 0.5),  # C4
        (392.0, 0.5),  # G4
        (392.0, 0.5),  # G4
        (440.0, 0.5),  # A4
        (440.0, 0.5),  # A4
        (392.0, 1.0),  # G4

        (349.2, 0.5),  # F4
        (349.2, 0.5),  # F4
        (329.6, 0.5),  # E4
        (329.6, 0.5),  # E4
        (293.6, 0.5),  # D4
        (293.6, 0.5),  # D4
        (261.6, 1.0),  # C4
    ]:
        print(freq, dura)
        # wave generator has been deprecated
        # player.play(pyao.wave.gen_sawtooth(pyao.preset.B16C2R44100LE, freq, dura))
