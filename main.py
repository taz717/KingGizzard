from src import kingGizzard as kg
import chess as ch
import cv2
import threading
import numpy as np
import time


numToLetterDict = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}


class Main:
    """
    main class, runs the game
    """

    def __init__(self, board=ch.Board):
        """
        initializes the board
        parems: board (chess.Board)
        returns: none
        """
        self.board = board
        self.gameState = True
        self.kingWon = False
        self.playerWon = False
        self.reference_frame = None
        self.centroids = []
    
    ## play player move
    def play_player_move(self):
        """
        plays the opponent's move
        parems: none
        returns: none but it does add the ops move to
        the board object
        """
        try:
            print(self.board.legal_moves)

            if self.board.is_checkmate() == True:
                self.kingWon = True

            print("""To undo your last move, type "undo".""")

            ## get user input
            play = input("your move: ")

            # Use this to check current reference image
            if play == "show":
                cv2.imshow("Reference image", self.reference_frame)
                cv2.waitKey(6000)
                cv2.destroyWindow("Reference image")
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.play_player_move()
                return

            self.board.push_san(play)
        except:
            self.play_player_move()

    def make_matrix(self, board):
        """
        converts the board object to a 2d array
        parems: board (chess.Board)
        returns: matrix (2d array)
        """

        ## https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers

        pgn = board.epd()
        foo = []  # Final board
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  # This is the row I make
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(" ")
                else:
                    foo2.append(thing)
            foo.append(foo2)
        return foo

    def compare_boards(self, matrix1, matrix2):
        """
        compares two 2d arrays and returns the values that are different
        parems: matrix1 (2d array), matrix2 (2d array)
        returns: vals (list)
        """
        vals = []
        for i in range(len(matrix1)):
            for j in range(len(matrix1)):
                if matrix1[i][j] != matrix2[i][j]:
                    vals.append(numToLetterDict[j + 1] + str(i + 1))
                
        return vals

    ## play king gizzard move
    def player_engine_move(self, maxDepth, color, cap):
        """
        plays the engine's move
        parems: maxDepth (int), color (chess.WHITE or chess.BLACK)
        returns: none but it does add the engine's move to
        the board object
        """
        # cap = cv2.VideoCapture(0)
        # ret, frame = cap.read()
        # self.board = frame
        win = True
        engine = kg.KingGizzard(self.board, maxDepth, color)
        move = engine.get_best_move()
        if move == True:
            self.playerWon = True
        else:
            self.board.push(engine.get_best_move())


        ret, frame = cap.read()
        self.reference_frame = frame.copy()
        # cv2.imshow("Reference frame", self.reference_frame)
        # cv2.waitKey(6000)
        # cv2.destroyWindow("Reference frame")

    def translate_boards(self, previousTurn):
        """
        translates the board to a string
        parems: previousTurn (chess.Board)
        returns: none
        """

        print(previousTurn == self.board)

    def start_game(self, cap):
        """
        starts the game
        parems: none
        returns: none
        """

        ret, frame = cap.read()

        self.oldFrame = frame
        
        ## get opponent color
        color = None
        while color not in ["w", "b"]:
            color = input("choose color (w/b): ")
        maxDepth = None
        while isinstance(maxDepth, int) == False:
            maxDepth = int(input("choose max depth: "))
        if color == "b":
            while self.board.is_checkmate() == False:
                print("King Gizzard is thinking...")

                previousBoard = self.make_matrix(self.board)
                self.player_engine_move(maxDepth, ch.WHITE, cap)
                print(self.board)
                vals = self.compare_boards(previousBoard, self.make_matrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                print(vals)
                
                self.play_player_move()

            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while self.board.is_checkmate() == False:
                print(self.board)
                self.play_player_move()
                print(self.board)

                print("King Gizzard is thinking...")
                previousBoard = self.make_matrix(self.board)
                self.player_engine_move(maxDepth, ch.BLACK, cap)
                vals = self.compare_boards(previousBoard, self.make_matrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                # Really, should be sending vals to translator,
                # then from there, making adjustments to the
                # board on the translator as appropriate (confirming it from
                # visual data from openCV image)
                print(vals)

                print(self.make_matrix(newBoard))

            print(self.board)

            matchEnd = self.board.outcome()

            if matchEnd.termination.value == 2:
                print("Stalemate! No one wins...")
            elif self.kingWon == True:
                print("King Gizzard the great has won!")
            elif self.playerWon == True:
                print("I can't believe that I've lost to a human...")

        ## ask if user wants to play again
        self.gameState = input("Play again? (y/n): ")
        self.kingWon = False
        self.playerWon = False
        cv2.destroyAllWindows()
        return self.gameState

    
    def frame_comparison(self, cap):

        # Pull reference frame here, and process that for the greyscale
        ret, frame = cap.read()

        while True:
            cv2.resize(frame, (600, 600))
            cv2.imshow("Webcam", frame)
            grey1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grey1_resized = cv2.resize(grey1, (600, 600))

            key = cv2.waitKey(1)
            if key == ord('c'):
                ret2, new_frame = cap.read()
                if not ret2:
                    print("Error capturing frame")
                    break
                grey2 = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
                grey2_resized = cv2.resize(grey2, (600, 600))

                diff = cv2.absdiff(grey1_resized, grey2_resized)
                is_diff = np.all((diff == 0) | (diff == 255))

                if not is_diff:
                    _, threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    small_movement_bound = 100
                    bounding_box = [cv2.boundingRect(cnt) for cnt in contours if cv2.contourArea(cnt) > small_movement_bound]

                    self.centroids = []  # Reset the centroids list
                    for x, y, w, h in bounding_box:
                        centroid_x = x + (w // 2)
                        centroid_y = y + (h // 2)
                        centroid = (centroid_x, centroid_y)
                        self.centroids.append(centroid)
                        self.centroids = self.centroids[-2:] #only stores the last 2 centroids
                        cv2.circle(diff, centroid, 2, (255, 255, 255), 1)
                        cv2.rectangle(diff, (x, y), (x + w, y + h), (255, 255, 255), 1)
                        cv2.imshow("Difference", diff)

                        text = f"Centroid: {centroid}"
                        cv2.putText(diff, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    cv2.imshow("Difference", diff)
                    frame = new_frame
                else:
                    print("No changes yet")


            if key == ord('p'):  # Print centroids when 'p' key is pressed
                for centroid in self.centroids:
                    print("Centroid:", centroid)
            
            
            # Push 'q' to quit
            if key == ord('q'):
                break

            

        cap.release()

        return



if __name__ == "__main__":
    # Fresh Board
    newBoard = ch.Board()
    
    # Mate in 2
    # newBoard = ch.Board("1n4k1/r5np/1p4PB/p1p5/2q3P1/2P4P/8/4QRK1")

    # white and black can castle on queen or king side
    # newBoard = ch.Board("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R")

    # Mate in 1
    #newBoard = ch.Board("k7/ppp5/8/8/8/8/3Q4/4RK2")
    # Stalemate check
    # board = chess.Board("k7/8/8/8/8/8/5q2/7K")

    cap = cv2.VideoCapture(0)

    game = Main(newBoard)

    #print(game.make_matrix(newBoard))

    t = threading.Thread(target=game.frame_comparison, args=(cap,))
    t. start()
    
    # print(game.make_matrix(newBoard))
    game.start_game(cap)

    if game.gameState == "y":
        game.board.reset()
        game.start_game(cap)


    t.join()
    print("Thanks for playing!")

