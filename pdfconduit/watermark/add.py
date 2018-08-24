# Add a watermark PDF file to another PDF file
from tempfile import NamedTemporaryFile
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.pdf import PageObject
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.lib.pagesizes import letter
from pdfconduit.upscale import upscale
from pdfconduit.rotate import rotate
from pdfconduit.utils import add_suffix, resource_path, Info


class WatermarkAdd:
    def __init__(self, document, watermark, underneath=False, overwrite=False, output=None, suffix='watermarked',
                 decrypt=False, tempdir=None, method='pdfrw'):
        """
        Add a watermark to an existing PDF document

        1. Read PDF document and decrypt if encrypted
        2. Get input PDF document info
            2a. Retrieve dimensions
            2b. Determine orientation
            2c. Upscale to fit letter
        3. Get watermark info
            3a. Retrieve dimensions
            3b. Rotate if necessary
            3c. Upscale to fit document
        4. Set file names
            4a. Check if a upscaled doc was created, if not use original document
            4b. Check if watermark was rotated, if not use original watermark
        5. Add watermark to PDF document
            5a. Create watermarked document filename (ex: originalpdfname_watermarked.pdf)
            5b. Create PDF file reader and file writer objects
            5c. Add watermark to each page of original
            5d. Save watermarked document to file
        """
        self.rotate = 0
        self.scale = 0
        self.underneath = underneath
        self.tempdir = tempdir
        self.method = method

        self.document_reader = self._document_reader(document, decrypt)
        self.document = self._get_document_info(document)
        self.watermark_file = self._get_watermark_info(self.document, watermark)
        pdf_fname, wtrmrk_fname = self._set_filenames

        if overwrite:
            self.output_filename = document
        elif output:
            self.output_filename = output
        elif suffix:
            self.output_filename = add_suffix(document, suffix)
        else:
            tmpf = NamedTemporaryFile(suffix='.pdf', dir=self.tempdir, delete=False)
            self.output_filename = resource_path(tmpf.name)

        self.add(pdf_fname, wtrmrk_fname)

    def __str__(self):
        return str(self.output_filename)

    @staticmethod
    def _document_reader(document, decrypt=False):
        # 1. Read PDF document and create file reader object
        if decrypt:
            reader = PdfFileReader(document)
            reader.decrypt(decrypt)
            return reader
        else:
            return PdfFileReader(document)

    def _get_document_info(self, filename):
        pdf_file = {'path': filename}

        # 2a. Get PDF width and height
        pdf_file.update(Info(self.document_reader).dimensions)

        # 2b. Get PDF file orientation
        if pdf_file['h'] > pdf_file['w']:
            pdf_file['orientation'] = 'portrait'
            letter_size = {'w': int(letter[0]), 'h': int(letter[1])}
        else:
            pdf_file['orientation'] = 'landscape'
            letter_size = {'h': int(letter[0]), 'w': int(letter[1])}

        # 2c. Upscale PDF if it is smaller than a letter
        if pdf_file['w'] <= letter_size['w'] or pdf_file['h'] <= letter_size['h']:
            scale = float(letter_size['w'] / pdf_file['w'])
            pdf_file['upscaled'] = upscale(pdf_file['path'], scale=scale, tempdir=self.tempdir)
            self.document_reader = self._document_reader(pdf_file['upscaled'])
        return pdf_file

    def _get_watermark_info(self, document, watermark, margin_x=0, margin_y=0):
        # 3a. Get watermark path and dimensions
        watermark_file = {'path': watermark}
        watermark_file.update(Info(watermark).dimensions)

        # 3b. Check if watermark file needs to be rotated
        if watermark_file['w'] > watermark_file['h'] and document['orientation'] is 'portrait':
            self.rotate = 90
            watermark_file['rotated'] = rotate(watermark, self.rotate, tempdir=self.tempdir, method=self.method)

        # Set watermark file to be used for upscaling
        try:
            wtrmrk = watermark_file['rotated']
            watermark_file.update(Info(watermark_file['rotated']).dimensions)
        except KeyError:
            wtrmrk = watermark_file['path']

        # 3c. Check if watermark file needs to be upscaled
        scale = 0
        if watermark_file['w'] <= document['w']:
            scale = float(document['w'] / watermark_file['w'])

            if watermark_file['h'] * scale > document['h']:
                scale = float(document['h'] / watermark_file['h'])

            watermark_file['upscaled'] = upscale(wtrmrk, scale=scale, tempdir=self.tempdir, method=self.method)
        self.scale = scale
        return watermark_file

    @property
    def _set_filenames(self):
        # 4a. If upscaled PDF file does not exists use input PDF path
        try:
            pdf = self.document['upscaled']
        except KeyError:
            pdf = self.document['path']

        # 4b. If rotated watermark file does not exists use input watermark path
        try:
            try:
                watermark = self.watermark_file['upscaled']
            except KeyError:
                watermark = self.watermark_file['rotated']
        except KeyError:
            watermark = self.watermark_file['path']
        return pdf, watermark

    def add(self, document, watermark):
        """Add watermark to PDF by merging original PDF and watermark file."""
        # 5a. Create output PDF file name
        output_filename = self.output_filename

        def pypdf3():
            """Much slower than PyPDF3 method."""
            # 5b. Get our files ready
            document_reader = PdfFileReader(document)
            output_file = PdfFileWriter()

            # Number of pages in input document
            page_count = document_reader.getNumPages()

            # Watermark objects
            watermark_reader = PdfFileReader(watermark)
            wtrmrk_page = watermark_reader.getPage(0)
            wtrmrk_width = (wtrmrk_page.mediaBox.getWidth() / 2) + 0
            wtrmrk_height = (wtrmrk_page.mediaBox.getHeight() / 2) + 80
            wtrmrk_rotate = -int(Info(watermark_reader).rotate) if Info(watermark_reader).rotate is not None else 0

            # 5c. Go through all the input file pages to add a watermark to them
            for page_number in range(page_count):
                # Merge the watermark with the page
                if not self.underneath:
                    input_page = document_reader.getPage(page_number)
                    if wtrmrk_rotate is not 0:
                        input_page.mergeRotatedTranslatedPage(wtrmrk_page, wtrmrk_rotate, wtrmrk_width, wtrmrk_height)
                    else:
                        wtrmrk_width = 0
                        wtrmrk_height = 0
                        input_page.mergeTranslatedPage(wtrmrk_page, wtrmrk_width, wtrmrk_height)
                else:
                    size = Info(document_reader).dimensions
                    input_page = PageObject().createBlankPage(document_reader, size['w'], size['h'])
                    if wtrmrk_rotate is not 0:
                        input_page.mergeRotatedTranslatedPage(wtrmrk_page, wtrmrk_rotate, wtrmrk_width, wtrmrk_height)
                    else:
                        wtrmrk_width = 0
                        wtrmrk_height = 0
                        input_page.mergeTranslatedPage(wtrmrk_page, wtrmrk_width, wtrmrk_height)
                    input_page.mergePage(document_reader.getPage(page_number))

                # Add page from input file to output document
                output_file.addPage(input_page)

            # 5d. finally, write "output" to PDF
            with open(output_filename, "wb") as outputStream:
                output_file.write(outputStream)
            return output_filename

        def pdfrw():
            """Faster than PyPDF3 method by as much as 15x."""
            # TODO: Fix issue where watermark is improperly placed on large pagesize PDFs
            # print(Info(document).size)
            # print(Info(watermark).size)
            # print('\n')

            # Open both the source files
            wmark_trailer = PdfReader(watermark)
            trailer = PdfReader(document)

            # Handle different sized pages in same document with
            # a memoization cache, so we don't create more watermark
            # objects than we need to (typically only one per document).

            wmark_page = wmark_trailer.pages[0]
            wmark_cache = {}

            # Process every page
            for pagenum, page in enumerate(trailer.pages, 1):

                # Get the media box of the page, and see
                # if we have a matching watermark in the cache
                mbox = tuple(float(x) for x in page.MediaBox)
                odd = pagenum & 1
                key = mbox, odd
                wmark = wmark_cache.get(key)
                if wmark is None:

                    # Create and cache a new watermark object.
                    wmark = wmark_cache[key] = PageMerge().add(wmark_page)[0]

                    # The math is more complete than it probably needs to be,
                    # because the origin of all pages is almost always (0, 0).
                    # Nonetheless, we illustrate all the values and their names.

                    page_x, page_y, page_x1, page_y1 = mbox
                    page_w = page_x1 - page_x
                    page_h = page_y1 - page_y  # For illustration, not used

                    # Scale the watermark if it is too wide for the page
                    # (Could do the same for height instead if needed)
                    if wmark.w > page_w:
                        wmark.scale(1.0 * page_w / wmark.w)

                    # Always put watermark at the top of the page
                    # (but see horizontal positioning for other ideas)
                    wmark.y += page_y1 - wmark.h

                    # For odd pages, put it at the left of the page,
                    # and for even pages, put it on the right of the page.
                    if odd:
                        wmark.x = page_x
                    else:
                        wmark.x += page_x1 - wmark.w

                    # Optimize the case where the watermark is same width
                    # as page.
                    if page_w == wmark.w:
                        wmark_cache[mbox, not odd] = wmark

                # Add the watermark to the page
                PageMerge(page).add(wmark, prepend=self.underneath).render()

            # Write out the destination file
            PdfWriter(output_filename, trailer=trailer).write()

        if self.method is 'pypdf3':
            return pypdf3()
        else:
            return pdfrw()
