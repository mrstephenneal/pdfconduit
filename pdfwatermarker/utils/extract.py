# Extract images from a PDF
from PIL import Image


def extract_img(page):
    xobj = page['/Resources']['/XObject'].getObject()
    for obj in xobj:
        if xobj[obj]['/Subtype'] == '/Image':
            print(obj)
            size = (xobj[obj]['/Width'], xobj[obj]['/Height'])
            data = xobj[obj].getData()
            if xobj[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if xobj[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(obj[1:] + ".png")  # TODO: Add save destination parameter
            elif xobj[obj]['/Filter'] == '/DCTDecode':
                img = open(obj[1:] + ".jpg", "wb")
                img.write(data)
                img.close()
            elif xobj[obj]['/Filter'] == '/JPXDecode':
                img = open(obj[1:] + ".jp2", "wb")
                img.write(data)
                img.close()