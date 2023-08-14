###############################################################################
# This program will compare two images and highlight the differences between
# the two images. This program will be used to compare the current frame to
# the previous frame to determine if there is a change in the frame. If there
# is a change in the frame, the program will then determine if the change is
# due to a piece being moved or if the change is due to a piece being removed
# from the board.
###############################################################################

import cv2
import numpy as np

###############################################################################


def frame_comparison():
    image_path1 = (
        "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess1.png"
    )
    # image_path2 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess1.png"
    image_path2 = (
        "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess2.png"
    )
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    if image1 is None:
        print("Error opening file 1")
        exit()

    if image2 is None:
        print("Error opening file 2")
        exit()

    grey_1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grey_1_resized = cv2.resize(grey_1, (600, 600))

    grey_2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    grey_2_resized = cv2.resize(grey_2, (600, 600))
    diff = cv2.absdiff(grey_1_resized, grey_2_resized)

    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    # Find contours of the changed regions
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Get the bounding boxes of the changed regions
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]

    # Draw rectangles around the changed regions on the images
    for x, y, w, h in bounding_boxes:
        cv2.rectangle(diff, (x, y), (x + w, y + h), (255, 255, 255), 2)

    # Display the images with the changed regions highlighted
    cv2.imshow("Image 1", grey_1_resized)
    cv2.imshow("Image 2", grey_2_resized)
    cv2.imshow("Difference", diff)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # is_diff = np.all((diff == 0) | (diff == 255))

    # if not is_diff:
    #     cv2.imshow("Difference", diff)
    # else:
    #     print ("No difference in images")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows

    return


###############################################################################
# Testing
###############################################################################

if __name__ == "__main__":
    frame_comparison()
