import cv2
#set up camera calibration
#get camera
# Get the first available camera
# Create a VideoCapture object to access the camera
# Create a VideoCapture object to access the camera
camera = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not camera.isOpened():
    print("Failed to open camera")
    exit()

# Define the size of the chessboard
chessboard_size = (8, 8)

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()

    # If the frame was not read successfully, exit the loop
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    _, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx_polygon = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Draw the contour and approximated polygon on the frame
    cv2.drawContours(frame, [approx_polygon], 0, (0, 255, 0), 3)


    # Display the resulting frame
    cv2.imshow('Camera', frame)


#detect board 

#create the boxes for each position

#Highlight empty boxes red

#Highlight boxes that contain a piece  green

#put positions into 2d  array


    # Check for the 'q' key to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows() 