import cv2

import numpy as np

def apply_filter(image, filter_type):

    """Apply the selected color filter or edge detection."""

    # Create a copy of the image to avoid modifying the original

    filtered_image = image.copy()

    if filter_type == "red_tint":

        filtered_image[:, :, 1] = 0  # Green channel to 0

        filtered_image[:, :, 0] = 0  # Blue channel to 0

    elif filter_type == "green_tint":

        filtered_image[:, :, 0] = 0  # Blue channel to 0

        filtered_image[:, :, 2] = 0  # Red channel to 0

    elif filter_type == "blue_tint":

        filtered_image[:, :, 1] = 0  # Green channel to 0

        filtered_image[:, :, 2] = 0  # Red channel to 0

    elif filter_type == "sobel":

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)

        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

        combined_sobel = cv2.bitwise_or(sobelx.astype('uint8'), sobely.astype('uint8'))

        filtered_image = cv2.cvtColor(combined_sobel, cv2.COLOR_GRAY2BGR)

    elif filter_type == "canny":

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray_image, 100, 200)

        filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif filter_type=="cartoon":
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=cv2.medianBlur(gray,5)
        edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color=cv2.bilateralFilter(image,9,300,300)
        filtered_image=cv2.bitwise_and(color,color,mask=edges)

    return filtered_image

# Load the imageq

image_path = 'example.jpg'  # Provide your image path

image = cv2.imread(image_path)

if image is None:

    print("Error: Image not found!")

else:

    filter_type = "original"  # Default filter type

    print("Press the following keys to apply filters:")

    print("r - Red Tint")

    print("g - Green Tint")

    print("b - Blue Tint")

    print("s - Sobel Edge Detection")

    print("c - Canny Edge Detection")

    print("t - Median Blur(Cartoon)")

    print("q - Quit")

    while True:

        # Apply the selected filter

        filtered_image = apply_filter(image, filter_type)

        # Display the filtered image
        resized_image=cv2.resize(filtered_image, (600,500), interpolation=cv2.INTER_AREA)

        cv2.imshow("Filtered Image", resized_image)

        # Wait for key press

        key = cv2.waitKey(0) & 0xFF

        # Map key presses to filters

        if key == ord('r'):

            filter_type = "red_tint"

        elif key == ord('g'):

            filter_type = "green_tint"

        elif key == ord('b'):

            filter_type = "blue_tint"

        elif key == ord('s'):

            filter_type = "sobel"

        elif key == ord('c'):

            filter_type = "canny"
        
        elif key == ord('t'):

            filter_type = "cartoon"

        elif key == ord('q'):

            print("Exiting...")

            break

        else:

            print("Invalid key! Please use 'r', 'g', 'b', 's', 'c', or 'q'.")

    cv2.destroyAllWindows()