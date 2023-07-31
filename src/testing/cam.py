import cv2 
import numpy as np



def frame_comparison():
    image_path1 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess1.png"
    image_path3 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess3.png"
    image_path2 = "C:\\Users\\azn_g\\Desktop\School\\Final Project\\King Gizzard\\chess2.png"
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)
    image3 = cv2.imread(image_path3)
    grey_3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
    grey_3_resized = cv2.resize(grey_3, (600, 600))
    cv2.imwrite("Starting game.png", grey_3_resized)
    centroids = []
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



    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    # Find contours of the changed regions
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding boxes of the changed regions (ignores small movements)
    small_movement_bound = 100
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > small_movement_bound]
    num = 1

    # Draw rectangles around the changed regions on the images
    for x, y, w, h in bounding_boxes:
        centroid_x = x + (w // 2)
        centroid_y = y + (h // 2)
        centroid = (centroid_x, centroid_y)
        centroids.append(centroid)
        cv2.circle(diff, centroid, 2, (255,255,255), 1)
        text = "Centroid: " + str(num)
        #cv2.putText(diff, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(diff, (x,y), (x + w, y + h), (255, 255, 255), 1)
        cv2.imshow("Difference", diff)
        num=num+1
        

    # Display the images with the changed regions highlighted
    cv2.imshow("Image 1", grey_1_resized)
    cv2.imshow("Image 2", grey_2_resized)
    cv2.imshow("Difference", diff)
    for i in centroids:
            print("centroid position: " + str(i))
    cv2.imwrite("Centroid position.png", diff)

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

if __name__ == "__main__":
    frame_comparison()