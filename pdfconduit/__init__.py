from pdfconduit._version import __author__, __version__
from pdfconduit.utils import *
from pdfconduit.watermark import Watermark, Label, WatermarkAdd
from pdfconduit.upscale import upscale
from pdfconduit.rotate import rotate
from pdfconduit.encrypt import Encrypt
from pdfconduit.merge import Merge
from pdfconduit.slice import slicer
from pdfconduit.flatten import Flatten
from pdfconduit.utils.gui import GUI


__all__ = ["upscale", "rotate", "Encrypt", "Merge", "Watermark", "Label", "WatermarkAdd", "slicer",
           "GUI", "Info", "Flatten"]
__version__ = __version__
__author__ = __author__
