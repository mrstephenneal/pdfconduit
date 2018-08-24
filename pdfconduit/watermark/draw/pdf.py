# Dynamically generate watermark pdf file
import io
from tempfile import NamedTemporaryFile, mkdtemp
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pdfconduit.utils import resource_path, write_pdf, LETTER
from pdfconduit.watermark.draw.image import img_opacity
from pdfconduit.watermark.canvas import CanvasStr, CanvasImg


def text_width(string, font_name, font_size):
    """Determine with width in pixels of string."""
    return stringWidth(string, fontName=font_name, fontSize=font_size)


def center_str(txt, font_name, font_size, offset=0):
    """Center a string on the x axis of a reportslab canvas"""
    return -(text_width(txt, font_name, font_size) / 2.0) + offset


def split_str(string):
    """Split string in half to return two strings"""
    split = string.split(' ')
    return ' '.join(split[:len(split) // 2]), ' '.join(split[len(split) // 2:])


class DrawPDF:
    def __init__(self, tempdir=None, compress=0, pagesize=LETTER):
        if tempdir:
            self.dir = tempdir
        else:
            self.dir = mkdtemp()
        tmppdf = NamedTemporaryFile(suffix='.pdf', dir=self.dir, delete=False)
        self.dst = resource_path(tmppdf.name)

        # create a new PDF with Reportlab
        self.packet = io.BytesIO()
        self.can = Canvas(self.packet, pagesize=pagesize, pageCompression=compress, bottomup=1)  # Initialize canvas

    def __str__(self):
        return str(self.dst)

    def _write(self):
        self.packet.seek(0)  # move to the beginning of the StringIO buffer
        write_pdf(self.packet, self.dst)  # Save new pdf file
        return self.dst

    def write(self):
        return self._write()


class WatermarkDraw(DrawPDF):
    def __init__(self, canvas_objects, rotate=0, compress=0, pagesize=LETTER, tempdir=None):
        super(WatermarkDraw, self).__init__(tempdir, compress, pagesize)
        self.canvas_objects = canvas_objects
        self.rotate = rotate

        self.draw()

    def draw(self):
        # Move canvas origin to the middle of the page
        self.can.translate(self.can._pagesize[0] / 2, self.can._pagesize[1] / 2)

        # Rotate canvas
        self.can.rotate(self.rotate)

        # Iterate canvas objects and determine if string or image
        for obj in self.canvas_objects:
            # Adjust x and y based on rotation
            obj.x += int(self.rotate * 1.5)
            obj.y += -int(self.rotate * 3)

            # Check if CanvasObject is a string or image
            if isinstance(obj, CanvasStr):
                self._draw_string(obj)
            elif isinstance(obj, CanvasImg):
                self._draw_image(obj)
        self.can.showPage()
        self.can.save()

    def _draw_image(self, ci):
        """
        Draw image object to reportlabs canvas.

        :param ci: CanvasImage object
        """
        img = img_opacity(ci.image, ci.opacity, tempdir=self.dir)
        self.can.drawImage(img, x=ci.x, y=ci.y, width=ci.w, height=ci.h, mask=ci.mask,
                           preserveAspectRatio=ci.preserve_aspect_ratio, anchorAtXY=True)

    def _draw_string(self, cs):
        """
        Draw string object to reportlabs canvas.

        Canvas Parameter changes (applied if set values differ from string object values)
        1. Font name
        2. Font size
        3. Font fill color & opacity
        4. X and Y position

        :param cs: CanvasString object
        """
        # 1. Font name
        if self.can._fontname != cs.font:
            self.can.setFont(cs.font, cs.size)

        # 2. Font size
        elif self.can._fontsize != cs.size:
            self.can.setFontSize(cs.size)

        # 3. Font file color
        self.can.setFillColor(cs.color, cs.opacity)

        # 4. X and Y positions
        # X and Y are both centered
        if cs.y_centered and cs.x_centered:
            # Check if text_width is greater than the canvas page width
            if text_width(cs.string, cs.font, cs.size) > self.can._pagesize[0]:
                str1, str2 = split_str(cs.string)
                self.can.drawString(x=center_str(str1, cs.font, cs.size, offset=0), y=cs.size, text=str1)
                self.can.drawString(x=center_str(str2, cs.font, cs.size, offset=0), y=-cs.size, text=str2)
                return
            else:
                x = center_str(cs.string, cs.font, cs.size, offset=0)
                y = 0

        # Y is centered and X is not
        elif cs.y_centered and not cs.x_centered:
            x = cs.x
            y = 0

        # X is centered and Y is not
        elif cs.x_centered and not cs.y_centered:
            x = center_str(cs.string, cs.font, cs.size, offset=0)
            y = cs.y
        else:
            x = cs.x
            y = cs.y
        self.can.drawString(x=x, y=y, text=cs.string)
        return
