import unittest
from tests.pdfconduit.test_encrypt import TestEncrypt
from tests.pdfconduit.test_merge import TestMerge
from tests.pdfconduit.test_rotate_pypdf3 import TestRotatePyPDF3
from tests.pdfconduit.test_rotate_pdfrw import TestRotatePdfrw
from tests.pdfconduit.test_slice import TestSlice
from tests.pdfconduit.test_upscale_pypdf3 import TestUpscalePyPDF3
from tests.pdfconduit.test_upscale_pdfrw import TestUpscalePdfrw
from tests.pdfconduit.test_watermark_pypdf3 import TestWatermarkMethodsPyPDF3
from tests.pdfconduit.test_watermark_pdfrw import TestWatermarkMethodsPdfrw


def main():
    unittest.main()


if __name__ == '__main__':
    main()
