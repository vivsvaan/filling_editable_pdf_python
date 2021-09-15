from .pdf_processing import ProcessPdf

'''
    replace all the constants (the one in caps) with your own lists
'''

'''
    Data Object contains key (keys which are in pdf) and value (actual value) pair
    DATA_OBJECT = {
        'fname': 'Peter', 
        'lname': 'Parker',
        'sex': 'male',
        'mobile': '8888888888'
    }
'''
data = DATA_OBJECT_HERE

output_file = 'final_pdf.pdf'

temp_files = []

pdf = ProcessPdf('pdf_temp/', output_file)

''' 
    PDF_TEMPLATE_PATH = path/to/your.pdf
'''
data_pdf = pdf.add_data_to_pdf(PDF_TEMPLATE_PATH_HERE, data)

temp_files.append(data_pdf)

''' 
IMAGES = {'passport': 'path/to/passport_image.jpg', 'address_proof': 'path/to/address_proof.jpg'}
POSITIONS = [
    {'page': 1, 'x0': 100, 'y0': 100, 'x1': 200, 'y1': 200, 'image': 'passport'},
    {'page': 2, 'x0': 100, 'y0': 100, 'x1': 200, 'y1': 200, 'image': 'address'}
]
'''
data_image_pdf = pdf.add_image_to_pdf(data_pdf, IMAGES, POSITIONS)

temp_files.append(data_image_pdf)

compressed_pdf = pdf.compress_pdf(data_image_pdf)

pdf.delete_tempfiles(temp_files)

