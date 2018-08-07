from pdfwatermarker import Watermark, info
import os
from tests import directory, pdf


def main():
    print('Testing Watermark class reliability')
    address = '43 Indian Lane'
    town = 'Franklin'
    state = 'MA'
    
    w = Watermark(pdf)
    w.draw(address, str(town + ', ' + state), opacity=0.08)
    w.add()
    wm = w.cleanup()

    if os.path.exists(wm):
        print('Success!')


if __name__ == '__main__':
    main()
