'''
This script puts boxes around text given an image (excluding text found near the margins).

image_filepath can be an image file of a page from a pdf file.
output_file should be the output directory.

This script produces images of each individual cropped word (often will crop smaller segments than words) in the format cropped_wordN.png (where N stands for a number starting with 0) and an image containing the outermost points of these words' bounding boxes, as cropped_words.png.


To run this script:
    python3 bounding_boxes-v2.py image_filepath output_directory

(The arguments OUTPUT_FILE, X_MIN, and Y_MIN, are optional, and the OUTPUT_FILE argument can be anywhere after the image_filepath and does not even need to be labeled with OUTPUT_FILE= in front of it.)
'''

# Packages to import
import sys
import cv2  # OpenCV, for identifying "structure"

print(sys.argv)

image_filepath = str(sys.argv[1])
output_directory = str(sys.argv[2])

x_min_distance = 130
y_min_distance = 150

# Printing arguments
print("------------------------------------")
print(f"Image filepath defined as {image_filepath}")
print(f"X_MIN distance defined as {x_min_distance}")
print(f"Y_MIN distance defined as {y_min_distance}")
# print(f"OUTPUT_FILE defined as {output_file}")
print("------------------------------------")

# Reading image from filepath
original_image = cv2.imread(image_filepath)
x_length, y_length, z_length = original_image.shape
# x_length = original_image.shape[0]
# y_length = original_image.shape[1]
print(f"Length of x-axis on the original image: {x_length}")
print(f"Length of y-axis on the original image: {y_length}")
print(f"Length of z-axis(?) on the original image: {z_length}")

# Cropping doesn't seem to help with the purpose we have in mind, but it does work here if you want to test it:
# cropped_image = original_image[min_distance:x_length -
# min_distance, min_distance:y_length-min_distance]
# cv2.imwrite("CroppedImage.png", cropped_image)

# Preprocessing for Structure (not individual characters)
# grayscale
# grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
grayscaled_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("temp/index_gray.png", grayscaled_image)

# blur
# reminder: look into these parameters further
blurred_image = cv2.GaussianBlur(grayscaled_image, (7, 7), 0)  # 7-by-7 size
cv2.imwrite("temp/index_blur.png", blurred_image)

# thresh
# makes a black image with white text
# reminder2: look into these parameters further too
threshold_image = cv2.threshold(
    blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("temp/index_threshold.png", threshold_image)

# kernels and dilation (convolutions)
# this "kernel" version should not be visible
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
# cv2.imwrite("temp/index_kernel.png", kernel)
after_convolutions = cv2.dilate(threshold_image, kernel, iterations=1)
cv2.imwrite("temp/dilated.png", after_convolutions)

# Making the bounding boxes themselves now that we have the structure more clear
contours = cv2.findContours(
    after_convolutions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# the number of contours you're looking for should be the number that len(contours should end up with)
contours = contours[0] if len(contours) == 2 else contours[1]
contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

image_copy = cv2.imread(image_filepath)
i = 0
# Adding conditions to the rectangles made
for contour in contours:
    xValue, yValue, width, height = cv2.boundingRect(contour)

    if height < 200 and xValue in range(y_min_distance, x_length - x_min_distance) and yValue in range(y_min_distance, y_length-y_min_distance):
        cv2.rectangle(original_image, (xValue, yValue),
                      (xValue+width, yValue+height), (0, 255, 0), 2)
        # Output (as an image for every cropped word)
        cv2.imwrite(
            f"{output_directory}cropped_word{i}.png", image_copy[yValue:yValue+height, xValue:xValue+width])
        print(f"Wrote image to {output_directory}cropped_word{i}.png.")
        i += 1
# Output (as one image withbounding boxes shown)
cv2.imwrite(f"{output_directory}cropped_words.png", original_image)
print(f"Wrote image to {output_directory}cropped_words.png")
