# Create flat PDF by converting each input PDF page to a PNG
import os
import shutil
import fitz
import PySimpleGUI as gui
from io import BytesIO
from PIL import Image
from tempfile import NamedTemporaryFile, mkdtemp
from tqdm import tqdm
from pdfconduit.utils import add_suffix
from pdfconduit.watermark.canvas.objects import CanvasImg, CanvasObjects
from pdfconduit.watermark.draw.pdf import WatermarkDraw
from pdfconduit.merge import Merge
from pdfconduit.upscale import upscale


def clean_temps(tempdir):
    # TODO: Files remaining open on window and preventing deletion
    if os.path.isdir(tempdir):
        try:
            shutil.rmtree(tempdir)
        except PermissionError:
            print(tempdir, 'was not removed')


class PDFtoIMG:
    def __init__(self, file_name, tempdir=None, ext='png', progress_bar=None):
        """Convert each page of a PDF file into a PNG image"""
        self.file_name = file_name
        self.tempdir = tempdir
        self.ext = ext
        self.progress_bar = progress_bar

        self.doc = fitz.open(self.file_name)
        self.output_dir = os.path.dirname(file_name) if tempdir is None else tempdir

        # storage for page display lists
        self.dlist_tab = [None] * len(self.doc)
        self.pdf_data = self._get_pdf_data()

    def _get_pdf_data(self):
        # PySimpleGUI progress bar
        if self.progress_bar is 'gui':
            data = []
            for i, cur_page in enumerate(range(len(self.doc))):
                data.append(self._get_page_data(cur_page))
                if not gui.EasyProgressMeter('Getting PDF page data', i + 1, len(self.doc), orientation='h'):
                    break
            return data
        # TQDM progress bar
        elif self.progress_bar is 'tqdm':
            return [self._get_page_data(cur_page) for cur_page in tqdm(range(len(self.doc)),
                                                                       desc='Getting PDF page data',
                                                                       total=len(self.doc), unit='Pages')]
        # No progress bar
        else:
            return [self._get_page_data(cur_page) for cur_page in range(len(self.doc))]

    def _get_page_data(self, pno, zoom=0):
        """
        Return a PNG image for a document page number. If zoom is other than 0, one of
        the 4 page quadrants are zoomed-in instead and the corresponding clip returned.
        """
        dlist = self.dlist_tab[pno]  # get display list
        if not dlist:  # create if not yet there
            self.dlist_tab[pno] = self.doc[pno].getDisplayList()
            dlist = self.dlist_tab[pno]
        r = dlist.rect  # page rectangle
        mp = r.tl + (r.br - r.tl) * 0.5  # rect middle point
        mt = r.tl + (r.tr - r.tl) * 0.5  # middle of top edge
        ml = r.tl + (r.bl - r.tl) * 0.5  # middle of left edge
        mr = r.tr + (r.br - r.tr) * 0.5  # middle of right egde
        mb = r.bl + (r.br - r.bl) * 0.5  # middle of bottom edge
        mat = fitz.Matrix(2, 2)  # zoom matrix
        if zoom == 1:  # top-left quadrant
            clip = fitz.Rect(r.tl, mp)
        elif zoom == 4:  # bot-right quadrant
            clip = fitz.Rect(mp, r.br)
        elif zoom == 2:  # top-right
            clip = fitz.Rect(mt, mr)
        elif zoom == 3:  # bot-left
            clip = fitz.Rect(ml, mb)
        if zoom == 0:  # total page
            pix = dlist.getPixmap(alpha=False)
        else:
            pix = dlist.getPixmap(alpha=False, matrix=mat, clip=clip)
        return pix.getPNGData()  # return the PNG image

    def _get_output(self, index):
        if not self.tempdir:
            output_file = add_suffix(self.file_name, str(index), ext=self.ext)
            return os.path.join(self.output_dir, output_file)
        else:
            return NamedTemporaryFile(suffix='.png', dir=self.tempdir, delete=True).name

    def save(self):
        # PySimpleGUI progress bar
        if self.progress_bar is 'gui':
            saved = []
            for i, img in enumerate(self.pdf_data):
                output = self._get_output(i)
                saved.append(output)
                with Image.open(BytesIO(img)) as image:
                    image.save(output)
                if not gui.EasyProgressMeter('Saving PDF pages as PNGs', i + 1, len(self.doc), orientation='h'):
                    break
            self.doc.close()
            return saved
        # TQDM progress bar
        elif self.progress_bar is 'tqdm':
            loop = enumerate(tqdm(self.pdf_data, desc='Saving PDF pages as PNGs', total=len(self.pdf_data),
                                  unit='PNGs'))
        # No progress bar
        else:
            loop = enumerate(self.pdf_data)
        saved = []
        for i, img in loop:
            output = self._get_output(i)
            saved.append(output)
            with Image.open(BytesIO(img)) as image:
                image.save(output)
        self.doc.close()
        return saved


class IMGtoPDF:
    def __init__(self, imgs, destination=None, tempdir=None, progress_bar=None):
        """Convert each image into a PDF page and merge all pages to one PDF file"""
        self.imgs = imgs
        self.output_dir = destination
        self.tempdir = tempdir
        self.progress_bar = progress_bar

        self.pdf_pages = self.img2pdf()

    def img2pdf(self):
        # TODO: Figure out weather this method is causing unclosed file warnings and errors
        # PySimpleGUI progress bar
        if self.progress_bar is 'gui':
            pdfs = []
            for index, i in enumerate(self.imgs):
                with Image.open(i) as im:
                    width, height = im.size

                    co = CanvasObjects()
                    co.add(CanvasImg(i, 1.0, w=width, h=height))

                    pdf = WatermarkDraw(co, tempdir=self.tempdir, pagesize=(width, height)).write()
                    pdfs.append(pdf)
                if not gui.EasyProgressMeter('Saving PNGs as flat PDFs', index + 1, len(self.imgs), orientation='h'):
                    break
            return pdfs
        # TQDM progress bar
        elif self.progress_bar is 'tqdm':
            loop = tqdm(self.imgs, desc='Saving PNGs as flat PDFs', total=len(self.imgs), unit='PDFs')
        # No progress bar
        else:
            loop = self.imgs
        pdfs = []
        for i in loop:
            with Image.open(i) as im:
                width, height = im.size

            co = CanvasObjects()
            co.add(CanvasImg(i, 1.0, w=width, h=height))

            pdf = WatermarkDraw(co, tempdir=self.tempdir, pagesize=(width, height)).write()
            pdfs.append(pdf)
        return pdfs

    def save(self, remove_temps=True, output_name='merged imgs'):
        m = str(Merge(self.pdf_pages, output_name=output_name, output_dir=self.output_dir))
        if remove_temps:
            clean_temps(self.tempdir)
        return m


class Flatten:
    def __init__(self, file_name, scale=2.0, suffix='flat', tempdir=None, progress_bar=None):
        """Create a flat single-layer PDF by converting each page to a PNG image"""
        self._file_name = file_name
        self.tempdir = tempdir if tempdir else mkdtemp()
        self.suffix = suffix
        self.directory = os.path.dirname(file_name)
        self.progress_bar = progress_bar

        if scale and scale is not 0 and scale is not 1.0:
            self.file_name = upscale(file_name, scale=scale, tempdir=tempdir)
        else:
            self.file_name = self._file_name

        self.imgs = None
        self.pdf = None

    def __str__(self):
        return str(self.pdf)

    def get_imgs(self):
        self.imgs = PDFtoIMG(self.file_name, tempdir=self.tempdir, progress_bar=self.progress_bar).save()
        return self.imgs

    def save(self, remove_temps=True):
        if self.imgs is None:
            self.get_imgs()
        i2p = IMGtoPDF(self.imgs, self.directory, self.tempdir, self.progress_bar)
        self.pdf = i2p.save(remove_temps=remove_temps, output_name=add_suffix(self._file_name, self.suffix))
        return self.pdf
