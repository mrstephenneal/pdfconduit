# Modify the opacity of an image file
import os
from PIL import Image, ImageEnhance


def _add_suffix(file_path, suffix, sep='_', ext=None):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    # Split file_path on last '.' to separate file_name and file_extension
    split = os.path.basename(file_path).rsplit('.', 1)

    # Use original file_extension if None is given
    ext = split[1] if not ext else ext.strip('.')

    # Rebuild new file_path with suffix
    return os.path.join(os.path.dirname(file_path), split[0] + sep + suffix + '.' + ext)


def img_opacity(image, opacity):
    """
    Reduce the opacity of a PNG image.

    Inspiration: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

    :param image: PNG image file
    :param opacity: float representing opacity percentage
    :return: Path to modified PNG
    """
    # Validate parameters
    assert 0 <= opacity <= 1, 'Opacity must be a float between 0 and 1'
    assert os.path.isfile(image), 'Image is not a file'

    # Open image in RGBA mode if not already in RGBA
    im = Image.open(image)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()

    # Adjust opacity
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)

    # Save modified image file
    dst = _add_suffix(image, str(str(int(opacity * 100)) + '%'), ext='.png')
    im.save(dst)
    return dst


def main():
    image = '/Users/Stephen/Desktop/test.jpg'
    opacity = 0.15
    img_opacity(image, opacity)


if __name__ == '__main__':
    main()
