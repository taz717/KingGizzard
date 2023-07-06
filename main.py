from src import kingGizzard as kg
import chess as ch

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

    ## play opponent move
    def play_opponent_move(self):
        """
        plays the opponent's move
        parems: none
        returns: none but it does add the ops move to
        the board object
        """
        try:
            ## Don't list this, it doesn't look as nice

            print(self.board.legal_moves)

            if self.board.is_checkmate() == True:
                self.kingWon = True

            print("""To undo your last move, type "undo".""")
            ## get user input
            play = input("your move: ")
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.play_opponent_move()
                return

            self.board.push_san(play)
        except:
            self.play_opponent_move()

    def make_matrix(self, board):
        """
        converts the board object to a 2d array
        parems: board (chess.Board)
        returns: matrix (2d array)
        """

        # type(board) == chess.Board()
        ## https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers
        ## returns 2d array with board

        pgn = board.epd()
        foo = []  # Final board
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  # This is the row I make
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(".")
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
    def player_engine_move(self, maxDepth, color):
        """
        plays the engine's move
        parems: maxDepth (int), color (chess.WHITE or chess.BLACK)
        returns: none but it does add the engine's move to
        the board object
        """
        win = True
        engine = kg.KingGizzard(self.board, maxDepth, color)
        move = engine.get_best_move()
        if move == True:
            self.playerWon = True
        else:
            self.board.push(engine.get_best_move())

    def translate_boards(self, previousTurn):
        """
        translates the board to a string
        parems: previousTurn (chess.Board)
        returns: none
        """
        print(previousTurn == self.board)

    def start_game(self):
        """
        starts the game
        parems: none
        returns: none
        """
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
                self.player_engine_move(maxDepth, ch.WHITE)
                print(self.board)
                vals = self.compare_boards(previousBoard, self.make_matrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                print(vals)

                self.play_opponent_move()

            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while self.board.is_checkmate() == False:
                print(self.board)
                self.play_opponent_move()
                print(self.board)

                print("King Gizzard is thinking...")
                previousBoard = self.make_matrix(self.board)
                self.player_engine_move(maxDepth, ch.BLACK)
                vals = self.compare_boards(previousBoard, self.make_matrix(self.board))
                ## TODO SEND VALS TO ARDUINO TO MOVE PIECES
                print(vals)

            print(self.board)

            matchEnd = self.board.outcome()

            if matchEnd.termination.value == 2:
                print("Stalemate! No one wins...")
            elif self.kingWon == True:
                print("King Gizzard the great has won!")
            elif self.playerWon == True:
                print("I can't believe that I've lost to a human...")

            # print(self.board.outcome())

        ## ask if user wants to play again
        self.gameState = input("Play again? (y/n): ")
        self.kingWon = False
        self.playerWon = False
        return self.gameState
        # ## reset the board
        # self.board.reset
        # ## start new game
        # self.start_game()


if __name__ == "__main__":
    # Fresh Board
    # newBoard = ch.Board()
    # Mate in 2
    newBoard = ch.Board("1n4k1/r5np/1p4PB/p1p5/2q3P1/2P4P/8/4QRK1")
    # Mate in 1
    # newBoard = ch.Board("k7/ppp5/8/8/8/8/3Q4/4RK2")
    # Stalemate check
    # board = chess.Board("k7/8/8/8/8/8/5q2/7K")

    game = Main(newBoard)
    game.start_game()

    if game.gameState == "y":
        game.board.reset()
        game.start_game()

    print("Thanks for playing!")
    exit()
