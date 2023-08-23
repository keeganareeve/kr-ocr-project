'''
Converts a page from a PDF file to PNG.

To run this script:
    python3 pdf_page_to_png.py "pages.pdf" <page_number>  

Page numbers (represented by filenames of png output files) begin from the number 1.
'''

import PyPDF2
from pdf2image import convert_from_path

if len(sys.argv) < 2:
    image_filepath = "./test1.pdf"
else:
    image_filepath = sys.argv[1]

if len(sys.argv) < 3:
    page_number_to_convert = 65
else:
    page_number_to_convert = sys.argv[2]
if len(sys.argv) < 4:
    output_directory = "./"
else:
    output_directory = sys.argv[3]

def convert_page_to_png(pdf_path, page_number, output_path):
    with open(pdf_path, 'rb') as file:
        # PdfFileReader() is now deprecated, but PdfReader() worked instead
        reader = PyPDF2.PdfReader(file)

        # Check if the requested page number is within the valid range
        if page_number < 0 or page_number >= len(reader.pages):
            print(
                f"The page number exceeds the number of pages in the document. The PDF has {len(reader.pages)} pages.")
            return

        # Convert the requested page to an image
        images = convert_from_path(
            pdf_path, first_page=page_number + 1, last_page=page_number + 1)

        # Save the image as PNG
        images[0].save(output_path, 'PNG')
        print(f"Page {page_number + 1} converted to PNG successfully.")


output_image = f'{output_directory}page{page_number_to_convert}.png'
convert_page_to_png(pdf_file, page_number_to_convert, output_image)
