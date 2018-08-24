# Test encrypt module reliability
from pdfconduit import Encrypt, Info
from tests import pdf


def main():
    print('Testing Encrypt reliability')
    owner_pw = 'foo'
    user_pw = 'baz'

    p = Encrypt(pdf, user_pw, owner_pw)
    print(p.output)

    security = Info(p.output, user_pw).security

    try:
        assert Info(p.output, user_pw).encrypted is True
        assert security['/Length'] == 128
        assert security['/P'] == -1852
        print('Success!')
    except AssertionError:
        print('Failed!')


if __name__ == '__main__':
    main()
