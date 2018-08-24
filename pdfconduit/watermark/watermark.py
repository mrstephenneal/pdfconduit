# Apply a watermark to a PDF file
import os
import shutil
from tempfile import mkdtemp
from looptools import Timer
from pdfconduit.utils import add_suffix, open_window, Receipt, IMAGE_DEFAULT
from pdfconduit.encrypt import Encrypt
from pdfconduit.watermark.draw import WatermarkDraw
from pdfconduit.watermark.add import WatermarkAdd
from pdfconduit.watermark.canvas import CanvasConstructor


class Watermark:
    def __init__(self, document, remove_temps=True, move_temps=None, open_file=True, tempdir=mkdtemp(), receipt=None,
                 use_receipt=True, progress_bar_enabled=False, progress_bar='tqdm'):
        """
        Watermark and encrypt a PDF document.

        Manage watermarking processes from single class initialization.  This class utilizes the draw,
        add and encrypt modules.

        :param document: str
            PDF document full path
        :param remove_temps: bool
            Remove temporary files after completion
        :param open_file: bool
            Open file after completion
        :param tempdir: function or str
            Temporary directory for file writing
        :param receipt: cls
            Use existing Receipt object if already initiated
        :param use_receipt: bool
            Print receipt information to console and write to file
        """
        self.time = Timer()
        self.document_og = document
        self.document = self.document_og
        self.watermark = None
        self.remove_temps = remove_temps
        self.move_temps = move_temps
        self.open_file = open_file
        self.tempdir = tempdir
        self.progress_bar_enabled = progress_bar_enabled
        self.progress_bar = progress_bar

        self.use_receipt = use_receipt
        if isinstance(receipt, Receipt):
            self.receipt = receipt
        else:
            self.receipt = Receipt(use_receipt).set_dst(document)

    def __str__(self):
        return str(self.document)

    def cleanup(self):
        runtime = self.time.end
        self.receipt.add('~run time~', runtime)
        if self.use_receipt:
            self.receipt.dump()
        if self.move_temps:
            if os.path.isdir(self.move_temps):
                shutil.move(self.tempdir, self.move_temps)
        if self.remove_temps:
            if os.path.isdir(self.tempdir):
                shutil.rmtree(self.tempdir)
        else:
            open_window(self.tempdir)
        return self.document

    def draw(self, text1=None, text2=None, copyright=True, image=IMAGE_DEFAULT, rotate=30, opacity=0.08, compress=0,
             flatten=False, add=False):
        """
        Draw watermark PDF file.

        Create watermark using either a reportlabs canvas or a PIL image.

        :param text1: str
            Text line 1
        :param text2: str
            Text line 2
        :param copyright: bool
            Draw copyright and year to canvas
        :param image: str
            Logo image to be used as base watermark
        :param rotate: int
            Degrees to rotate canvas by
        :param opacity: float
            Watermark opacity
        :param compress: bool
            Compress watermark contents  (not entire PDF)
        :param flatten: bool
            Draw watermark with multiple layers or a single flattened layer
        :param add: bool
            Add watermark to original document
        :return: str
            Watermark PDF file full path
        """
        # Add to receipt
        self.receipt.add('Text1', text1)
        self.receipt.add('Text2', text2)
        self.receipt.add('Image', image)
        self.receipt.add('WM Opacity', str(int(opacity * 100)) + '%')
        self.receipt.add('WM Compression', compress)
        self.receipt.add('WM Flattening', flatten)

        co = CanvasConstructor(text1, text2, copyright, image, rotate, opacity, tempdir=self.tempdir)
        objects, rotate = co.img() if flatten else co.canvas()  # Run img constructor method if flatten is True

        # Draw watermark to file
        self.watermark = WatermarkDraw(objects, rotate=rotate, compress=compress, tempdir=self.tempdir).write()

        if not add:
            return self.watermark
        else:
            self.add()
            return self.cleanup()

    def add(self, document=None, watermark=None, underneath=False, output=None, suffix='watermarked', method='pdfrw'):
        """
        Add a watermark file to an existing PDF document.

        Rotate and upscale watermark file as needed to fit existing PDF document.  Watermark can be overlayed or
        placed underneath.

        :param document: str
            PDF document full path
        :param watermark: str
            Watermark PDF full path
        :param underneath: bool
            Place watermark either under or over existing PDF document
        :param output: str
            Output file path
        :param suffix: str
            Suffix to append to existing PDF document file name
        :param method: str
            PDF library to be used for watermark adding
        :return: str
            Watermarked PDF Document full path
        """
        self.receipt.add('WM Placement', 'Overlay')
        if not watermark:
            watermark = self.watermark
        if not document:
            document = self.document
        self.document = str(WatermarkAdd(document, watermark, output=output, underneath=underneath,
                                         tempdir=self.tempdir, suffix=suffix, method=method))
        self.receipt.add('Watermarked PDF', os.path.basename(self.document))
        if self.open_file:
            open_window(self.document)
        return self.document

    def encrypt(self, user_pw='', owner_pw=None, encrypt_128=True, allow_printing=True, allow_commenting=False,
                document=None):
        """
        Encrypt a PDF document to add passwords and restrict permissions.

        Add a user password that must be entered to view document and a owner password that must be entered to alter
        permissions and security settings.  Encryption keys are 128 bit when encrypt_128 is True and 40 bit when
        False.  By default permissions are restricted to print only, when set to false all permissions are allowed.
        TODO: Add additional permission parameters

        :param user_pw: str
            User password required to open and view PDF document
        :param owner_pw: str
            Owner password required to alter security settings and permissions
        :param encrypt_128: bool
            Encrypt PDF document using 128 bit keys
        :param allow_printing: bool
            Restrict permissions to print only
        :return: str
            Encrypted PDF full path
        """
        document = self.document if document is None else document
        self.receipt.add('User pw', user_pw)
        self.receipt.add('Owner pw', owner_pw)
        if encrypt_128:
            self.receipt.add('Encryption key size', '128')
        else:
            self.receipt.add('Encryption key size', '40')
        if allow_printing:
            self.receipt.add('Permissions', 'Allow printing')
        else:
            self.receipt.add('Permissions', 'Allow ALL')
        p = str(Encrypt(document, user_pw, owner_pw, output=add_suffix(self.document_og, 'secured'),
                        bit128=encrypt_128, allow_printing=allow_printing, allow_commenting=allow_commenting,
                        progress_bar_enabled=self.progress_bar_enabled, progress_bar=self.progress_bar))
        self.receipt.add('Secured PDF', os.path.basename(p))
        return p
