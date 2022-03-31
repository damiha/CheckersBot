import copy
import time
import sys

from helpers import getBlackPiecesFromFEN, getWhitePiecesFromFEN
from info_ai import InfoAI
from draughts import WHITE as WHITE_PLAYER, BLACK as BLACK_PLAYER


class AIEngine:

    def __init__(self, appInfo):

        self.infoAI = InfoAI()
        # get app info to receive commands
        self.appInfo = appInfo

    def runTimer(self):

        startTime = time.perf_counter()

        while self.appInfo.analysisRunning:

            endTime = time.perf_counter()
            self.infoAI.runtime = round(endTime - startTime, 2)

            # sleep to prevent time measuring from becoming a performance drainer
            time.sleep(0.01)

    def runMinimax(self, position):

        # reset before running
        self.infoAI.evaluatedPositions = 0
        self.infoAI.estimation = 0

        # whose_turn() == 2 => white player
        isMaximizingPlayer = position.whose_turn() == 2

        self.minimax(position, isMaximizingPlayer, self.infoAI.searchDepth)
        self.appInfo.analysisRunning = False

    # TODO: after basic search depth exceeded, look one step further to avoid immediate danger
    def minimax(self, position, isMaximizingPlayer, depth):

        if depth == 0 or not self.appInfo.analysisRunning or position.is_over():
            return self.staticEvaluation(position)

        if isMaximizingPlayer:
            # set to -Infinity
            maxEvaluation = -sys.maxsize

            moves = position.get_possible_moves()

            for pieceMove in moves:
                newPosition = copy.deepcopy(position)
                newPosition.move(pieceMove)

                newIsMaximizingPlayer = newPosition.whose_turn() == 2
                newEvaluation = self.minimax(newPosition, newIsMaximizingPlayer, depth - 1)

                if newEvaluation > maxEvaluation:
                    maxEvaluation = newEvaluation

                    if depth == self.infoAI.searchDepth:
                        self.infoAI.bestMove = pieceMove
                        self.infoAI.estimation = maxEvaluation

            return maxEvaluation

        else:
            # set to +Infinity
            minEvaluation = sys.maxsize

            moves = position.get_possible_moves()

            for pieceMove in moves:
                newPosition = copy.deepcopy(position)
                newPosition.move(pieceMove)

                newIsMaximizingPlayer = newPosition.whose_turn() == 2
                newEvaluation = self.minimax(newPosition, newIsMaximizingPlayer, depth - 1)

                if newEvaluation < minEvaluation:
                    minEvaluation = newEvaluation

                    if depth == self.infoAI.searchDepth:
                        self.infoAI.bestMove = pieceMove
                        self.infoAI.estimation = minEvaluation

            return minEvaluation

    # TODO: come up with a decent static evaluation
    def staticEvaluation(self, position):
        self.infoAI.evaluatedPositions += 1

        if position.is_over():
            if position.has_player_won(WHITE_PLAYER):
                return sys.maxsize
            elif position.has_player_won(BLACK_PLAYER):
                return -sys.maxsize
            else:
                # draw
                return 0
        else:
            # TODO: weight men and king pieces differently
            numberOfWhitePieces = getWhitePiecesFromFEN(position.get_li_fen())
            numberOfBlackPieces = getBlackPiecesFromFEN(position.get_li_fen())

            # ^3 to preserve sign but reward/punish strong imbalance
            return (numberOfWhitePieces - numberOfBlackPieces) ** 3






