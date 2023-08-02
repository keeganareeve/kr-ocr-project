# Packages to import
import sys
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
x_min_distance = 130
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
contours = cv2.findContours(
    after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])


'''
Getting the contours we're interested in.
'''
contours_away_from_margins = []
for contour in contours:
    xValue, yValue, width, height = cv2.boundingRect(contour)

    if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length):
        contours_away_from_margins.append(contour)


'''
For testing parameters from this script, if necessary.
'''
output_file = "temp/boundingBoxes.png"


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
Cropping contours from image and saving these contours as images and text.
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


croppedImages = getContours(image_copy, contours_away_from_margins)
saveImages(croppedImages, "temp/cropped_images/")

croppedText = []
for i, cropped_section in enumerate(croppedImages):
    croppedText.append(pytesseract.image_to_string(cropped_section))
saveText(croppedText, "temp/croppedText.txt")
