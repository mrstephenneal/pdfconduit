from pdfconduit import Flatten
from pdfconduit.utils.gui import get_directory


def main():
    d = get_directory()

    flat = Flatten(d, scale=1.5, progress_bar='gui').save(remove_temps=False)
    print(flat)


if __name__ == '__main__':
    main()