from .pdf_processing import ProcessPdf

'''
    replace all the constants (the one in caps) with your own lists
'''

data = DATA_OBJECT_HERE

output_file = 'final_pdf.pdf'

temp_files = []

pdf = ProcessPdf('pdf_temp/', output_file)

data_pdf = pdf.add_data_to_pdf(PDF_TEMPLATE_PATH_HERE, data)

temp_files.append(data_pdf)

data_image_pdf = pdf.add_image_to_pdf(data_pdf, IMAGES, POSITIONS)

temp_files.append(data_image_pdf)

compressed_pdf = pdf.compress_pdf(data_image_pdf)

pdf.delete_tempfiles(temp_files)

