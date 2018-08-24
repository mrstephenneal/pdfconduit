import unittest
import os
import shutil
import time
from pdfconduit import Info, slicer
from tests import directory, pdf


class TestSlice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        dst = os.path.join(results, 'slice')

        # Create destination if it does not exist
        if not os.path.isdir(dst):
            os.mkdir(dst)

        # Move each file into results folder
        for i in cls.files:
            source = i
            target = os.path.join(dst, str(os.path.basename(i)))
            shutil.move(source, target)

    def setUp(self):
        self.pdf = os.path.join(directory, pdf)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (' '.join(self.id().split('.')[-1].split('_')[1:]), t))

    def test_slice(self):
        fp = 1
        lp = 1
        sliced = slicer(self.pdf, first_page=fp, last_page=lp)
        self.files.append(sliced)

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))

    def test_slice_4to7(self):
        fp = 4
        lp = 7
        sliced = slicer(self.pdf, first_page=fp, last_page=lp, suffix='sliced_4-7')
        self.files.append(sliced)

        self.assertTrue(os.path.isfile(sliced))
        self.assertEqual(Info(sliced).pages, len(range(fp, lp+1)))


if __name__ == '__main__':
    unittest.main()
