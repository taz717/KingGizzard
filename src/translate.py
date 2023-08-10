class translator:
    def __init__(self):
        self.numToColDict = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }

        self.boardPrevious = [
            ["r", "n", "b", "k", "q", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],

            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "K", "Q", "B", "N", "R"],
        ]
        self.boardCurrent = [
            ["r", "n", "b", "k", "q", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "K", "Q", "B", "N", "R"],
        ]

        self.boardPreviousBin = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]

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
                    vals.append(
                        # [Binary, location, row, col]
                        # or
                        # [Piece, location, row, col]
                        [
                            matrix1[i][j],
                            self.numToColDict[j + 1] + str(8 - i),
                            i,
                            j,
                        ]
                    )
        return vals

    def calculate_move(self, change):
        """
        This method is meant to form a move from the change 2Dlist
        that is returned from the compare_boards method

        it follows the chess.com notation for moves dealing with
        takes, king side castling, and queen side castling

        parems: change (2d list)
        returns: move (str)
        """
        move = ""
        print(change)

        endPiece = change[0][0].upper()
        end = change[0][1]
        startPiece = change[1][0].upper()
        start = change[1][1]

        ## king side castle
        if (
            startPiece == "K"
            and start == "E1"
            and end == "G1"
            or startPiece == "K"
            and start == "E8"
            and end == "G8"
        ):
            return "O-O"

        ## queen side castle
        elif (
            startPiece == "K"
            and start == "E1"
            and end == "C1"
            or startPiece == "K"
            and start == "E8"
            and end == "C8"
        ):
            return "O-O-O"

        ## takes
        elif endPiece != " ":
            return startPiece + "x" + end

        ## normal move no takes
        return startPiece + end

    def update_board(self, board):
        """
        updates the current board to the new board
        parems: board (2d list)
        returns: None
        """
        self.boardCurrent = board

    def update_board_bin(self, board):
        """
        updates the current board to the new board
        parems: board (2d list)
        returns: None
        """

        self.boardPreviousBin = board

    def convert_board(self, vals):
        """
        converts the new bin board to new piece board
        parems: vals (list)
        returns: None
        """

        pieceMoved = self.boardCurrent[vals[1][2]][vals[1][3]]
        self.boardCurrent[vals[1][2]][vals[1][3]] = " "
        self.boardCurrent[vals[0][2]][vals[0][3]] = pieceMoved

    def translate(self, boardCurrentBin):
        """
        translates the bin 2d list to a 2d list of pieces
        then figures out the move and returns it
        parems: boardCurrentBin (2d list)
        returns: move (str)
        """

        binChange = self.compare_boards(self.boardPreviousBin, boardCurrentBin)
        self.convert_board(binChange)
        pieceChange = self.compare_boards(self.boardPrevious, self.boardCurrent)
        move = self.calculate_move(pieceChange)

        self.update_board_bin(boardCurrentBin)
        self.update_board(self.boardCurrent)

        return move



if __name__ == "__main__":
    normalBoardBinMove = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]

    t = translator()
    # print(t.compare_boards(t.boardCurrent, testMoveBoard))
    print(t.translate(normalBoardBinMove))

