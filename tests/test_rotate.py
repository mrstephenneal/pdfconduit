import unittest
import os
from tempfile import TemporaryDirectory
from looptools import Timer
from pdfconduit import Info, rotate
from tests import *


class TestRotatePdfrw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf_path = pdf_path

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_rotate_90_pdfrw(self):
        """Rotate a PDF file by 90 degrees using the `pdfrw` library."""
        rotation = 90
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_180_pdfrw(self):
        """Rotate a PDF file by 180 degrees using the `pdfrw` library."""
        rotation = 180
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_180_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_270_pdfrw(self):
        """Rotate a PDF file by 270 degrees using the `pdfrw` library."""
        rotation = 270
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_270_pdfrw', tempdir=self.temp.name, method='pdfrw')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_90_pypdf3(self):
        """Rotate a PDF file by 90 degrees using the `pypdf3` library."""
        rotation = 90
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_pdfrw', tempdir=self.temp.name, method='pypdf3')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_180_pypdf3(self):
        """Rotate a PDF file by 180 degrees using the `pypdf3` library."""
        rotation = 180
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_180_pdfrw', tempdir=self.temp.name, method='pypdf3')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated

    @Timer.decorator
    def test_rotate_270_pypdf3(self):
        """Rotate a PDF file by 270 degrees using the `pypdf3` library."""
        rotation = 270
        rotated = rotate(self.pdf_path, rotation, suffix='rotated_270_pdfrw', tempdir=self.temp.name, method='pypdf3')

        # Assert rotated pdf file exists
        self.assertTrue(os.path.isfile(rotated))

        # Assert pdf file was rotated by the correct amount of degrees
        self.assertEqual(Info(rotated).rotate, rotation)
        return rotated


if __name__ == '__main__':
    unittest.main()
