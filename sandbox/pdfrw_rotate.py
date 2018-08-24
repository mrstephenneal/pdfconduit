# Rotate a pdf file
import os
from tempfile import NamedTemporaryFile
from pdfrw import PdfReader, PdfWriter


def add_suffix(file_path, suffix, sep):
    split = os.path.basename(file_path).rsplit('.', 1)
    return os.path.join(os.path.dirname(file_path), split[0] + sep + suffix + '.' + split[1])


def rotate(file_name, rotate, suffix='rotated', tempdir=None):
    """Rotate PDF by increments of 90 degrees."""
    # Set output file name
    if tempdir:
        outfn = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
    elif suffix:
        outfn = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        outfn = NamedTemporaryFile(suffix='.pdf').name

    trailer = PdfReader(file_name)
    pages = trailer.pages

    ranges = [[1, len(pages)]]

    for onerange in ranges:
        onerange = (onerange + onerange[-1:])[:2]
        for pagenum in range(onerange[0] - 1, onerange[1]):
            pages[pagenum].Rotate = (int(pages[pagenum].inheritable.Rotate or 0) + rotate) % 360

    outdata = PdfWriter(outfn)
    outdata.trailer = trailer
    outdata.write()
    return outfn


def main():
    pdf = 'your/path/to/doc.pdf'
    r = 90
    rotate(pdf, r)


if __name__ == '__main__':
    main()
