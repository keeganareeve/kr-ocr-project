'''
Modified script from https://github.com/Breta01/handwriting-ocr/blob/master/src/ocr/words.py.

So far, this script only produces bounding boxes on the first half of a png on some images, and on others, it finds no text at all. But it does group together the bounding boxes as it's supposed to.
-------------------------------------------------------------------------------
May change substantially if I find a better method to do this.

To run script:
    python3 group_bounding_boxes.py

'''

from imutils import contours
import imutils
import numpy as np
import cv2

image_filepath = "temp/page67.png"
output_filepath = "temp/index_boundingBoxes.png"

# Variables to tweak
x_min_distance = 130
y_min_distance = 150


def union(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return [x, y, w, h]


def _intersect(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    # in original code :  if w<0 or h<0:
    if h < 0:
        return False
    return True


def _group_rectangles(rec):
    """
    Union intersecting rectangles.
    Argvs:
        rec - list of rectangles in form [x, y, w, h]
    Return:
        list of grouped rectangles 
    """
    tested = [False for i in range(len(rec))]
    final = []
    i = 0
    while i < len(rec):
        if not tested[i]:
            j = i+1
            while j < len(rec):
                if not tested[j] and _intersect(rec[i], rec[j]):
                    rec[i] = union(rec[i], rec[j])
                    tested[j] = True
                    j = i
                j += 1
            xValue = rec[i][0]
            yValue = rec[i][1]
            width = rec[i][2]  # won't be used at all
            height = rec[i][3]
            # the if-statement excludes bounding boxes at margins
            if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length - y_min_distance):
                final += [rec[i]]
                print(f"Added {rec[i]}")
        i += 1

    return final


img = cv2.imread(image_filepath)
image_copy = cv2.imread(image_filepath)
x_length, y_length, z_length = img.shape

grayscaled_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(grayscaled_image, (7, 7), 0)
threshold_image = cv2.threshold(
    blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)

# threshold image
ret, threshed_img = cv2.threshold(
    grayscaled_image, 80, 255, cv2.THRESH_BINARY_INV)

# find contours and get the external one

# edged = imutils.auto_canny(threshed_img)

ctrz = cv2.findContours(after_convolutions, cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

'''
# getting box edges with specific contours
contours_away_from_margins = []
for pair in zip(ctrz, hierarchy):
    curr_contour = pair[0]
    curr_edge = pair[1]

    xValue, yValue, width, height = cv2.boundingRect(curr_contour)

    if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
        contours_away_from_margins.append(tuple(curr_contour, curr_edge))
'''

'''
contours_away_from_margins = []
for curr_contour in ctrz_copy:

    xValue, yValue, width, height = cv2.boundingRect(curr_contour)

    if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
        contours_away_from_margins.append(curr_contour)
final_contours = contours_away_from_margins
'''

cnts = imutils.grab_contours(ctrz)
(cnts, boundingBoxes) = imutils.contours.sort_contours(
    cnts, method="left-to-right")
boundingBoxes = list(boundingBoxes)
boundingBoxes = _group_rectangles(boundingBoxes)

for (x, y, w, h) in boundingBoxes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imwrite(output_filepath, img)
