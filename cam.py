import cv2 
import numpy as np
from PIL import ImageGrab


def frame_comparison():
    image_path1 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess1.png"
    #image_path2 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess1.png"
    image_path2 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess2.png"
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    if image1 is None:
        print("Error opening file 1")
        exit()

    if image2 is None:
        print ("Error opening file 2")
        exit()


    grey_1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grey_1_resized = cv2.resize(grey_1, (600, 600))

    grey_2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    grey_2_resized = cv2.resize(grey_2, (600, 600))
    diff = cv2.absdiff (grey_1_resized, grey_2_resized)

    is_diff = np.all((diff == 0) | (diff == 255))

    if not is_diff: 
        cv2.imshow("Difference", diff)
    else:
        print ("No difference in images")
    cv2.waitKey(0)
    cv2.destroyAllWindows

    return

if __name__ == "__main__":
    frame_comparison()