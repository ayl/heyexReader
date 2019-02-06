Welcome to Python Heyex Reader's documentation!
===============================================

This is a native python implementation for reading Heidelberg Heyex Spectralis 
files. The current version only supports the Heyex VOL files. 

The github repository for this project is located at: `https://github.com/ayl/heyexReader <https://github.com/ayl/heyexReader>`_

============
Installation
============

::

   $ pip install heyexReader

============
Requirements
============

* Numpy
* Pillow

===============
Getting Started
===============

.. code-block:: python

   import heyexReader

   vol = heyexReader.volFile("test.vol")

   vol.renderIRslo("slo.png", renderGrid = True)
   vol.renderOCTscans("oct", renderSeg = True)

   print(vol.oct.shape)
   print(vol.irslo.shape)


.. toctree::
   :maxdepth: 2

   source/heyexReader.rst


