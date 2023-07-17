'''
Default pdf filepath and output directory can be edited in the __init__() function of the eddirs class.
'''

# import PyPDF2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

import sys
import re
import random

import os
import shutil

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np  # linear algebra


class eddirs:
    def __init__(self):

        self.pdf_filepath = ""
        self.output_dir = ""

        pass

    def print_arguments(self):
        print("Your number of arguments: " + str(len(sys.argv)))
        for item in sys.argv:
            print(item)

    def threeArgvs(self):
        # python3 {script name} rmpat={TRUE/FALSE} {pdf filepath} {outputdir}
        # for pdf2txt.py & pdf2parasAndSents.py
        # (formerly, ocr-v1.py & ocr-v2.py)

        if len(sys.argv) <= 2:
            # includes .pdf
            pdfdir = self.pdf_filepath
            outputdir = self.output_dir  # only the dir itself: NO .pdf

        elif len(sys.argv) == 3:
            if str(sys.argv[2])[:len("pdfdir=")] == "pdfdir=":
                pdfdir = (str(sys.argv[2]))[len("pdfdir="):]
            else:
                pdfdir = str(sys.argv[2])

            outputdir = self.output_dir

        elif len(sys.argv) == 4:
            if str(sys.argv[2])[:len("pdfdir=")] == "pdfdir=":
                pdfdir = (str(sys.argv[2]))[len("pdfdir="):]
            else:
                pdfdir = str(sys.argv[2])

            if str(sys.argv[3])[:len("outputdir=")] == "outputdir=":
                outputdir = (str(sys.argv[3]))[len("outputdir="):]
            else:
                outputdir = str(sys.argv[3])

        return pdfdir, outputdir

    def twoArgvs(self):
        # python3 {script name} {pdf filepath} {outputdir}
        # for pdf2lines.py
        # (formerly, ocr-v3.py)

        if len(sys.argv) == 1:
            pdfdir = self.pdf_filepath
            output_path = self.output_dir
        elif len(sys.argv) == 2:
            # Recall that sys.argv[0] is the script filename
            pdfdir = sys.argv[1]
            output_path = self.output_dir
        elif len(sys.argv) == 3:
            pdfdir = sys.argv[1]
            output_path = sys.argv[2]

        return pdfdir, output_path

    def cpPdfs(self, source_dirs, dest_dirs, sequences):

        for dest_dir in dest_dirs:
            os.makedirs(dest_dir, exist_ok=True)

            for source_dir in source_dirs:
                for filename in os.listdir(source_dir):

                    if filename.lower().endswith('.pdf'):
                        file_name_without_extension = os.path.splitext(filename)[
                            0]
                        for sequence in sequences:

                            num_from_end = -1*(len(sequence))
                            if sequence == file_name_without_extension[num_from_end:]:
                                source_path = os.path.join(
                                    source_dir, filename)
                                dest_path = os.path.join(
                                    dest_dir, filename)
                                shutil.copy2(source_path, dest_path)
                                print(
                                    f"Copied {filename} from {source_dir}\n\tinto {dest_dir}\n")

    def subdirs(self, directory):
        subdirs = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                subdirs.append(item_path)
        return subdirs

    def rec_subdirs(self, dir):
        # Recursive version of the above function
        subdirs = []
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)
            if os.path.isdir(item_path):
                subdirs.append(item_path)
                subdirs.extend(self.rec_subdirs(item_path))
        return subdirs


class cleanstr:
    def __init__(self):

        self.obj = "0"

        pass

    def set_rm_opt(self):
        # Option to remove page numbers
        if len(sys.argv) < 2:
            # result = all_groups_string
            print("Option set: will save original text.\n")
            self.obj = "1"
        elif str(sys.argv[1]) in ["rmpat=TRUE", "TRUE", "1", "rmpat=1", "T"]:
            # result = cleanstr.rmpat(all_groups_string)
            print("Option set: will remove page number (string patterns).\n")
            self.obj = "2"
        elif str(sys.argv[1]) in ["rmpat=FALSE", "FALSE", "0", "rmpat=0", "F"]:
            # result = all_groups_string
            print("Option set: will save original text.\n")
            self.obj = "3"
        else:
            print(
                "ERROR: self.obj not set properly!\nself.obj improperly remains at 0.\n")
        return self.obj

    def get_substr(self, string, char="/"):
        # Find the last occurrence of "/"
        last_char_index = string.rfind(char)
        if last_char_index != -1:
            return string[last_char_index + 1:]
        return string

    def rmpat(self, string):
        pattern = r"\n(\d+\s\*\s(\w+\s)+)\n|\n((\w+\s)+\*\s\d+)\n"
        cleaned_string = re.sub(pattern, "", string)
        return cleaned_string

    def str2txt(self, text, directory, filename, output_file):

        if directory[-1] == "/":  # If the directory name has a slash at the end
            filepath = f"{directory}{filename}"  # Omits adding extra slash
        elif directory[-1] != "/":  # If the directory doesn't have a slash at the end
            filepath = f"{directory}/{filename}"  # Adds in slash

        if directory[-1] == "/":  # If the directory name has a slash at the end
            # Omits adding extra slash
            output_filepath = f"{directory}{output_file}"
        elif directory[-1] != "/":  # If the directory doesn't have a slash at the end
            output_filepath = f"{directory}/{output_file}"  # Adds in slash

        with open(output_filepath, "w") as file:
            file.write(text)

        if self.obj in ["1", "3"]:
            print(
                f"\n\n---Original string saved as text file: {output_filepath}.---\n")
        elif self.obj == "0":
            print(
                f"\n\n---String saved as text file: {output_filepath}.--\n\t---Further options not set in setopt()---\n")
        elif self.obj == "2":
            print(
                f"\n\n---Modified string saved to text file: {output_filepath}---\n\t---Page numbers removed---\n")

    def parasAndSents2txt(self, directory, filename1, filename2, paras, sents):

        if directory[-1] == "/":  # If the directory name has a slash at the end
            filepath1 = f"{directory}{filename1}"  # Omits adding extra slash
        elif directory[-1] != "/":  # If the directory doesn't have a slash at the end
            filepath1 = f"{directory}/{filename1}"  # Adds in slash

        if directory[-1] == "/":  # If the directory name has a slash at the end
            filepath2 = f"{directory}{filename2}"  # Omits adding extra slash
        elif directory[-1] != "/":  # If the directory doesn't have a slash at the end
            filepath2 = f"{directory}/{filename2}"  # Adds in slash

        with open(filepath1, 'w') as file:
            for item in paras:
                file.write(str(item) + '\n')

            print("Saved to filepath: "+filepath1)

        with open(filepath2, 'w') as file:
            for item in sents:
                file.write(str(item) + '\n')
            print("Saved to filepath: "+filepath2)

        pass

    def threeLongRange(self, inputlist):
        ending_number = random.randint(3, len(inputlist))
        range_of_three = inputlist[ending_number-3:ending_number]
        return range_of_three


class ocrcmds:
    def __init__(self):
        pass

    def pdf2txt(self, pdf_path, start_page, num_pages):
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)

            # Determines end page for group
            num_total_pages = len(pdf_reader.pages)
            end_page = min(start_page + num_pages, num_total_pages)

            # Extracts pages as images
            images = convert_from_path(
                pdf_path, first_page=start_page+1, last_page=end_page)

            text_group = []
            for page_num, image in enumerate(images):
                image_text = pytesseract.image_to_string(image)
                text_group.append(image_text)

            # Concatenate the text from all pages in the group
            group_text = "\n".join(text_group)
            return group_text

    def img2lines(self, image_filepath):

        image = Image.open(image_filepath)
        gray = image.convert('L')  # grayscale

        # Grayscale to binary, finds pixels (points) and creates shapes out of the black pixels
        binary = gray.point(lambda x: 0 if x < 127 else 255, '1')

        # OCR on binary image
        result = pytesseract.image_to_string(binary)
        lines = result.split('\n')

        # Removes empty lines
        lines = [line for line in lines if line.strip()]

        return lines

    def pdf2lines(self, pdf_path, start_page=0, num_pages=20):
        pdf_reader = PdfReader(pdf_path)

        # Determines end page for group
        num_total_pages = len(pdf_reader.pages)
        end_page = min(start_page + num_pages, num_total_pages)

        # Extracts pages as images
        images = convert_from_path(
            pdf_path, first_page=start_page+1, last_page=end_page)

        lines = []
        for image in images:
            # Opens image
            gray = image.convert('L')  # grayscale

            # grayscale to binary, finds pixels (points) and creates shapes out of the black pixels
            binary = gray.point(lambda x: 0 if x < 127 else 255, '1')

            # Performs OCR on binary image
            result = pytesseract.image_to_string(binary)
            lines.extend(result.split('\n'))

        # Removes empty lines
        lines = [line for line in lines if line.strip()]

        return lines


class preproc:
    def __init__(self):

        pass

    def str2paras(self, text):
        # Split the text into paragraphs based on the delimiter
        # Use '\r\n\r\n' if that's the delimiter you want to split on
        paragraphs = text.split("\n\n")

        # Remove leading and trailing whitespace from each paragraph
        paragraphs = [paragraph.strip() for paragraph in paragraphs]

        return paragraphs

    def rmVoidParas(self, paragraphs):
        filtered_paragraphs = []

        for paragraph in paragraphs:
            if re.search(r'\w', paragraph):
                filtered_paragraphs.append(paragraph)

        return filtered_paragraphs

    def combParas(self, paragraphs):
        # Combines paragraphs from different pages if the sentence in the first paragraph is incomplete.
        combined_paragraphs = []
        current_paragraph = paragraphs[0]

        for i in range(1, len(paragraphs)):
            if not re.search(r'[.!?]\s*$', current_paragraph):
                current_paragraph += " " + paragraphs[i]
            else:
                combined_paragraphs.append(current_paragraph)
                current_paragraph = paragraphs[i]

        combined_paragraphs.append(current_paragraph)

        return combined_paragraphs

    def extrSents(self, text):

        sents = re.split(r'\.\s*', text)
        sents = [sent.strip() for sent in sents if sent.strip()]

        return sents

    def addnums(self, strings_as_list):
        return [f"#&[{i+1}.]&# {string}" for i, string in enumerate(strings_as_list)]

    def rm_newline(self, strings):
        return [s.replace('\n', '') for s in strings]
