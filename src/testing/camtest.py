import cv2

def main():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow("webcam", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return

main()

