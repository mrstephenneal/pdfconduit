import unittest
import os
import shutil
import time
from pdfconduit import Watermark, slicer, Info, Label
from tests import directory, pdf as p


class TestWatermarkMethodsPyPDF3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdfs = ['plan_l.pdf', 'plan_p.pdf', 'con docs2.pdf']
        # cls.pdfs = ['plan_l.pdf', 'plan_p.pdf']
        # cls.pdfs = ['con docs2_sliced.pdf']

        cls.w = Watermark(p, use_receipt=False, open_file=False)
        if 'con docs2_sliced.pdf' in cls.pdfs and not os.path.exists(os.path.join(directory, 'con docs2_sliced.pdf')):
            slicer(os.path.join(directory, 'con docs2.pdf'), first_page=1, last_page=1, suffix='sliced')

        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'watermark')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        cls.w.cleanup()

    def setUp(self):
        self.pdfs = [os.path.join(directory, pdf) for pdf in self.pdfs]
        self.address = '43 Indian Lane'
        self.town = 'Franklin'
        self.state = 'MA'
        self.rotate = 30
        self.owner_pw = 'foo'
        self.user_pw = 'baz'
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

    def test_watermark_pypdf3(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate,
                                 flatten=False)
            added = self.w.add(pdf, wtrmrk, method='pypdf3', suffix='watermarked_pypdf3')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_underneath_pypdf3(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=True, suffix='watermarked_underneath_pypdf3', method='pypdf3')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_overlay_pypdf3(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=False, suffix='watermarked_overlay_pypdf3', method='pypdf3')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_flat_pypdf3(self):
        for pdf in self.pdfs:
            flat = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=True)
            added = self.w.add(pdf, flat, suffix='watermarked_flat_pypdf3', method='pypdf3')
            self.files.append(added)

            self.assertTrue(os.path.exists(flat))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_layered_pypdf3(self):
        for pdf in self.pdfs:
            layered = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=False)
            added = self.w.add(pdf, layered, suffix='watermarked_layered_pypdf3', method='pypdf3')
            self.files.append(added)

            self.assertTrue(os.path.exists(layered))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_label(self):
        for pdf in self.pdfs:
            label = os.path.basename(pdf)
            l = Label(pdf, label, tempdir=self.w.tempdir).write(cleanup=False)
            self.files.append(l)

            self.assertTrue(os.path.exists(l))
            self.assertTrue(Info(l).resources())


if __name__ == '__main__':
    unittest.main()
