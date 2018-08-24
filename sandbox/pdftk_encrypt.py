"""
Encrypt a PDF file using pdftk

pdftk server must be installed on your machine
https://www.pdflabs.com/tools/pdftk-server/
"""
import os
from PyPDF2 import PdfFileReader


# Replace with your own pdftk path
PDFTK_PATH = '/opt/pdflabs/pdftk/bin/pdftk'


def get_pdftk_path():
    if os.path.exists(PDFTK_PATH):
        return PDFTK_PATH


def add_suffix(file_path, suffix):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    split = os.path.basename(file_path).rsplit('.', 1)
    ext = split[1]
    name = split[0]
    out = str(name + '_' + suffix + '.' + ext)
    return os.path.join(os.path.dirname(file_path), out)


def secure(pdf, user_pw, owner_pw, restrict_permission=True, pdftk=get_pdftk_path(), output=None):
    """
    Encrypt a PDF file and restrict permissions to print only.

    Utilizes pdftk command line tool.

    :param pdf: Path to PDF file
    :param user_pw: Password to open and view
    :param owner_pw: Password to modify permissions
    :param restrict_permission: Restrict permissions to print only
    :param pdftk: Path to pdftk binary
    :param output: Output path
    :return: Output path
    """
    if pdftk:
        # Check that PDF file is encrypted
        with open(pdf, 'rb') as f:
            reader = PdfFileReader(f)
            if reader.isEncrypted:
                print('PDF is already encrypted')
                return pdf

        # Create output filename if not already set
        if not output:
            output = add_suffix(pdf, 'secured')

        # Replace spaces within paths with backslashes followed by a space
        pdf_en = pdf.replace(' ', '\ ')
        output_en = output.replace(' ', '\ ')

        # Concatenate bash command
        command = pdftk + ' ' + pdf_en + ' output ' + output_en + ' owner_pw ' + owner_pw + ' user_pw ' + user_pw

        # Append string to command if printing is allowed
        if restrict_permission:
            command += ' allow printing'

        # Execute command
        os.system(command)
        print('Secured PDF saved to...', output)
        return output
    else:
        print('Unable to locate pdftk binary')


def main():
    pdf = 'path/to/your/pdf.pdf'
    u = 'userpassword'
    p = 'ownerpassword'
    secure(pdf, u, p)


if __name__ == '__main__':
    main()
