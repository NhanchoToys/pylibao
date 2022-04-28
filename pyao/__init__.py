"""
Python libao interface.
"""

__all__ = [
    'AO',
    'AODevice',
    'AOFormat',
    'pyao_init',
    'pyao_shutdown',
    'default_driver_id',
    'pyao_fast_play',
    'pyao_fast_play_file',
    'AO_FMT_NATIVE',
    'AO_FMT_LITTLE',
    'AO_FMT_BIG'
]

from pyao._abstract import (
    AODevice,
    AOFormat,
    AO,
    pyao_init,
    pyao_shutdown,
    pyao_default_driver_id as default_driver_id,
    pyao_fast_play,
    pyao_fast_play_file,
    AO_FMT_NATIVE,
    AO_FMT_LITTLE,
    AO_FMT_BIG
)