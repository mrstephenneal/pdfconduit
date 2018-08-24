# -*- mode: python -*-

block_cipher = None


a = Analysis(['watermarker.py'],
             pathex=['C:\\Users\\Stephen\\Scripts\\pdfconduit'],
             binaries=[],
             datas=[('pdfconduit/utils/lib/font', 'lib/font'), ('pdfconduit/utils/lib/img', 'lib/img')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Watermarker',
          icon='pdfconduit/utils/lib/icon/stamp.ico',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )