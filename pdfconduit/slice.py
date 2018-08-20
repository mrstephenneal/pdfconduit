# Slice PDF to remove unwanted pages
import os
from tempfile import NamedTemporaryFile
from PyPDF3 import PdfFileReader, PdfFileWriter
from pdfconduit.utils import add_suffix


def slicer(document, first_page=None, last_page=None, suffix='sliced', tempdir=None):
    """Slice a PDF document to remove pages."""
    # Set output file name
    if tempdir:
        output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False)
    elif suffix:
        output = os.path.join(os.path.dirname(document), add_suffix(document, suffix))
    else:
        output = NamedTemporaryFile(suffix='.pdf').name

    # Reindex page selections for simple user input
    first_page = first_page - 1 if not None else None

    pdf = PdfFileReader(document)
    writer = PdfFileWriter()

    pages = list(range(pdf.getNumPages()))[first_page:last_page]
    for page in pages:
        writer.addPage(pdf.getPage(page))

    with open(output, 'wb') as out:
        writer.write(out)
    return output
