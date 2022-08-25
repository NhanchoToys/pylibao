# pyao
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://github.com/NCBM/pyao/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Version](https://img.shields.io/pypi/v/pylibao)](https://pypi.org/project/pylibao/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pylibao)](https://pypi.org/project/pylibao/)

Python libao interface.

## Overview

PyAO is a Python wrapper for libao. It provides a simple interface for playing audio data.

## Installation

```
pip install pylibao
```

## Usage

Here is a simple example:

```python
import pyao

preset = pyao.presets.B16C2R44100LE

with pyao.open(pyao.get_default_driver_id(), preset) as ao:
    ao.play(b'\x00\x01\x02\x03')  # play data
```
