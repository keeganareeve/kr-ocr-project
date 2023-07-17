'''
Converts a pdf file to a list of lines of text.
To run this script:
    python3 ocr-v3.py {pdf filepath} {outputdir}

(first need to check whether this method works)

pdfdir refers (again) to the full filepath.
'''
import sys
import myfunctions
preproc = myfunctions.preproc()
cleanstr = myfunctions.cleanstr()
ocrcmds = myfunctions.ocrcmds()
eddirs = myfunctions.eddirs()

pdfdir, outputdir = eddirs.twoArgvs()

eddirs.print_arguments()

lines = ocrcmds.pdf2lines(pdfdir)
lines_with_nums = preproc.addnums(lines)

filetype = ".txt"
filename = cleanstr.get_substr(pdfdir, "/")
withoutDotPDF = filename[:-4]  # ".pdf" has length of 4
output_path = withoutDotPDF + "_asLines" + filetype

with open(output_path, 'w') as file:
    for L in lines_with_nums:
        file.write(str(L) + '\n')

    print(f"Saved to filepath: {outputdir}/{output_path}")
