import os
import PySimpleGUI as gui
from platform import system
from pdfconduit import __version__
from pdfconduit.utils import available_images


def get_directory():
    with gui.FlexForm('Source Directory') as form:
        form_rows = [
            [gui.Text('Enter the Source folders')],
            [gui.Text('Destination Folder', size=(15, 1), justification='right'), gui.InputText('Dest'), gui.FolderBrowse()],
            [gui.Submit(), gui.Cancel()]]

        button, (source) = form.LayoutAndRead(form_rows)
        return source[0]


def get_file():
    with gui.FlexForm('Source File') as form:
        form_rows = [
            [gui.Text('Select a source file')],
            [gui.Text('Source File', size=(15, 1), justification='right'), gui.InputText(),
             gui.FileBrowse(file_types=(("PDF Files", "*.pdf"),))],
            [gui.Submit(), gui.Cancel()]]

        button, (source) = form.LayoutAndRead(form_rows)
        return source[0]


def _line(char='_', width=105, size=(75, 1)):
    return gui.Text(char * width, size=size)


class GUI:
    @staticmethod
    def encrypt():
        from pdfconduit.encrypt import Encrypt

        title = 'PDF Encryptor'
        label_w = 20

        def header():
            return [[gui.Text('HPA Design', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('PDF Encryption utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
                    [_line()]]

        def footer(message='Click Submit to encrypt PDF'):
            return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]

        def folder(params):
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source folder', size=(label_w, 1), auto_size_text=False),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FolderBrowse(button_text='Folder')],

                    [_line()],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            params['pdf'] = values[0]
            return params

        def settings(p):
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source PDF file', size=(label_w, 1), auto_size_text=False), gui.InputText(p['pdf']),
                     gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
                     gui.SimpleButton('Folder')],

                    [_line()],

                    # Encryption
                    [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                    [gui.Text('User Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                    [gui.Text('Owner Password', size=(label_w, 1), auto_size_text=False), gui.InputText()],
                    [gui.Checkbox('128 bit encryption', default=True)],
                    [gui.Checkbox('Allow Printing', default=True), gui.Checkbox('Allow Commenting', default=False)],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            user_pw = values[1] if len(values[1]) > 0 else ''
            owner_pw = values[2] if len(values[2]) > 0 else ''
            params = {
                'pdf': values[0],
                'user_pw': user_pw,
                'owner_pw': owner_pw,
                '128bit': values[3],
                'allow_printing': values[4],
                'allow_commenting': values[5],
            }
            if button == 'Folder':
                params = folder(params)
                params = settings(params)
            return params

        p = {
            'pdf': '',
            'user_pw': '',
            'owner_pw': '',
            '128bit': True,
            'allow_printing': True,
            'allow_commenting': False,
        }

        p = settings(p)

        if os.path.isfile(p['pdf']):
            p['pdf'] = [p['pdf']]
        elif os.path.isdir(p['pdf']):
            src_dir = p['pdf']
            p['pdf'] = [os.path.join(src_dir, pdf) for pdf in os.listdir(src_dir) if pdf.endswith('.pdf')]

        for pdf in p['pdf']:
            e = Encrypt(pdf, p['user_pw'], p['owner_pw'], bit128=p['128bit'], allow_printing=p['allow_printing'],
                        allow_commenting=p['allow_commenting'])
        return str(e)

    @staticmethod
    def watermark():
        from pdfconduit.utils import Receipt
        from pdfconduit.watermark import Watermark
        from pdfconduit.flatten import Flatten

        label_w = 20
        title = 'PDF Watermarker'

        def header():
            return [[gui.Text('HPA Design', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('PDF Watermark utility', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
                    [gui.Text('version: ' + __version__, size=(30, 1), font=("Helvetica", 16), text_color='blue')],
                    [_line()]]

        def footer(message='Click Submit to watermark PDF'):
            return [[gui.Text(message)], [gui.Submit(), gui.Cancel()]]

        def folder(params):
            with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                inputs = [
                    # Source
                    [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                    [gui.Text('Source folder', size=(label_w, 1), auto_size_text=False),
                     gui.InputText(params['pdf'], size=(30, 1)),
                     gui.FolderBrowse(button_text='Folder')],

                    [_line()],
                ]
                layout = []
                layout.extend(header())
                layout.extend(inputs)
                layout.extend(footer())

                (button, (values)) = form.LayoutAndShow(layout)

            params['pdf'] = values[0]
            return params

        def input_source():
            return [
                # Source
                [gui.Text('Source', font=('Helvetica', 15), justification='left')],
                [gui.Text('Source file or folder', size=(label_w, 1), auto_size_text=False),
                 gui.InputText(params['pdf'], size=(30, 1), key='pdf'),
                 gui.FileBrowse(button_text='File', file_types=(("PDF Files", "*.pdf"),)),
                 gui.SimpleButton('Folder')],
                [_line()],
            ]

        def input_text():
            return [
                # Watermark Text
                [gui.Text('Project address', font=('Helvetica', 15), justification='left')],
                [gui.Text('Address', size=(label_w, 1), auto_size_text=False), gui.InputText(params['address'], key='address')],
                [gui.Text('Town', size=(label_w, 1), auto_size_text=False), gui.InputText(params['town'], key='town')],
                [gui.Text('State', size=(label_w, 1), auto_size_text=False), gui.InputText(params['state'], key='state')],

                [_line()],
            ]

        def input_watermark_settings():
            return [
                # Watermark Settings
                [gui.Text('Watermark Settings', font=('Helvetica', 15), justification='left')],
                [gui.Text('Logo Image', size=(label_w, 1), auto_size_text=False),
                 gui.InputCombo(values=(params['image']), size=(30, 4), key='image')],

                [gui.Text('File Compression', size=(label_w, 1), auto_size_text=False),
                 gui.Radio('Uncompressed', "RADIO1", default=params['compression']['uncompressed'], key='uncompressed'),
                 gui.Radio('Compressed', "RADIO1", default=params['compression']['compressed'], key='compressed')],

                [gui.Text('Watermark Flattening', size=(label_w, 1), auto_size_text=False),
                 gui.Radio('Flattened', "RADIO3", default=params['flattening']['flattened'], key='flattened'),
                 gui.Radio('Layered', "RADIO3", default=params['flattening']['layered'], key='layered')],
                [gui.Text('Watermark Placement', size=(label_w, 1), auto_size_text=False),
                 gui.Radio('Overlay', "RADIO2", default=params['placement']['overlay'], key='overlay'),
                 gui.Radio('Underneath', "RADIO2", default=params['placement']['underneath'], key='underneath')],

                [gui.Text('Opacity', size=(label_w, 1), auto_size_text=False),
                 gui.Slider(range=(1, 20), orientation='h', size=(34, 30), default_value=params['opacity'], key='opacity')],

                [_line()],
            ]

        def input_encryption():
            return [
                # Encryption
                [gui.Text('Encryption Settings', font=('Helvetica', 15), justification='left')],
                [gui.Checkbox('Encrypt', default=params['encrypt'], key='encrypt'),
                 gui.Checkbox('Allow Printing', default=params['allow_printing'], key='allow_printing'),
                 gui.Checkbox('Allow Commenting', default=params['allow_commenting'], key='allow_commenting')],
                [gui.Text('User Password', size=(label_w, 1), auto_size_text=False),
                 gui.InputText(params['user_pw'], key='user_pw')],
                [gui.Text('Owner Password', size=(label_w, 1), auto_size_text=False),
                 gui.InputText(params['owner_pw'], key='owner_pw')],

                [_line()],
                [gui.Checkbox('Flatten PDF pages', default=params['flat'], key='flat')],
            ]

        def window():
            """GUI window for inputing Watermark parameters"""
            platform = system()
            if system() is 'Windows':
                with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                    with gui.FlexForm(title) as form2:
                        layout_tab_1 = []
                        layout_tab_1.extend(header())
                        layout_tab_1.extend(input_source())
                        layout_tab_1.extend(input_text())
                        layout_tab_1.extend(input_encryption())
                        layout_tab_1.extend(footer())

                        layout_tab_2 = []
                        layout_tab_2.extend(input_watermark_settings())

                        r = gui.ShowTabbedForm(title, (form, layout_tab_1, 'Document Settings'),
                                               (form2, layout_tab_2, 'Watermark Settings'))
                        values = []
                        button = None
                        for but, result in r:
                            if but is not None:
                                button = but
                            values.extend(result)
                        return button, values, platform
            else:
                with gui.FlexForm(title, auto_size_text=True, default_element_size=(40, 1)) as form:
                    layout = []
                    layout.extend(header())
                    layout.extend(input_source())
                    layout.extend(input_text())
                    layout.extend(input_watermark_settings())
                    layout.extend(input_encryption())
                    layout.extend(footer())
                    button, values = form.LayoutAndShow(layout)
                    return button, values, platform

        def settings(params):
            # Fix opacity if it is adjusted$
            if params['opacity'] < 1:
                params['opacity'] = int(params['opacity'] * 100)

            button, values, platform = window()

            params['pdf'] = values['pdf'] if platform == 'Darwin' else values[0]
            params['address'] = values['address'] if platform == 'Darwin' else values[1]
            params['town'] = values['town'] if platform == 'Darwin' else values[2]
            params['state'] = values['state'] if platform == 'Darwin' else values[3]

            params['image'] = values['image'] if platform == 'Darwin' else values[10]
            params['compression']['uncompressed'] = values['uncompressed'] if platform == 'Darwin' else values[11]
            params['compression']['compressed'] = values['compressed'] if platform == 'Darwin' else values[12]
            params['flattening']['flattened'] = values['flattened'] if platform == 'Darwin' else values[13]
            params['flattening']['layered'] = values['layered'] if platform == 'Darwin' else values[14]
            params['placement']['overlay'] = values['overlay'] if platform == 'Darwin' else values[15]
            params['placement']['underneath'] = values['underneath'] if platform == 'Darwin' else values[16]
            params['opacity'] = float(values['opacity'] * .01) if platform == 'Darwin' else float(values[17] * .01)

            params['encrypt'] = values['encrypt'] if platform == 'Darwin' else values[4]
            params['allow_printing'] = values['allow_printing'] if platform == 'Darwin' else values[5]
            params['allow_commenting'] = values['allow_commenting'] if platform == 'Darwin' else values[6]
            params['user_pw'] = values['user_pw'] if platform == 'Darwin' else values[7]
            if not len(params['user_pw']) > 0:
                params['user_pw'] = ''
            params['owner_pw'] = values['owner_pw'] if platform == 'Darwin' else values[8]
            if not len(params['owner_pw']) > 0:
                params['owner_pw'] = ''
            params['flat'] = values['flat'] if platform == 'Darwin' else values[9]
            if button == 'Folder':
                params = folder(params)
                params = settings(params)

            return params

        params = {
            'pdf': '',
            'address': '',
            'town': '',
            'state': '',
            'image': available_images(),
            'compression': {
                'uncompressed': True,
                'compressed': False
            },
            'flattening': {
                'flattened': True,
                'layered': False,
            },
            'placement': {
                'overlay': True,
                'underneath': False
            },
            'opacity': 8,
            'encrypt': True,
            'allow_printing': True,
            'allow_commenting': False,
            'user_pw': '',
            'owner_pw': '',
            'flat': False,
        }

        params = settings(params)

        if os.path.isfile(params['pdf']):
            params['pdf'] = [params['pdf']]
        elif os.path.isdir(params['pdf']):
            src_dir = params['pdf']
            params['pdf'] = [os.path.join(src_dir, pdf) for pdf in os.listdir(src_dir) if pdf.endswith('.pdf')]

        receipt = Receipt(gui=True)
        receipt.set_dst(params['pdf'][0])

        for pdf in params['pdf']:
            # Execute Watermark class
            wm = Watermark(pdf, receipt=receipt, progress_bar='gui', progress_bar_enabled=True)
            wm.draw(text1=params['address'],
                    text2=str(params['town'] + ', ' + params['state']),
                    image=params['image'],
                    opacity=params['opacity'],
                    compress=params['compression']['compressed'],
                    flatten=params['flattening']['flattened'])
            doc = wm.add(underneath=params['placement']['underneath'], method='pdfrw')
            if params['flat']:
                doc = Flatten(doc, 2.0, progress_bar='gui', tempdir=wm.tempdir).save()
            if params['encrypt']:
                doc = wm.encrypt(params['user_pw'], params['owner_pw'], document=doc)

        wm.cleanup()

        print('\nSuccess!')

