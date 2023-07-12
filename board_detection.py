import cv2
import numpy as np
import os
import glob
 
# Defining the dimensions of checkerboard
CHECKERBOARD = (7,7)
def draw_points(grid):
    img = cv2.imread("images/new_frame.png")
    for key in grid:
        for i in grid[key]:
            cv2.circle(img, (i[0], i[1]), 5, (0, 255, 0), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
def get_missing_col_row(grid):
    yDiff =  grid["2"][0][1] - grid['1'][0][1]
    xDiff=  grid["1"][1][0] - grid['1'][0][0]
    col1X =  grid['1'][0][0] - xDiff
    col8X =  grid['1'][6][0] + xDiff
    row1Y =  grid['1'][0][1] - yDiff
    row8Y = grid["7"][0][1] + yDiff
    #add points to the columns that are unmarked
    for key in grid:
        grid[key].append((col1X, grid[key][0][1]))
        grid[key].append((col8X, grid[key][0][1]))

    grid['0'] = []
    grid['8'] = []
    #add points the the last two rows 
    for i in range(len(grid['1'])):
        grid['0'].append((grid['1'][i][0], row1Y))
        grid['8'].append((grid['1'][i][0], row8Y)) 
        
                #First iteration go back by 1 and from that 
    return grid
def get_board():
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
        
        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
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
                
           
    grid = get_missing_col_row(grid)
    draw_points(grid)

    return(grid)


    
def main():
    print(get_board())


main()