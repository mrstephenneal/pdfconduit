# Set directory paths and file names
import os
import sys
from inspect import stack
from pathlib import Path


def bundle_dir():
    """Handle resource management within an executable file."""
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(stack()[1][1]))
    if os.path.exists(bundle_dir):
        return bundle_dir


def resource_path(relative):
    """Adjust path for executable use in executable file"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


if 'pathlib' in sys.modules:
    def _add_suffix(file_path, suffix, sep, ext):
        p = Path(file_path)
        _ext = p.suffix if ext is None else str('.' + ext.strip('.'))
        out = p.stem + sep + suffix + _ext  # p.suffix is file extension
        return os.path.join(os.path.dirname(file_path), out)
else:
    def _add_suffix(file_path, suffix, sep, ext):
        split = os.path.basename(file_path).rsplit('.', 1)
        ext = split[1] if ext is None else ext
        return os.path.join(os.path.dirname(file_path), split[0] + sep + suffix + '.' + ext)


def add_suffix(file_path, suffix='modified', sep='_', ext=None):
    """Adds suffix to a file name seperated by an underscore and returns file path."""
    return _add_suffix(file_path, suffix, sep, ext)


def set_destination(source, suffix, filename=False, ext=None):
    """Create new pdf filename for temp files"""
    source_dirname = os.path.dirname(source)

    # Do not create nested temp folders (/temp/temp)
    if not source_dirname.endswith('temp'):
        directory = os.path.join(source_dirname, 'temp')  # directory
    else:
        directory = source_dirname

    # Create temp dir if it does not exist
    if not os.path.isdir(directory):
        os.mkdir(directory)

    # Parse source filename
    if filename:
        src_file_name = filename
    else:
        src_file_name = Path(source).stem  # file name
    if ext:
        src_file_ext = ext
    else:
        src_file_ext = Path(source).suffix  # file extension

    # Concatenate new filename
    dst_path = src_file_name + '_' + suffix + src_file_ext
    full_path = os.path.join(directory, dst_path)  # new full path

    if not os.path.exists(full_path):
        return full_path
    else:
        # If file exists, increment number until filename is unique
        number = 1
        while True:
            dst_path = src_file_name + '_' + suffix + '_' + str(number) + src_file_ext
            if not os.path.exists(dst_path):
                break
            number = number + 1
        full_path = os.path.join(directory, dst_path)  # new full path
        return full_path
