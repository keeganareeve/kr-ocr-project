'''
Counts the number of pages in a PDF file and returns the total page count.

To run:
    python3 count_pdf_pages.py {pdf_file}
'''

import sys
import PyPDF2


def count_pgs(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            page_count = len(pdf_reader.pages)
            return page_count
    except Exception as e:
        print(f"Error: {e}")
        return None


# Replace 'your_pdf_file.pdf' with the actual path to your PDF file
if len(sys.argv) > 1:
    pdf_file_path = str(sys.argv[1])
else:
    pdf_file_path = './inputForCropping/test1.pdf'
page_count = count_pgs(pdf_file_path)

if page_count is not None:
    print(f"The PDF file '{pdf_file_path}' has {page_count} pages.")
