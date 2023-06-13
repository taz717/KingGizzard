import chess as ch
import random as rd


class KingGizzard:
    """
    King Gizzard is a chess engine that uses the minimax algorithm
    to evaluate the best move for the engine.
    """

    def __init__(self, board, maxDepth, color):
        """
        initializes the engine
        parems: board (chess.Board), maxDepth (int), color (chess.Color)
        returns: none
        """
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def get_best_move(self):
        """
        returns the best move for the engine
        parems: none
        returns: best move (chess.Move)
        """
        return self.engine(None, 1)

    def evaluate(self):
        """
        returns the value of the current board
        parems: none
        returns: value (float)
        """
        compt = 0
        for i in range(64):
            compt += self.square_res_points(ch.SQUARES[i])
        compt += self.mate_oppurtunity() + self.opening() + 0.001 * rd.random()
        return compt

    def opening(self):
        """
        returns a value for the opening
        parems: none
        returns: value (float)
        """
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    def mate_oppurtunity(self):
        """
        returns a value for the mate oppurtunity
        parems: none
        returns: value (float)
        """
        if self.board.legal_moves.count() == 0:
            ## engine getting checked
            if self.board.turn == self.color:
                -999

            else:
                ## opponent getting checked
                return 999

        ## there is a legal move
        else:
            return 0

    ## takes a square as input and returns
    ## Han's Berlinder's system value of its resident
    ## https://www.chessprogramming.org/Hans_Berliner
    def square_res_points(self, square):
        """
        returns the value of a piece on a square
        parems: square (chess.SQUARE)
        returns: value (float)
        """
        pieceValue = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == ch.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == ch.BISHOP:
            pieceValue = 3.33
        elif self.board.piece_type_at(square) == ch.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == ch.QUEEN:
            pieceValue = 8.8

        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):
        """
        checks for moves, evaluates them and returns the best one
        essentially its main function.

        uses alpha-beta pruning to reduce the number of nodes to be evaluated

        parems: candidate (float), depth (int)
        returns: value (float)
        """
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evaluate()

        else:
            ## list of legal moves for the current board
            moveList = list(self.board.legal_moves)

            ##  init candidate
            newCandidate = None

            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            for i in moveList:
                ## play i
                self.board.push(i)

                ## recursive call
                ## get value
                value = self.engine(newCandidate, depth + 1)

                ## minmax
                ## basic

                ## if maxim (engine turn)
                if value > newCandidate and depth % 2 != 0:
                    newCandidate = value
                    if depth == 1:
                        move = i

                ## if minim (opponent turn)
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                ## alpha-beta pruning
                ## if previous move was made by engine
                if candidate != None and value < candidate and depth % 2 == 0:
                    self.board.pop()
                    break

                ## if previous move was made by opponent
                elif candidate != None and value > candidate and depth % 2 != 0:
                    self.board.pop()
                    break

                ## undo last move
                self.board.pop()

        if depth > 1:
            ## return value of the node in the tree
            return newCandidate
        else:
            return move
