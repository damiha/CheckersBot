import copy
import time
import sys

from constants import refreshTime
from helpers import getBlackPiecesFromFEN, getWhitePiecesFromFEN, getKeyFromPosition
from info_ai import InfoAI
from draughts import WHITE as WHITE_PLAYER, BLACK as BLACK_PLAYER, Move


class AIEngine:

    def __init__(self, appInfo):

        self.infoAI = InfoAI()
        # get app info to receive commands
        self.appInfo = appInfo

        # lru_cache doesn't work since treats calls too differently
        self.cache = dict()

    def runTimer(self):

        startTime = time.perf_counter()

        while self.appInfo.analysisRunning:

            endTime = time.perf_counter()
            self.infoAI.runtime = round(endTime - startTime, 2)

            # sleep to prevent time measuring from becoming a performance drainer
            time.sleep(refreshTime)

    def runMinimax(self, position):

        # reset before running
        self.infoAI.evaluatedPositions = 0
        self.infoAI.bestMoveSequence = None
        self.infoAI.estimation = None
        self.cache = dict()

        # whose_turn() == 2 => white player
        isMaximizingPlayer = position.whose_turn() == 2

        alpha = -sys.maxsize
        beta = sys.maxsize

        self.minimax(position, isMaximizingPlayer, self.infoAI.searchDepth, alpha, beta)
        self.appInfo.analysisRunning = False

    # TODO: after basic search depth exceeded, look one step further to avoid immediate danger
    def minimax(self, position, isMaximizingPlayer, depth, alpha, beta):

        key = getKeyFromPosition(position)

        if self.infoAI.memoizationOn and (value := self.cache.get(key)) is not None:
            return value

        elif depth == 0 or not self.appInfo.analysisRunning or position.is_over():

            evaluation = self.staticEvaluation(position)

            if self.infoAI.memoizationOn:
                self.cache[key] = evaluation

            return evaluation

        if isMaximizingPlayer:
            # set to -Infinity
            maxEvaluation = -sys.maxsize

            moves, captures = position.legal_moves()

            for moveSequence in moves:

                newPosition = copy.deepcopy(position)

                # apply whole FORCING move sequence
                for pieceMove in moveSequence:
                    newPosition.move(pieceMove)

                # after moves have been applied, it's certainly other player's turn
                newEvaluation = self.minimax(newPosition, not isMaximizingPlayer, depth - 1, alpha, beta)

                if newEvaluation > maxEvaluation:
                    maxEvaluation = newEvaluation

                    if depth == self.infoAI.searchDepth:
                        self.infoAI.bestMoveSequence = moveSequence
                        self.infoAI.estimation = maxEvaluation

                        if self.infoAI.debugOn:
                            print(self.infoAI.bestMoveSequence)
                            print(self.infoAI.estimation)

                # code for alpha-beta-pruning
                alpha = max(alpha, newEvaluation)
                if self.infoAI.alphaBetaOn and beta <= alpha:
                    break

            return maxEvaluation

        else:
            # set to +Infinity
            minEvaluation = sys.maxsize

            moves, captures = position.legal_moves()

            for moveSequence in moves:

                newPosition = copy.deepcopy(position)

                # apply whole FORCING move sequence
                for pieceMove in moveSequence:
                    newPosition.move(pieceMove)

                newEvaluation = self.minimax(newPosition,  not isMaximizingPlayer, depth - 1, alpha, beta)

                if newEvaluation < minEvaluation:
                    minEvaluation = newEvaluation

                    if depth == self.infoAI.searchDepth:
                        self.infoAI.bestMoveSequence = moveSequence
                        self.infoAI.estimation = minEvaluation

                        if self.infoAI.debugOn:
                            print(self.infoAI.bestMoveSequence)
                            print(self.infoAI.estimation)

                # code for alpha-beta-pruning
                beta = min(beta, newEvaluation)
                if self.infoAI.alphaBetaOn and beta <= alpha:
                    break

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






