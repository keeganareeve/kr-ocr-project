# Packages to import
import sys
import numpy as np
import cv2  # OpenCV, for identifying "structure"
import pytesseract

''''
# Checking version of OpenCV
print(f"Version of cv2 package: {cv2.__version__}")
'''

'''
Setting arguments.
'''
image_filepath = sys.argv[1]
output_file = "temp/boundingBoxes.png"

x_min_distance = 170
y_min_distance = 150

'''
Preprocessing.
'''
original_image = cv2.imread(image_filepath)
image_copy = cv2.imread(image_filepath)
x_length, y_length, z_length = original_image.shape

grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(grayscaled_image, (7, 7), 0)
threshold_image = cv2.threshold(
    blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)

# OpenCV version 4.8.0. FindContours() returns 2 things.
contours, hierarchy = cv2.findContours(
    after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])


'''
Getting the contours we're interested in.
'''
contours_away_from_margins = []
for pair in zip(contours, hierarchy):
    curr_contour = pair[0]
    curr_hierarchy = pair[1]

    xValue, yValue, width, height = cv2.boundingRect(curr_contour)

    if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
        contours_away_from_margins.append(curr_contour)

'''
Now that we have the contours, get box edges, filter out boxes with area of 30,000 pixels or more, start merging boxes, and put rectangles on image_copy.
'''
# functions


# tuplify
def tup(point):
    return (point[0], point[1])

# returns true if the two boxes overlap


def overlap(source, target):
    # unpack points
    tl1, br1 = source
    tl2, br2 = target

    # checks
    if (tl1[0] >= br2[0] or tl2[0] >= br1[0]):
        return False
    if (tl1[1] >= br2[1] or tl2[1] >= br1[1]):
        return False
    return True

# returns all overlapping boxes


def getAllOverlaps(boxes, bounds, index):
    overlaps = []
    for a in range(len(boxes)):
        if a != index:
            if overlap(bounds, boxes[a]):
                overlaps.append(a)
    return overlaps


def medianCanny(img, thresh1, thresh2):
    median = np.median(img)
    img = cv2.Canny(img, int(thresh1 * median), int(thresh2 * median))
    return img


# go through the contours and save the box edges
boxes = []  # each element is [[top-left], [bottom-right]]
hierarchy = hierarchy[0]
for pair in zip(contours_away_from_margins, hierarchy):
    curr_contour = pair[0]
    curr_hierarchy = pair[1]

    x, y, w, h = cv2.boundingRect(curr_contour)

    if curr_hierarchy[3] < 0:
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 1)
        boxes.append([[x, y], [x+w, y+h]])
cv2.imwrite("temp/image.png", image_copy)  # testing this step
print(f"Saved image with box edges to temp/image_copy.png.")


# filter out excessively large boxes
filtered = []
max_area = 30000
for box in boxes:
    w = box[1][0] - box[0][0]
    h = box[1][1] - box[0][1]
    if w*h < max_area:
        filtered.append(box)
boxes = filtered

# go through the boxes and start merging
merge_margin = 15

# this is gonna take a long time
finished = False
highlight = [[0, 0], [1, 1]]
points = [[[0, 0]]]
while not finished:
    # set end con
    finished = True

    # check progress
    print("Len Boxes: " + str(len(boxes)))

    # draw boxes # comment this section out to run faster
    copy = np.copy(original_image)
    for box in boxes:
        cv2.rectangle(copy, tup(box[0]), tup(box[1]), (0, 200, 0), 1)
    cv2.rectangle(copy, tup(highlight[0]), tup(highlight[1]), (0, 0, 255), 2)
    for point in points:
        point = point[0]
        cv2.circle(copy, tup(point), 4, (255, 0, 0), -1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # loop through boxes
    index = len(boxes) - 1
    while index >= 0:
        # grab current box
        curr = boxes[index]

        # add margin
        tl = curr[0][:]
        br = curr[1][:]
        tl[0] -= merge_margin
        tl[1] -= merge_margin
        br[0] += merge_margin
        br[1] += merge_margin

        # get matching boxes
        overlaps = getAllOverlaps(boxes, [tl, br], index)

        # check if empty
        if len(overlaps) > 0:
            # combine boxes
            # convert to a contour
            con = []
            overlaps.append(index)
            for ind in overlaps:
                tl, br = boxes[ind]
                con.append([tl])
                con.append([br])
            con = np.array(con)

            # get bounding rect
            x, y, w, h = cv2.boundingRect(con)

            # stop growing
            w -= 1
            h -= 1
            merged = [[x, y], [x+w, y+h]]

            # highlights
            highlight = merged[:]
            points = con

            # remove boxes from list
            overlaps.sort(reverse=True)
            for ind in overlaps:
                del boxes[ind]
            boxes.append(merged)

            # set flag
            finished = False
            break

        # increment
        index -= 1


'''
For testing parameters from this script, if necessary.
'''


def testParameters(output_file, ctrs, original_image=original_image):
    for c in ctrs:
        xValue, yValue, width, height = cv2.boundingRect(c)

        # if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
        cv2.rectangle(original_image, (xValue, yValue),
                      (xValue+width, yValue+height), (0, 255, 0), 2)
    cv2.imwrite(output_file, original_image)
    print(f"Wrote image to {output_file}.")


testParameters(output_file, contours_away_from_margins)  # _away_from_margins)


'''
Cropping contours from image and saving as images.
'''


def getContours(image, ctrs):
    imageList = []
    for c in ctrs:
        xValue, yValue, width, height = cv2.boundingRect(c)
        # If point starts at top right, it should be '-' instead of '+'
        imageList.append(image[yValue:yValue + height, xValue:xValue + width])
    return imageList


def saveImages(imageList, directory):
    i = 0
    for img in imageList:
        # if i < 20:
        output_filename = f"{directory}croppedImage{i}.png"
        cv2.imwrite(output_filename, img)
        print(f"Wrote {output_filename} to {directory} directory.")
        i += 1
    return None


def saveText(string_list, filepath):
    try:
        with open(filepath, 'w') as file:
            for item in string_list:
                file.write(item + '\n')
        print("List of strings has been successfully saved to", filepath)
    except IOError as e:
        print("Error:", e)


'''
croppedImages = getContours(image_copy, contours_away_from_margins)
'''

'''
# saveImages(croppedImages, "temp/cropped_images/")

croppedText = []
for i, cropped_section in enumerate(croppedImages):
    croppedText.append(pytesseract.image_to_string(cropped_section))
# saveText(croppedText, "temp/croppedText.txt")
'''
