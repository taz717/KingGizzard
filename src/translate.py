class translator:
    def __init__(self):
        self.numToLetterDict = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }
        self.boardCurrent = [
            ["R", "N", "B", "K", "Q", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "k", "q", "b", "n", "r"],
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
                        [matrix1[i][j], self.numToLetterDict[j + 1] + str(i + 1)]
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

        startPiece = change[0][0].upper()
        print (startPiece)
        start = change[0][1]
        print (start)
        endPiece = change[1][0].upper()
        print (endPiece)
        end = change[1][1]
        print (end)

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


# if __name__ == "__main__":
#     normalBoardBinMove = [
#         [1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 1, 0, 0, 0, 0, 0, 0],
#         [1, 0, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1],
#     ]

#     t = translator()
#     # print(t.compare_boards(t.boardCurrent, testMoveBoard))
#     print(t.translate(normalBoardBinMove))
