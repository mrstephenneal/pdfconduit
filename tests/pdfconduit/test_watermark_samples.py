import unittest
import os
from pdfconduit.utils.samples import Samples
from tests import pdf


class TestWatermarkSamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = pdf
        dst = os.path.join(os.path.dirname(src), 'samples')

        cls.s = Samples(src, dst)

    @classmethod
    def tearDownClass(cls):
        cls.s.cleanup()

    def test_samples_opacity(self):
        m = self.s.opacity()

        self.assertTrue(os.path.exists(m))

    def test_samples_watermarks(self):
        m = self.s.watermarks()

        self.assertTrue(os.path.exists(m))

    def test_samples_placement(self):
        m = self.s.placement()

        self.assertTrue(os.path.exists(m))

    def test_samples_layering(self):
        m = self.s.layering()

        self.assertTrue(os.path.exists(m))


if __name__ == '__main__':
    unittest.main()
