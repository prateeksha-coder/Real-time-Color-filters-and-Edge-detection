#works on webcam feed live 
import cv2
import numpy as np

def apply_filter(image, filter_type):
    """Apply the selected color filter or edge detection."""
    
    filtered_image = image.copy()

    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0  # Green = 0
        filtered_image[:, :, 0] = 0  # Blue = 0

    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0  # Blue = 0
        filtered_image[:, :, 2] = 0  # Red = 0

    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  # Green = 0
        filtered_image[:, :, 2] = 0  # Red = 0

    elif filter_type == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        combined = cv2.bitwise_or(
            np.uint8(np.abs(sobelx)),
            np.uint8(np.abs(sobely))
        )
        filtered_image = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)

    elif filter_type == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif filter_type=="cartoon":
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=cv2.medianBlur(gray,5)
        edges=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
        color=cv2.bilateralFilter(image,9,300,300)
        filtered_image=cv2.bitwise_and(color,color,mask=edges)

    return filtered_image


# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not accessible")
    exit()

filter_type = "original"

print("Press keys to apply filters:")
print("r - Red Tint")
print("g - Green Tint")
print("b - Blue Tint")
print("s - Sobel Edge Detection")
print("c - Canny Edge Detection")
print("t - Median Blur(Cartoon)")
print("q - Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    filtered_frame = apply_filter(frame, filter_type)
    resized_frame = cv2.resize(filtered_frame, (600, 500))

    cv2.imshow("Webcam Filter Feed", resized_frame)

    key = cv2.waitKey(1) & 0xFF

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

cap.release()
cv2.destroyAllWindows()
