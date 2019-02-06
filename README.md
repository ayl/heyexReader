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


