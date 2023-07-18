'''
Converts a pdf file to a list of lines of text.
To run this script:
    python3 pdf2lines.py {pdf filepath} {outputdir}

pdfdir refers (again) to the full filepath.
'''
import sys
import myfunctions
preproc = myfunctions.preproc()
cleanstr = myfunctions.cleanstr()
ocrcmds = myfunctions.ocrcmds()
eddirs = myfunctions.eddirs()

pdfdir, outputdir = eddirs.twoArgvs()

print(f"\npdfdir set as {pdfdir}")
print(f"outputdir set as {outputdir}\n")

eddirs.print_arguments()

lines = ocrcmds.pdf2lines(pdfdir)
lines_with_nums = preproc.addnums(lines)

filetype = ".txt"
filename = cleanstr.get_substr(pdfdir, "/")
# print(f"Filename (without directory or filetype): {filename}")
withoutDotPDF = filename[:-4]  # ".pdf" has length of 4
# print(f"WithoutDotPDF (without directory): {withoutDotPDF}")
# print(f"outputdir: {outputdir}")
output_path = outputdir + withoutDotPDF + "_asLines" + filetype

with open(output_path, 'w') as file:
    for L in lines_with_nums:
        file.write(str(L) + '\n')

    print(f"Saved to filepath: {output_path}")
