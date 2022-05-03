# pyao

Python libao interface.

## Overview

PyAO is a Python wrapper for libao. It provides a simple interface for playing audio data.

## Installation

W.I.P.

## Usage

Here is a simple example:

```python
import pyao

pyao.init()

preset = pyao.presets.FMT_B16C2R44100LE

with pyao.AO.open_live(pyao.default_driver_id(), preset) as ao:
    ao.play(b'\x00\x01\x02\x03')  # play data

pyao.shutdown()
```