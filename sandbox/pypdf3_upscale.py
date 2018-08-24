# Upscale a PDF file
import os
from tempfile import NamedTemporaryFile

try:
    from PyPDF3 import PdfFileReader, PdfFileWriter
    from PyPDF3.pdf import PageObject
except ImportError:
    from PyPDF2 import PdfFileReader, PdfFileWriter
    from PyPDF2.pdf import PageObject


def dimensions(path):
    """Get width and height of a PDF"""
    pdf = PdfFileReader(path)
    size = pdf.getPage(0).mediaBox
    return {'w': float(size[2]), 'h': float(size[3])}


def add_suffix(file_path, suffix, sep):
    split = os.path.basename(file_path).rsplit('.', 1)
    return os.path.join(os.path.dirname(file_path), split[0] + sep + suffix + '.' + split[1])


def upscale(file_name, scale=1.5, margin_x=0, margin_y=0, suffix='scaled', tempdir=None):
    """Upscale a PDF to a large size."""
    # Set output file name
    if tempdir:
        output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
    elif suffix:
        output = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        output = NamedTemporaryFile(suffix='.pdf').name

    reader = PdfFileReader(file_name)
    writer = PdfFileWriter()
    dims = dimensions(file_name)
    target_w = dims['w'] * scale
    target_h = dims['h'] * scale

    # Number of pages in input document
    page_count = reader.getNumPages()

    for page_number in range(page_count):
        wtrmrk = reader.getPage(page_number)

        page = PageObject.createBlankPage(width=target_w, height=target_h)
        page.mergeScaledTranslatedPage(wtrmrk, scale, margin_x, margin_y)
        writer.addPage(page)

    with open(output, "wb") as outputStream:
        writer.write(outputStream)

    return output


def main():
    pdf = 'your/path/to/doc.pdf'
    scale = 1.0
    upscale(pdf, scale)


if __name__ == '__main__':
    main()
