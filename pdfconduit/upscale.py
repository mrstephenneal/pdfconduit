# Upscale a PDF file
import os
from tempfile import NamedTemporaryFile
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject
from pdfrw import PdfReader, PdfWriter, PageMerge, IndirectPdfDict
from pdfconduit.utils import Info, add_suffix


class Upscale:
    def __init__(self, file_name, margin_x=0, margin_y=0, scale=1.5, suffix='scaled', tempdir=None, method='pdfrw'):
        self.file_name = file_name
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.scale = scale
        self.suffix = suffix

        # Set output file name
        if tempdir:
            self.output = NamedTemporaryFile(suffix='.pdf', dir=tempdir, delete=False).name
        elif suffix:
            self.output = os.path.join(os.path.dirname(file_name), add_suffix(file_name, suffix))
        else:
            self.output = NamedTemporaryFile(suffix='.pdf').name

        # Get target width and height
        dims = Info(self.file_name).dimensions
        self.target_w = dims['w'] * self.scale
        self.target_h = dims['h'] * self.scale

        # Execute either pdfrw or PyPDF3 method
        if method is 'pypdf3':
            self.pypdf3()
        else:
            self.pdfrw()

    def __str__(self):
        return self.file

    @property
    def file(self):
        return str(self.output)

    def _pdfrw_adjust(self, page):
        info = PageMerge().add(page)
        x1, y1, x2, y2 = info.xobj_box
        viewrect = (self.margin_x, self.margin_y, x2 - x1 - 2 * self.margin_x, y2 - y1 - 2 * self.margin_y)
        page = PageMerge().add(page, viewrect=viewrect)
        page[0].scale(self.scale)
        return page.render()

    def pdfrw(self):
        reader = PdfReader(self.file_name)
        writer = PdfWriter(self.output)
        for i in list(range(0, len(reader.pages))):
            writer.addpage(self._pdfrw_adjust(reader.pages[i]))
        writer.trailer.Info = IndirectPdfDict(reader.Info or {})
        writer.write()

    def pypdf3(self):
        reader = PdfFileReader(self.file_name)
        writer = PdfFileWriter()

        # Number of pages in input document
        page_count = reader.getNumPages()

        for page_number in range(page_count):
            wtrmrk = reader.getPage(page_number)

            page = PageObject.createBlankPage(width=self.target_w, height=self.target_h)
            page.mergeScaledTranslatedPage(wtrmrk, self.scale, self.margin_x, self.margin_y)
            writer.addPage(page)

        with open(self.output, "wb") as outputStream:
            writer.write(outputStream)
        return self.output


def upscale(file_name, margin_x=0, margin_y=0, scale=1.5, suffix='scaled', tempdir=None, method='pdfrw'):
    return str(Upscale(file_name, margin_x, margin_y, scale, suffix, tempdir, method))
