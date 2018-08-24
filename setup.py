from setuptools import setup, find_packages
from pdfconduit._version import __version__, __author__

long_description = """
A Pure-Python library built as a PDF toolkit.  Prepare documents for distribution.

Features:
- Watermark: Dynamically generate watermarks and add watermark to existing document
- Label: Overlay text labels such as filename or date to documents 
- Encrypt: Password protect and restrict permissions to print only
- Rotate: Rotate by increments of 90 degrees
- Upscale: Scale PDF size
- Merge: Concatenate multiple documents into one file
- Slice: Extract page ranges from documents
- Extract Text and Images
- Retrieve document metadata and information
"""

setup(
    name='pdfconduit',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'PyPDF3',
        'pdfrw',
        'PyMuPDF',
        'Pillow',
        'PySimpleGUI',
        'reportlab',
        'looptools',
        'tqdm',
    ],
    include_package_data=True,
    url='https://github.com/mrstephenneal/pdfconduit',
    license='',
    author=__author__,
    author_email='stephen@stephenneal.net',
    description='PDF toolkit for preparing documents for distribution.',
    long_description=long_description,
)
