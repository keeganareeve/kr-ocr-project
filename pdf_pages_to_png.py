'''
Converts each page of a PDF file into a separate PNG for the PNG files to be used in other scripts.

To run:
    python3 pdf_pages_to_png.py {pdf_filepath} {output_directory}
'''

import sys
import PyPDF2
from pdf2image import convert_from_path

if len(sys.argv) < 2:
    pdf_filepath = "./inputForCropping/test1.pdf"
else:
    pdf_filepath = str(sys.argv[1])
if len(sys.argv) < 3:
    # make sure this ends with a "/"
    output_directory = "./output_pngs/"
else:
    output_directory = str(sys.argv[2])


def convert_page_to_png(pdf_path, page_number, output_path):
    with open(pdf_path, 'rb') as file:
        # PdfFileReader() is now deprecated, but PdfReader() worked instead
        reader = PyPDF2.PdfReader(file)
        # Check if requested page number is within range
        if page_number < 0 or page_number >= len(reader.pages):
            print(
                f"The page number exceeds the number of pages in the document. The PDF has {len(reader.pages)} pages.")
            return
        # Convert to image
        images = convert_from_path(
            pdf_path, first_page=page_number + 1, last_page=page_number + 1)
        # Save image
        images[0].save(output_path, 'PNG')
        # print(
        # f"Page {page_number + 1} converted to PNG successfully as {output_path}")


def count_pgs(pdf_filepath):
    try:
        with open(pdf_filepath, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_count = len(pdf_reader.pages)
            return page_count
    except Exception as e:
        print(f"Error: {e}")
        return None


page_count = count_pgs(pdf_filepath)
if page_count is not None:
    print(f"The PDF file '{pdf_filepath}' has {page_count} pages.")

for page_number in range(0, page_count):
    output_image = f'{output_directory}{pdf_filepath.split("/")[-1][:-4]}page{page_number+1}.png'
    convert_page_to_png(pdf_filepath, page_number, output_image)
    print(
        f'Saved page {page_number} of {pdf_filepath} as a PNG file as {output_image}')
