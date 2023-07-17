'''
Converts a pdf file to a text file.
To run this script:
    python3 ocr-v1.py rmpat={TRUE/FALSE} {pdf filepath} {outputdir}
'''
import sys

import PyPDF2
from pdf2image import convert_from_path

import myfunctions
cleanstr = myfunctions.cleanstr()
ocrcmds = myfunctions.ocrcmds()
preproc = myfunctions.preproc()
eddirs = myfunctions.eddirs()

pdfdir, outputdir = eddirs.threeArgvs()

print(f"\npdfdir set as {pdfdir}")
print(f"outputdir set as {outputdir}\n")


filetype = ".txt"
filename = cleanstr.get_substr(pdfdir, "/")
withoutDotPDF = filename[:-4]  # ".pdf" has length of 4
output_file = withoutDotPDF + "ocrd" + filetype

print(f"Output file will be {output_file}")


pdf_file = pdfdir
start_page = 1
num_pages_per_group = 20


# Option to remove page numbers
optObj = cleanstr.set_rm_opt()

# Convert the PDF in groups
# Returns string
total_pages = len(PyPDF2.PdfReader(open(pdf_file, "rb")).pages)
all_groups = ""
group_num = 0
for group_start in range(start_page, total_pages, num_pages_per_group):
    group_text = ocrcmds.pdf2txt(pdf_file, group_start, num_pages_per_group)

    group_num += 1
    print("Group number "+str(group_num)+".")

    if optObj == "2":
        group_text = cleanstr.rmpat(group_text)
        print("Removed page numbers in group number " + str(group_num)+".")

    all_groups += group_text
all_groups_string = all_groups[:]

fulltxt = all_groups_string
fulltxt = fulltxt.replace('|', 'I')

# Save as text file
cleanstr.str2txt(fulltxt, outputdir, filename, output_file)
