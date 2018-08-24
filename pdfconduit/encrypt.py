# Encrypt a PDF file with password protection
from pdfconduit.utils import add_suffix
from PyPDF3 import PdfFileReader, PdfFileWriter


class Encrypt:
    def __init__(self, pdf, user_pw, owner_pw=None, output=None, suffix='secured', bit128=True, allow_printing=True,
                 allow_commenting=False, overwrite_permission=None, progress_bar_enabled=False, progress_bar='gui'):
        """Password protect PDF file and allow all other permissions."""
        self.pdf = pdf
        self.user_pw = user_pw
        self.owner_pw = owner_pw
        self.output = add_suffix(pdf, suffix=suffix) if not output else output
        self.encrypt_128 = bit128
        self.allow_printing = allow_printing
        self.allow_commenting = allow_commenting
        self.overwrite_permission = overwrite_permission
        self.progress_bar_enabled = progress_bar_enabled
        self.progress_bar = progress_bar

        self.encrypt()

    def __str__(self):
        return str(self.output)

    def encrypt(self):
        # Create PDF writer object
        pdf_writer = PdfFileWriter()
        with open(self.pdf, 'rb') as pdf_file:
            # Read opened PDF file
            pdf_reader = PdfFileReader(pdf_file)

            # Add each page from source PDF
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

            # Apply encryption to writer object
            pdf_writer.encrypt(self.user_pw, self.owner_pw, use_128bit=self.encrypt_128,
                               allow_printing=self.allow_printing, allow_commenting=self.allow_commenting,
                               overwrite_permission=self.overwrite_permission)

            pdf_writer.addMetadata({
                '/Producer': 'pdfconduit',
                '/Creator': 'HPA Design',
                '/Author': 'HPA Design',
            })

            # Write encrypted PDF to file
            with open(self.output, 'wb') as output_pdf:
                # pdf_writer.write(output_pdf, progress_bar='gui')
                pdf_writer.write(output_pdf, progress_bar=self.progress_bar,
                                 progress_bar_enabled=self.progress_bar_enabled)
        return self.output


def main():
    from pdfconduit.utils.gui import GUI
    GUI.encrypt()


if __name__ == '__main__':
    main()
