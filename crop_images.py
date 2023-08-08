'''
To run:
    python3 crop_images.py <input_directory> <output_directory>

The argument output_directory is optional: if it is not present it is assumed to be the same as the input_directory.

If both input and output directories are ommitted, they will be assumed to be the current directory both.

'''

import sys
import os
import numpy as np
import cv2


if len(sys.argv) > 1:
    input_directory = str(sys.argv[1])
else:
    input_directory = "./"


def print_top_directory_files(description, directory_path):
    try:
        filelist = []

        # List all entries in the directory
        entries = os.listdir(directory_path)

        # Filter and print only files in the top directory
        print(description)
        for entry in entries:
            entry_path = os.path.join(directory_path, entry)
            if os.path.isfile(entry_path):
                if entry[-4:] == ".png":
                    # print(entry)
                    filelist.append(entry)
        print(filelist)

        return filelist

    except OSError as e:
        print(f"Error: {e}")


# STEP 1
# Gets files from input directory
filelist = print_top_directory_files(
    'Files found in input image directory:', input_directory)

if len(filelist) == 0:
    curr_dir = str(os.getcwd())
    print(f"The current directory is {curr_dir}/")
    print("No png image files found in input directory.\nTry changing the directory.\n\n")
    print("---------------------------------------------")
    print('''
To run this script:
    python3 crop_images.py <input_directory> <output_directory>
          ''')
    print("---------------------------------------------")
    print("End.")

if len(sys.argv) < 3:
    image_directory = input_directory
elif len(sys.argv) == 3:
    image_directory = str(sys.argv[2])
    print(f"Set image directory as {image_directory}")
else:
    print("Error occurred. Check script arguments.")

i = 0
for file in filelist:
    i += 1
    # print(f"Image directory: {image_directory}")
    # STEP 2
    image_path = input_directory+file
    original_image = cv2.imread(image_path)

    x_min_distance = 130
    y_min_distance = 150

    original_image = cv2.imread(image_path)
    x_length, y_length, z_length = original_image.shape

    # STEP 3
    grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(
        grayscaled_image, (7, 7), 0)  # 7-by-7 size
    threshold_image = cv2.threshold(
        blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
    after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)
    contours = cv2.findContours(
        after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print("Reached end of Step 3!")

    # STEP 4
    # Converting the format of the contours
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

    # STEP 5
    # this may be a new idea for a procedure to use for finding lines of images instead of making only one:
    # https://stackoverflow.com/questions/64002869/how-to-combine-bounding-boxes-in-opencv-python

    rectTuples = []
    for contour in contours:
        xValue, yValue, width, height = cv2.boundingRect(contour)

        if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
            # cv2.rectangle(original_image, (xValue, yValue),
            # (xValue+width, yValue+height), (0, 0, 255), 2)

            rectTuples.append((xValue, yValue, width, height))

    # STEP 6
    # MERGE BOXES
    # Then, the same code as in group_bounding_boxes.py in order to merge boxes and crop.
    arr = []
    for x, y, w, h in rectTuples:
        arr.append((x, y))
        if x+w > x_length-x_min_distance:  # do these if-statements make any different?
            if y+h > y_length-y_min_distance:
                if y-h > y_min_distance:
                    # increases x coord by width of box, and y coord to height of box in order to combine all boxes
                    arr.append((x+w, y+h))

    x, y, w, h = cv2.boundingRect(np.asarray(arr))
    image_copy = cv2.imread(image_path)
    cv2.rectangle(
        image_copy, (x, y), (x+w, y+h), (0, 255, 0), 1)

    # STEP 7: Cropping them
    output_filepath = image_directory+'cropped'+file

    cropped_image = image_copy[y:y+h, x:x+w]
    cv2.imwrite(output_filepath, cropped_image)
    print(f"Saved {output_filepath}")

    if i == len(filelist):
        print("End.")
