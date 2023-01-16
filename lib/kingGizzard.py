import chess as ch
import random as rd


class kingGizzard:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.engine(None, 1)

    def evaluate(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOppurtunity() + self.opening() + 0.001 * rd.random()
        return compt

    def opening(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    def mateOppurtunity(self):
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
    def squareResPoints(self, square):
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

                ## minmax without pruning
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
