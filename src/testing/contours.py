import cv2
import numpy as np

# Read the image

cap = cv2.VideoCapture(0)

while True:
            
    ret, image = cap.read()

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale image
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the image to draw the contours on
    contour_image = np.copy(image)

    # Draw contours on the image
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    # Display the original image and the image with contours
    cv2.imshow("Original Image", image)
    cv2.imshow("Image with Contours", contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
