# TFT Thumbnail

![G-code preview thumbnail](images/thumbnail.jpg)

**tft-thumbnail** is a Prusa Slicer post processor for Two Trees Sapphire Pro/Plus (and MKS Robin Nano TFT35) 3D printers for generating compatible preview images.

## Installation

Download the `tft-thumbnail.py` and place it in your scripts folder. I use `~/bin` for this.

You will also need to make sure you have python3 installed and configured. On my Mac that can be done at the command prompt with:

`brew install python3`

Then I would reccomend you can test this post processing script on a small G-code file to check you have all the required python libraries installed.

`python3 tft-thumbnail.py test.gcode test-sp.gcode`

If you see any errors you can use `pip` to install any missing modules.

`pip install regex`

`pip install Image`

## Prusa Slicer Setup

You need to configure Prusa Slicer to output preview images (GCODE Thumbnails) and then run this a post processing script to convert them to a format compatible with the TFT35 display used by the Sapphire Pro/Plus 3D printers.

![Printer Settings](images/printer-settings.jpg)

Under the **Printer Settings** tab, in **Firmware** settings:

* G-code flavor: **Marlin 2**
* G-code thumbnails: **100x100, 200x200**
* Format of G-code thumbnails: **PNG**

![Print Settings](images/print-settings.jpg)

Under the **Print Settings** tab, in **Post-processing scripts** settings:

`/path/to/python3 /path/to/tft-thumbnail.py`
