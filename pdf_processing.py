import os
import re

import fitz  # requires fitz, PyMuPDF
import pdfrw
import subprocess
import os.path
import sys
from PIL import Image

'''
    replace all the constants (the one in caps) with your own lists
'''


FORM_KEYS = {
    "fname" : "string",
    "lname" : "string",
    "sex" : :checkbox",
    "mobile" : "number"
}

'''
FORM_KEYS is a dictionary (key-value pair) that contains 
1. keys - which are all the key names in the PDF form 
2. values - which are the type for all the keys in the PDF form. (string, checkbox, etc.)

Eg. PDF form contains 
1. First Name
2. Last Name
3. Sex (Male or Female)

This FORM_KEYS(key) returns the type of value for that key. I'm passing this as 2nd argument to encode_pdf_string() function.
'''


class ProcessPdf:

    def __init__(self, temp_directory, output_file):
        print('\n##########| Initiating Pdf Creation Process |#########\n')
        
        print('\nDirectory for storing all temporary files is: ', temp_directory)
        self.temp_directory = temp_directory
        print("Final Pdf name will be: ", output_file)
        self.output_file = output_file

    def add_data_to_pdf(self, template_path, data):
        print('\nAdding data to pdf...')
        template = pdfrw.PdfReader(template_path)

        for page in template.pages:
            annotations = page['/Annots']
            if annotations is None:
                continue

            for annotation in annotations:
                if annotation['/Subtype'] == ['/Widget']:
                    if annotation['/T']:
                        key = annotation['/T'][1:-1]
                        if re.search(r'.-[0-9]+', key):
                            key = key[:-2]
                        
                        if key in data:
                            annotation.update(
                                pdfrw.PdfDict(V=self.encode_pdf_string(data[key], FORM_KEYS[key]))
                            )
                        annotation.update(pdfrw.PdfDict(Ff=1))

        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(self.temp_directory + "data.pdf", template)
        print('Pdf saved')

        return self.temp_directory + "data.pdf"

    def encode_pdf_string(self, value, type):
        if type == 'string':
            if value:
                return pdfrw.objects.pdfstring.PdfString.encode(value.upper())
            else:
                return pdfrw.objects.pdfstring.PdfString.encode('')
        elif type == 'checkbox':
            if value == 'True' or value == True:
                return pdfrw.objects.pdfname.BasePdfName('/Yes')
                # return pdfrw.objects.pdfstring.PdfString.encode('Y')
            else:
                return pdfrw.objects.pdfname.BasePdfName('/No')
                # return pdfrw.objects.pdfstring.PdfString.encode('')
        return ''

    def convert_image_to_pdf(self, image_path, image_pdf_name):
        print('\nConverting image to pdf...')

        image = Image.open(image_path)
        image_rgb = image.convert('RGB')
        image_rgb.save(self.temp_directory + image_pdf_name)
        return self.temp_directory + image_pdf_name

    def add_image_to_pdf(self, pdf_path, images, positions):
        print('\nAdding images to Pdf...')

        file_handle = fitz.open(pdf_path)
        for position in positions:
            page = file_handle[int(position['page']) - 1]
            if not position['image'] in images:
                continue
            image = images[position['image']]
            page.insertImage(
                fitz.Rect(position['x0'], position['y0'], position['x1'], position['y1']),
                filename=image
            )

        file_handle.save(self.temp_directory + "data_image.pdf")
        print('images added')
        return self.temp_directory + "data_image.pdf"

    def delete_temp_files(self, pdf_list):
        print('\nDeleting Temporary Files...')
        for path in pdf_list:
            try:
                os.remove(path)
            except:
                pass

    def compress_pdf(self, input_file_path, power=3):
        """Function to compress PDF via Ghostscript command line interface"""
        quality = {
            0: '/default',
            1: '/prepress',
            2: '/printer',
            3: '/ebook',
            4: '/screen'
        }

        output_file_path = self.temp_directory + 'compressed.pdf'

        if not os.path.isfile(input_file_path):
            print("\nError: invalid path for input PDF file")
            sys.exit(1)

        if input_file_path.split('.')[-1].lower() != 'pdf':
            print("\nError: input file is not a PDF")
            sys.exit(1)

        print("\nCompressing PDF...")
        initial_size = os.path.getsize(input_file_path)
        subprocess.call(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                        '-dPDFSETTINGS={}'.format(quality[power]),
                        '-dNOPAUSE', '-dQUIET', '-dBATCH',
                        '-sOutputFile={}'.format(output_file_path),
                         input_file_path]
        )
        final_size = os.path.getsize(output_file_path)
        ratio = 1 - (final_size / initial_size)
        print("\nCompression by {0:.0%}.".format(ratio))
        print("Final file size is {0:.1f}MB".format(final_size / 1000000))
        return output_file_path

