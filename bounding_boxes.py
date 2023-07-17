'''
I'm going to use this script to block out images etc.
'''

# Packages to import
import sys
import pytesseract
import numpy
import cv2  # OpenCV, for identifying "structure"

if len(sys.argv) < 2:
    image_filepath = "temp/page66.png"
else:
    image_filepath = sys.argv[1]

if len(sys.argv) < 3:
    output_file = "temp/index_boundingBoxes.png"
else:
    output_file = sys.argv[2]

# Reading image from filepath
original_image = cv2.imread(image_filepath)

# Preprocessing for Structure (not individual characters)
# grayscale
grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
# cv2.imwrite("temp/index_gray.png", grayscaled_image)

# blur
# reminder: look into these parameters further
blurred_image = cv2.GaussianBlur(grayscaled_image, (7, 7), 0)  # 7-by-7 size
# cv2.imwrite("temp/index_blur.png", blurred_image)

# thresh
# makes a black image with white text
# reminder2: look into these parameters further too
threshold_image = cv2.threshold(
    blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
# cv2.imwrite("temp/index_threshold.png", threshold_image)

# kernels and dilation (convolutions)
# this "kernel" version should not be visible
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
# cv2.imwrite("temp/index_kernel.png", kernel)
after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)
# cv2.imwrite("temp/dilated.png", after_convolutions)

# Making the bounding boxes themselves now that we have the structure more clear
contours = cv2.findContours(
    after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# the number of contours you're looking for should be the number that len(contours should end up with)
contours = contours[0] if len(contours) == 2 else contours[1]

# now, left-to-right or top-to-bottom? EDIT: not sure if it makes a difference
# contours = sorted(contours, key=lambda x: cv2.boundingRect(x)
#                 [0])
contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

# Adding conditions to the rectangles made
for contour in contours:
    xValue, yValue, width, height = cv2.boundingRect(contour)
    # in pixels
    if not height > 200:  # and width > 35
        # cv2.rectangle(original_image, (xValue, yValue),
        #              (xValue+width, yValue+height), (36, 255, 12), 2)
        # if xValue > 100 and yValue > 100:
        cv2.rectangle(original_image, (xValue, yValue),
                      (xValue+width, yValue+height), (0, 0, 255), 2)

# Output
cv2.imwrite(output_file, original_image)
