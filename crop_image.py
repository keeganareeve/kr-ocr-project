'''
To run:
    python3 crop_image.py <image_filepath> <output_filepath>
            sys.argv[0]   sys.argv[1]       sys.argv[2]
'''

# STEP 1
# Possible issue with pytesseract python package: https://stackoverflow.com/questions/33401767/importerror-no-module-named-pytesseract

# Path to your image file
import sys
import os
import numpy as np
import cv2

# STEP 2
# '/content/gdrive/MyDrive/ImageFiles/inputForCropping/page66.png'
image_filepath = str(sys.argv[1])
image_name = str(os.path.basename(image_filepath))
output_filepath = str(sys.argv[2])

original_image = cv2.imread(image_filepath)

# STEP 2
image_path = image_filepath
original_image = cv2.imread(image_path)

x_min_distance = 130
y_min_distance = 150

original_image = cv2.imread(image_path)
x_length, y_length, z_length = original_image.shape

# STEP 3
grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(grayscaled_image, (7, 7), 0)  # 7-by-7 size
threshold_image = cv2.threshold(
    blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)
contours = cv2.findContours(
    after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
# cv2.rectangle(
#    image_copy, (x, y), (x+w, y+h), (0, 0, 255), 1)

# STEP 7: Cropping it
cropped_image = image_copy[y:y+h, x:x+w]
cv2.imwrite(output_filepath, cropped_image)
print(f"Saved {output_filepath}")
