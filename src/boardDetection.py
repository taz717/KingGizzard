import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
CHECKERBOARD = (7,7)

# class for the spaces within a chess board
class Space:
    def __init__(self, p1, p2, p3):
        self.maxY = p3[1]
        self.maxX = p2[0]
        self.minY = p1[1]
        self.minX = p1[0]
        centerX = (self.maxX - self.minX)//2
        centerY = (self.maxX - self.minX)//2
        self.center = (centerX, centerY)
        self.status = False 

    def __str__(self):
        string = f"min: ({self.minX}, {self.minY}) Max: ({self.maxX}, {self.maxY})"
        return string
    
    def in_space(self, x, y):
        if (self.minX <= x <= self.maxX and self.minY <= y <= self.maxY):
            self.empty = True
            return 
        else:
            self.status = False
            return
        
    def init_status(self):
        self.status = True

# Class that will hold all the spaces and the border min x,y and max x,y
class ChessBoard:
    def __init__(self):
        grid = get_grid()
        self.border = [grid['1'][0][0], grid['1'][-1][0],grid['1'][0][1], grid['8'][0][1]] 
        self.spaces = self.get_space(grid)
        
    def __str__(self):
        temp_dict = {key: str(value) for key, value in self.spaces.items()}
        return str(temp_dict)

    #move the points it spaces 
    def get_space(self, grid):
        squares = {}
        col = 0
        names = ['A','B','C','D','E','F', 'G','H']
        keyList = list(grid.keys())

        for keys in keyList[:-1]:
            col+=1
            for i in range(0, (len(grid['0'])-1)):
                space = Space(grid[keys][i],grid[keys][i+1], grid[str(int(keys)+1)][i])
                index  = str(names[i]) + str(col)
                squares[index] = space
        return squares
                 
    #will be used to determine where to look for changes 
    def in_border(self, x, y):
        if (self.border[0] <= x <= self.border[1] and self.border[2] <= y<= self.border[1]):
            return True
        else:
            return False
        
    # will initialize the first two lines on each side at the start 
    def initialize_board(self):
        names = ['A','B','C','D','E','F', 'G','H']
        lines = ['1','2', '7', '8']

        for i in lines:
            for n in names:
                self.spaces[n + i].status = True

    #display board in a 2d list with 1 and 0
    def display_board(self):
        boardState = []
        line = []

        for key in self.spaces:
            if self.spaces[key].status:
                line.append(1)
            else:
                line.append(0)
            if 'H' in key:
                boardState.append(line)
                line = []
        return boardState


#HELPER FUNCTIONS TO GET GRID

#Displays the points drawn within opencv            
def draw_points(grid):
    img = cv2.imread("C:\\Users\\Gordon\\OneDrive\\Desktop\\School\\cmpt496\\KingGizzard\\images\\chessboard.png")

    for key in grid:
        for i in grid[key]:
            cv2.circle(img, (i[0], i[1]), 5, (0, 255, 0), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#get the average y 
def get_average_y(grid):
    avgY = []

     #y vals  for each key all 7 vals  in each row
    for key in grid:
        y = 0
        for i in grid[key]:
            y += grid[key][1][1]
        avgY.append(y//7)
    return avgY

#get the average x 
def get_average_x(grid):
    avgX = []

    #x vals I need 7 keys and the index in each col
    for i in range(len(grid['1'])):
        x = 0
        for key in grid:
            x +=  grid[key][i][0]
        avgX.append(x//7)
    return  avgX

#get the board points 
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
   
#take picture of the 
def get_grid():

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
            cv2.imwrite('C:\\Users\\Gordon\\OneDrive\\Desktop\\School\\cmpt496\\KingGizzard\\images\\chessboard.png', frame)
            print("Screenshot saved as 'screenshot.png'")
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

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
    images = glob.glob('C:\\Users\\Gordon\\OneDrive\\Desktop\\School\\cmpt496\\KingGizzard\\images\\chessboard.png')
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
 
    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    #ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    y = get_average_y(grid)
    x = get_average_x(grid)
    grid = get_board(grid, x, y)
    draw_points(grid)

    return(grid)


def test():
    board = ChessBoard()
    print(str(board))
    print()
    print(board.display_board())
    board.initialize_board()
    print()
    print()
    print(board.display_board())


test()

# hello
print("small change to fix github commit")