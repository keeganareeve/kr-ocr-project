'''
(Requires myfunctions.py to run.)

Converts a pdf file to a list of paragraphs and a list of sentences.
Brackets signify that the sequence of characters (variable names) are optional.

Can run in virtual environment after running this command:
    {sudo} sh getdependencies.sh
    (this file gets the python packages from requirements.txt)

To run this script: (excluding the brackets)
    python3 pdf2parasAndSents.py [rmpat=]{TRUE/FALSE} [pdfdir=]{pdf filepath} [outputdir]={outputdir}
(make sure to use make the format 
    `python3 pdf2parasAndSents.py rmpat=FALSE pdfdir=/home/.../ outputdir=/home/.../'
      without spaces in any other positions and avoiding use of tildes)

The `rmpat=TRUE' argument condition will delete sequences in the patterns 01 * word or word * 01. This pattern can be changed by editing the pattern in the rmpat() function in the cleanstr class in myfunctions.py.
'''

import PyPDF2
from pdf2image import convert_from_path

import sys

import myfunctions
cleanstr = myfunctions.cleanstr()
ocrcmds = myfunctions.ocrcmds()
preproc = myfunctions.preproc()
eddirs = myfunctions.eddirs()

pdfdir, outputdir = eddirs.threeArgvs()

print(f"\npdfdir set as {pdfdir}")
print(f"outputdir set as {outputdir}\n")


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

list_of_paras = preproc.str2paras(fulltxt)
list_of_paras = preproc.rmVoidParas(list_of_paras)
comb_paras = preproc.combParas(list_of_paras)
comb_paras = preproc.addnums(comb_paras)
comb_paras = preproc.rm_newline(comb_paras)
print(cleanstr.threeLongRange(comb_paras))

comb_sents = preproc.extrSents(fulltxt)
comb_sents = preproc.addnums(comb_sents)
comb_sents = preproc.rm_newline(comb_sents)
print(cleanstr.threeLongRange(comb_sents))

filetype = ".txt"
filename = cleanstr.get_substr(pdfdir, "/")
withoutDotPDF = filename[:-4]  # ".pdf" has length of 4
filename1 = withoutDotPDF + "_asParas" + filetype
filename2 = withoutDotPDF + "_asSents" + filetype

# Save lists as text files
cleanstr.parasAndSents2txt(
    outputdir, filename1, filename2, comb_paras, comb_sents)
