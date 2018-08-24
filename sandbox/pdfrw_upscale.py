# Upscale a PDF file
import os
from tempfile import NamedTemporaryFile
from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict


def add_suffix(file_path, suffix, sep):
    split = os.path.basename(file_path).rsplit('.', 1)
    return os.path.join(os.path.dirname(file_path), split[0] + sep + suffix + '.' + split[1])


def upscale(file_name, scale=1.5, margin_x=0, margin_y=0, suffix='scaled', tempdir=None):
    """Upscale a PDF to a large size."""
    def adjust(page):
        info = PageMerge().add(page)
        x1, y1, x2, y2 = info.xobj_box
        viewrect = (margin_x, margin_y, x2 - x1 - 2 * margin_x, y2 - y1 - 2 * margin_y)
        page = PageMerge().add(page, viewrect=viewrect)
        page[0].scale(scale)
        return page.render()

    # Set output file name
    if tempdir:
        output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
    elif suffix:
        output = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
    else:
        output = NamedTemporaryFile(suffix='.pdf').name

    reader = PdfReader(file_name)
    writer = PdfWriter(output)
    for i in list(range(0, len(reader.pages))):
        writer.addpage(adjust(reader.pages[i]))
    writer.trailer.Info = IndirectPdfDict(reader.Info or {})
    writer.write()
    return output


def main():
    pdf = 'your/path/to/doc.pdf'
    scale = 1.0
    upscale(pdf, scale)


if __name__ == '__main__':
    main()
