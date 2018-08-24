# View directories and files in a window
from pathlib import Path
from subprocess import call, Popen


def open_window(path):
    """Open path in finder or explorer window"""
    try:
        call(["open", "-R", str(Path(str(path)))])
    except FileNotFoundError:
        Popen(r'explorer /select,' + str(Path(str(path))))