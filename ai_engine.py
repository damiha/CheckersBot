import time

from constants import refreshTime, valuePerMan, valuePerKing
from helpers import getKeyFromPosition, getBlackCharactersFromFEN, getWhiteCharactersFromFEN, \
    getNumberOfPiecesFromCharacters, getRingDistributionFromCharacters, getPositionalPoints
from info_ai import InfoAI
from draughts import WHITE as WHITE_PLAYER, BLACK as BLACK_PLAYER


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

        alpha = float("-inf")
        beta = float("inf")

        self.infoAI.estimation = self.minimax(position, isMaximizingPlayer, self.infoAI.searchDepth, alpha, beta)
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

            maxEvaluation = float("-inf")

            moves, captures = position.legal_moves()

            for moveSequence in moves:

                newPosition = position.copy_fast()

                # apply whole FORCING move sequence
                for pieceMove in moveSequence:
                    newPosition.move(pieceMove)

                # after moves have been applied, it's certainly other player's turn
                newEvaluation = self.minimax(newPosition, not isMaximizingPlayer, depth - 1, alpha, beta)

                # from this position, white can force a win so don't even consider other moves
                if newEvaluation == float("inf"):

                    self.updateStatsIfTopLevel(depth, maxEvaluation, moveSequence)
                    return float("inf")

                if newEvaluation > maxEvaluation:

                    maxEvaluation = newEvaluation
                    self.updateStatsIfTopLevel(depth, maxEvaluation, moveSequence)

                # code for alpha-beta-pruning
                alpha = max(alpha, newEvaluation)
                if self.infoAI.alphaBetaOn and beta <= alpha:
                    break

            return maxEvaluation

        else:

            minEvaluation = float("inf")

            moves, captures = position.legal_moves()

            for moveSequence in moves:

                newPosition = position.copy_fast()

                # apply whole FORCING move sequence
                for pieceMove in moveSequence:
                    newPosition.move(pieceMove)

                newEvaluation = self.minimax(newPosition, not isMaximizingPlayer, depth - 1, alpha, beta)

                # from this position, black can force a win so don't even consider other moves
                if newEvaluation == float("-inf"):

                    self.updateStatsIfTopLevel(depth, minEvaluation, moveSequence)
                    return float("-inf")

                if newEvaluation < minEvaluation:

                    minEvaluation = newEvaluation
                    self.updateStatsIfTopLevel(depth, minEvaluation, moveSequence)

                # code for alpha-beta-pruning
                beta = min(beta, newEvaluation)
                if self.infoAI.alphaBetaOn and beta <= alpha:
                    break

            return minEvaluation

    def updateStatsIfTopLevel(self, depth, bestEvaluation, bestMoveSequence):
        if depth == self.infoAI.searchDepth:
            self.infoAI.bestMoveSequence = bestMoveSequence
            self.infoAI.estimation = bestEvaluation

            if self.infoAI.debugOn:
                print(self.infoAI.bestMoveSequence)
                print(self.infoAI.estimation)

    # TODO: come up with a decent static evaluation
    def staticEvaluation(self, position):
        self.infoAI.evaluatedPositions += 1

        if position.is_over():
            if position.has_player_won(WHITE_PLAYER):
                return float("inf")
            elif position.has_player_won(BLACK_PLAYER):
                return float("-inf")
            else:
                # draw
                return 0.0
        else:
            fenString = position.get_li_fen()
            blackCharacters = getBlackCharactersFromFEN(fenString)
            whiteCharacters = getWhiteCharactersFromFEN(fenString)

            numberOfMenW, numberOfKingsW = getNumberOfPiecesFromCharacters(whiteCharacters)
            numberOfMenB, numberOfKingsB = getNumberOfPiecesFromCharacters(blackCharacters)

            ringDistributionWhite = getRingDistributionFromCharacters(whiteCharacters)
            ringDistributionBlack = getRingDistributionFromCharacters(blackCharacters)

            # reward play in the center
            positionalPointsWhite = getPositionalPoints(ringDistributionWhite)
            positionalPointsBlack = getPositionalPoints(ringDistributionBlack)

            # ^3 to preserve sign but reward/punish strong imbalance
            pointsWhite = numberOfMenW * valuePerMan + numberOfKingsW * valuePerKing + positionalPointsWhite
            pointsBlack = numberOfMenB * valuePerMan + numberOfKingsB * valuePerKing + positionalPointsBlack

            return (pointsWhite - pointsBlack) ** 3
