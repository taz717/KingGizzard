from lib import KingGizzard as kg
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
        engine = kg.KingGizzard(self.board, maxDepth, color)
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
            print(self.board.outcome())

            ## reset the board
            self.board.reset
            ## start new game
            self.start_game()


if __name__ == "__main__":
    newBoard = ch.Board()
    game = Main(newBoard)
    game.start_game()
