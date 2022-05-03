"""
Python libao interface.
"""

__all__ = [
    '_aointernal',
    'presets',
    'wave',
    'PlaybackError',
    'AO',
    'AODevice',
    'AOFormat',
    'init',
    'shutdown',
    'get_default_driver_id',
    'AO_FMT_NATIVE',
    'AO_FMT_LITTLE',
    'AO_FMT_BIG'
]

from pyao import _aointernal
from pyao._abstract import (
    PlaybackError,
    AODevice,
    AOFormat,
    AO,
    pyao_init as init,
    pyao_shutdown as shutdown,
    pyao_default_driver_id as get_default_driver_id,
    AO_FMT_NATIVE,
    AO_FMT_LITTLE,
    AO_FMT_BIG
)
from pyao import presets, wave
