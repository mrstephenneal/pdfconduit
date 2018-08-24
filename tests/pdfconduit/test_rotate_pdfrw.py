import unittest
import os
import shutil
import time
from pdfconduit import Info, rotate
from tests import pdf, directory


class TestRotatePdfrw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'rotate')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        cls.files = []

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            shutil.move(source, target)
            self.files.remove(i)

    def test_rotate_pdfrw(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_pdfrw', method='pdfrw')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_90_pdfrw(self):
        r = 90
        rotated1 = rotate(pdf, r, suffix='rotated_90_pdfrw', method='pdfrw')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_180_pdfrw(self):
        r = 180
        rotated1 = rotate(pdf, r, suffix='rotated_180_pdfrw', method='pdfrw')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)

    def test_rotate_270_pdfrw(self):
        r = 270
        rotated1 = rotate(pdf, r, suffix='rotated_270_pdfrw', method='pdfrw')
        self.files.append(rotated1)

        self.assertTrue(os.path.isfile(rotated1))
        self.assertEqual(Info(rotated1).rotate, r)


if __name__ == '__main__':
    unittest.main()
