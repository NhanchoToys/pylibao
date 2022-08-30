"""
Python libao interface.
"""

__all__ = [
    'PlaybackError',
    'init',
    'shutdown',
    'get_default_driver_id',
    'AO_FMT_NATIVE',
    'AO_FMT_LITTLE',
    'AO_FMT_BIG'
]

from pyao._ao import (
    PlaybackError,
    initialize as init,
    shutdown,
    get_default_driver_id,
    AO_FMT_NATIVE,
    AO_FMT_LITTLE,
    AO_FMT_BIG
)
from pyao import presets as _presets

import atexit

init()
atexit.register(shutdown)


class _preset:
    __getattribute__ = lambda self, attr: _presets.get_format_from_string(attr)


preset = _preset()
