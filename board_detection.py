import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
CHECKERBOARD = (7,7)
'''
# TODO create class that will contain the spaces
class ChessBoard:
    def __init__(self, spaces):


def get_space(grid):
    squares = {}
    col = 1
    Names = ['A','B','C','D','E','F', 'G','H']
    for i in range(len(grid['0']) - 1 ):
        if (i == 0 or i == 1):
'''           

def draw_points(grid):
    img = cv2.imread("images/new_frame.png")
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
    images = glob.glob('./images/new_frame.png')
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
                if (y > y_row + 5):
                    row += 1
                    y_row = y 
                    grid[str(row)] = [(int(x),int(y))]
                else:
                    grid[str(row)].append((int(x),int(y)))
                
    y = get_average_y(grid)
    x = get_average_x(grid)
    grid = get_board(grid, x, y)
    draw_points(grid)

    return(grid)


    
def main():
    get_grid()


main()