# Retrieve information about a PDF document
from PyPDF3 import PdfFileReader


class Info:
    def __init__(self, path, password=None, prompt=True):
        self.pdf = self._reader(path, password, prompt)

    @staticmethod
    def _reader(path, password, prompt):
        """Read PDF and decrypt if encrypted."""
        pdf = PdfFileReader(path) if not isinstance(path, PdfFileReader) else path
        # Check that PDF is encrypted
        if pdf.isEncrypted:
            # Check that password is none
            if not password:
                pdf.decrypt('')
                # Try and decrypt PDF using no password, prompt for password
                if pdf.isEncrypted and prompt:
                    print('No password has been given for encrypted PDF ', path)
                    password = input('Enter Password: ')
                else:
                    return False
            pdf.decrypt(password)
        return pdf

    @staticmethod
    def _resolved_objects(pdf, xobject):
        """Retrieve rotatation info."""
        return [pdf.getPage(i).get(xobject) for i in range(pdf.getNumPages())][0]

    @property
    def encrypted(self):
        """Check weather a PDF is encrypted"""
        return True if self.pdf.isEncrypted else False

    @property
    def decrypted(self):
        """Check weather a PDF is encrypted"""
        return True if self.pdf.isDecrypted else False

    @property
    def pages(self):
        """Retrieve PDF number of pages"""
        return self.pdf.getNumPages()

    @property
    def metadata(self):
        """Retrieve PDF metadata"""
        return self.pdf.getDocumentInfo()

    def resources(self):
        """Retrieve contents of each page of PDF"""
        return [self.pdf.getPage(i) for i in range(self.pdf.getNumPages())]

    @property
    def security(self):
        """Print security object information for a pdf document"""
        return {k: v for i in self.pdf.resolvedObjects.items() for k, v in i[1].items()}

    @property
    def dimensions(self):
        """Get width and height of a PDF"""
        size = self.pdf.getPage(0).mediaBox
        return {'w': float(size[2]), 'h': float(size[3])}

    @property
    def size(self):
        """Get width and height of a PDF"""
        size = self.pdf.getPage(0).mediaBox
        return float(size[2]), float(size[3])

    @property
    def rotate(self):
        """Retrieve rotation info."""
        return self._resolved_objects(self.pdf, '/Rotate')
