# kr-ocr-project

## Copies of Introductory Comments from Other Files ## 
### pdf2txt.py ###
Converts a pdf file to a text file.
To run this script:
    python3 pdf2txt.py [rmpat=]{TRUE/FALSE} {pdf filepath} {outputdir}

 The `rmpat=TRUE' argument condition will delete sequences in the patterns 01 * word or word * 01. This pattern can be changed by editing the pattern in the rmpat() function in the cleanstr class in myfunctions.py.

### pdf2parasAndSents.py ###
Converts a pdf file to a list of paragraphs and a list of sentences.
Brackets signify that the sequence of characters (variable names) are optional.

Can run in virtual environment after running this command:
    {sudo} sh getdependencies.sh
    (this file gets the python packages from requirements.txt)

To run this script: (excluding the brackets)
    python3 pdf2parasAndSents.py [rmpat=]{TRUE/FALSE} [pdfdir=]{pdf filepath} [outputdir]={outputdir}
(make sure to use make the format 
    `python3 pdf2parasAndSents.py rmpat=FALSE pdfdir=/home/... outputdir=/home/.../'
      without spaces in any other positions and avoiding use of tildes)

The `rmpat=TRUE' argument condition will delete sequences in the patterns 01 * word or word * 01. This pattern can be changed by editing the pattern in the rmpat() function in the cleanstr class in myfunctions.py.

### pdf2lines.py ###
Converts a pdf file to a list of lines of text.
To run this script:
    python3 pdf2lines.py {pdf filepath} {outputdir}

pdfdir refers (again) to the full filepath.

### bounding_boxes.py ###
This script puts boxes around text given an image.

image_filepath can be an image file of a page from a pdf file.
output_file should be an image file or filepath.

To run this script: (excluding the brackets)
  `python3 bounding_boxes-v2.py {image_filepath} {outputfile}'
  (default values for these two arguments can be set in the script below)

### bounding_boxes-v2.py ###
This script puts boxes around text given an image, excluding the margins of the image.
Modified version of bounding_boxes.py with this added condition.

image_filepath can be an image file of a page from a pdf file.
output_file should be an image file or filepath.

To run this script: (excluding the brackets)
  `python3 bounding_boxes-v2.py {image_filepath} {outputfile}'
  (default values for these two arguments can be set in the script below)