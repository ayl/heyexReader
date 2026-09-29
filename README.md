# heyexReader
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Documentation Status](https://readthedocs.org/projects/heyexreader/badge/?version=latest)](https://heyexreader.readthedocs.io/en/latest/?badge=latest)
[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-270/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

This is a native python implementation for reading Heidelberg Heyex
Spectralis files. The current version only supports the Heyex VOL files.

The full documentation of this project is located at: 
<http://heyexreader.readthedocs.io/>

# Installation

    $ pip install heyexReader

The PyPI release 0.1.3 uses `array.fromstring()`, which was removed in
Python 3.9. Reading a VOL file with that release on Python 3.9 or newer raises
`AttributeError`. The source contains the `frombytes()` compatibility fix
from [PR #6](https://github.com/ayl/heyexReader/pull/6), but it is not included
in PyPI release 0.1.3. Until a new release is published, install the fixed
source revision (Git is required):

```sh
python -m pip install "heyexReader @ git+https://github.com/ayl/heyexReader.git@73aa32cf7aa283446aee1be8808651598052bc26"
```

Use a fresh virtual environment. If 0.1.3 is already installed, add
`--force-reinstall` to replace it: the source still has version 0.1.3, so pip
may otherwise keep the published build.

# Testing

```sh
python -m pip install .
python -m unittest discover -s tests -v
```

The tests generate a small synthetic VOL file, read its SLO, OCT, and
segmentation buffers, and render PNGs. No patient files or display are needed.
CI runs these tests on Linux and Windows with Python 3.8, 3.11, and 3.14.

# Requirements

  - Numpy
  - Pillow

# Getting Started

``` python
import heyexReader

vol = heyexReader.volFile("test.vol")

vol.renderIRslo("slo.png", renderGrid = True)
vol.renderOCTscans("oct", renderSeg = True)

print(vol.oct.shape)
print(vol.irslo.shape)
```

# Thanks To

The basis for this code was ported from Markus Mayer's excellent work <https://www5.cs.fau.de/research/software/octseg/>. 


# Funded by
[![Research to Prevent Blindness](/funding/rpb.png?raw=true "RPB")](https://www.rpbusa.org/rpb/)
[![National Eye Institute](/funding/nei.jpg?raw=true "NEI")](https://nei.nih.gov/)
