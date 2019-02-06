# heyexReader
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


This is a native python implementation for reading Heidelberg Heyex
Spectralis files. The current version only supports the Heyex VOL files.

The full documentation of this project is located at: 
<https://github.com/ayl/heyexReader>

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
