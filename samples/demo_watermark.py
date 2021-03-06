from pdfconduit import Watermark
import os
from tests import pdf_path, test_data_dir
from looptools import Timer


@Timer.decorator
def main(move_temps):
    print('Testing Watermark draw and add functionality')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'

    w = Watermark(pdf_path, use_receipt=False, move_temps=move_temps)
    wtrmrk = w.draw(address, str(town + ', ' + state), opacity=0.08, flatten=False, rotate=30)
    added = w.add()
    w.cleanup()

    try:
        # File checks
        assert os.path.exists(wtrmrk) is False
        assert os.path.exists(added) is True
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main(test_data_dir)
