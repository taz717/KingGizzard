import cv2
import numpy as np


def frame_comparison():
       
        cap = cv2.VideoCapture(0)

        # prev_frame = None
        # capture_interval = 5
        # last_capture_time = time.time()

        # while True:
        #     ret, frame = cap.read()
        #     if not ret:
        #         print("Error capturing frame")
        #         break

            
        #     if prev_frame is not None:
        #         grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #         grey_frame_resized = cv2.resize(grey_frame, (600, 600))
        #         diff = cv2.absdiff(grey_frame_resized, prev_frame)

        #         cv2.imshow("Difference", diff)

        #     prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     prev_frame = cv2.resize(prev_frame, (600, 600))

            
        #     current_time = time.time()
        #     if current_time - last_capture_time >= capture_interval:
        #         last_capture_time = current_time

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        # cap.release()
        # cv2.destroyAllWindows()
        

        ret, frame = cap.read()
    
        while True:
            
            cv2.resize(frame, (600, 600))
            cv2.imshow("Webcam", frame)
            grey1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grey1_resized = cv2.resize(grey1, (600, 600))

            # Push 'c' to capture
            key = cv2.waitKey(1)
            if key == ord('c'):
                # cv2.imwrite("new_frame.png", frame)
                # print ("New frame captured")
                
                ret2, new_frame = cap.read()
                if not ret2:
                    print ("Error capturing frame")
                    break
                grey2 = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
                grey2_resized = cv2.resize(grey2, (600, 600))

                # Compare the old frame and the new frame to see if there is a change
                diff = cv2.absdiff(grey1_resized, grey2_resized)

                is_diff = np.all((diff == 0) | (diff == 255))

                if not is_diff:
                    
                    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

                    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    

                    bounding_box = [cv2.boundingRect(cnt) for cnt in contours]

                    for x, y, w, h in bounding_box:
                        cv2.rectangle(diff, (x,y), (x + w, y + h), (255, 255, 255), 1)
                        cv2.imshow("Difference", diff)

                    cv2.imshow("Difference", diff)
                    frame = new_frame
                else:
                    print ("No changes yet")


            # Push 'q' to quit
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
     
    frame_comparison()