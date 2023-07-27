import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
CHECKERBOARD = (7,7)
class Space:
    def __init__(self, p1, p2, p3, p4):
        self.maxY = p3[1]
        self.maxX = p2[0]
        self.minY = p1[1]
        self.minX = p1[0]
        centerX = (self.maxX - self.minX)//2
        centerY = (self.maxX - self.minX)//2
        self.center = (centerX, centerY)

    def in_space(self, x, y):
        if (self.minX <= x <= self.maxX and self.minY <= y <= self.maxY):
            return True
        else:
            return False
        
# TODO create class that will contain the spaces
class ChessBoard:
    def __init__(self, grid):
        self.border = [grid['1'][0][0], grid['1'][-1][0],grid['1'][0][1], grid['8'][0][1]] 
        self.spaces = self.get_space()
        
    
    def get_space(grid):
        squares = {}
        col = 0
        Names = ['A','B','C','D','E','F', 'G','H']
        for keys in grid:
            col+=1
            for i in range(len(grid['0']) - 1 ):
                space = space(grid[str(i+1)][i],grid[str(i+1)][i+1], grid[str(i+2)][i])
                index  = str(Names[i]) + str(col)
                squares[index] = space
        return squares
                 
    def is_in_border(self, x, y):
        if (self.boreder[0] <= x <= self.boreder[1] and self.boreder[2] <= y<= self.boreder[1]):
            return True
        else:
            return False


def draw_points(grid):
    img = cv2.imread("images/chessboard.png")
    for key in grid:
        for i in grid[key]:
            cv2.circle(img, (i[0], i[1]), 5, (0, 255, 0), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()

def get_average_y(grid):
    avgY = []
     #y vals  for each key all 7 vals  in each row
    for key in grid:
        y = 0
        for i in grid[key]:
            y += grid[key][1][1]
        avgY.append(y//7)
    return avgY
   
def get_average_x(grid):
    avgX = []
    #x vals I need 7 keys and the index in each col
    for i in range(len(grid['1'])):
        x = 0
        for key in grid:
            x +=  grid[key][i][0]
        avgX.append(x//7)
    return  avgX

def get_board(grid, avgX, avgY):
    yDiff =  avgY[1] - avgY[0]
    xDiff=  avgX[1] - avgX[0]
    avgX.insert(0,(avgX[0] - xDiff))
    avgX.append(avgX[7] + xDiff)
    avgY.insert(0, (avgY[0] - yDiff))
    avgY.append(avgY[7] + yDiff)
    col = 0 
    grid.clear()
    for y in avgY:
        grid[str(col)] = []
        for x in avgX:
            grid[str(col)].append((x,y))
        col +=1 

    return grid
   

def get_grid():
    '''
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Failed to open the webcam")
        exit()

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Display the frame in a window named "Webcam"
        cv2.imshow("Webcam", frame)

        # Wait for a key press event
        key = cv2.waitKey(1)

        # Capture a screenshot when the spacebar is pressed
        if key == ord('s'):  # Check for spacebar press
            # Save the frame as an image
            cv2.imwrite('images/screenshot.png', frame)
            print("Screenshot saved as 'screenshot.png'")
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
'''
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = []
    grid = {}
    
    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    
    # Extracting path of individual image stored in a given directory
    images = glob.glob('./images/chessboard.png')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
            
            imgpoints.append(corners2)
    
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            counter = 0
            row = 0
            y_row = 0
            for corner in corners:
                x, y = corner.ravel()  # Get the x and y coordinates
                if (y > y_row + 15):
                    row += 1
                    y_row = y 
                    grid[str(row)] = [(int(x),int(y))]
                else:
                    grid[str(row)].append((int(x),int(y)))
            cv2.imshow('img',img)
            cv2.waitKey(0)
    cv2.destroyAllWindows()
    h,w = img.shape[:2]
 
    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    y = get_average_y(grid)
    x = get_average_x(grid)
    grid = get_board(grid, x, y)
    draw_points(grid)

    return(grid)


    
def main():
    print(get_grid())


main()