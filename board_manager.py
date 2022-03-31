from draughts import Game, WHITE as WHITE_PLAYER

from constants import initial_board, tilesPerRow
from helpers import draughtsToCoords, coordsToDraughts


class BoardManager:

    def __init__(self):

        self.board = [row[:] for row in initial_board]

        # internal representation using pydraughts
        self.game = Game(variant="standard", fen="startpos")

        # info concerning game
        self.isGameOver = False
        self.whoWon = -1

        self.trackedPiecesForDrawing = []
        self.player = 1

        self.blackPiecesCaptured = 0
        self.whitePiecesCaptured = 0

        self.moveHistory = []

        self.allMoveSequences = []
        # the selected piece has to perform any of these longest sequence
        self.forcedMoveSequences = []
        # first moves available to a piece
        self.pieceMoves = []

        self.selected = (-1, -1)

    def resetBoard(self):
        for y in range(tilesPerRow):
            for x in range(tilesPerRow):
                self.board[y][x] = initial_board[y][x]

    def resetGame(self):
        self.game = Game(variant="standard", fen="startpos")

    def resetStatus(self):
        self.isGameOver = False
        self.whoWon = -1
        # to track a capture sequence
        self.trackedPiecesForDrawing = []
        self.player = 1

        self.blackPiecesCaptured = 0
        self.whitePiecesCaptured = 0

        self.moveHistory = []

        self.allMoveSequences = []
        self.forcedMoveSequences = []
        self.pieceMoves = []

        self.selected = (-1, -1)

    def reset(self):
        self.resetGame()
        self.resetBoard()
        self.resetStatus()

    def setGameStatus(self):

        self.isGameOver = self.game.is_over()

        if self.isGameOver:
            if self.game.is_draw() or self.game.is_threefold():
                self.whoWon = 0
            else:
                self.whoWon = 1 if self.game.has_player_won(WHITE_PLAYER) else 2

    # move = [from, to] in draughts notation
    # piece = at in draughts notation

    def makeMove(self, move):
        # use (now) old board position to determine if a promotion occurred
        # promotion moves are last moves, nothing happens when you get to the promotion square and jump away afterwards
        isPromotionMove = self.isPromotion(move)

        fromX, fromY = draughtsToCoords(move[0])
        toX, toY = draughtsToCoords(move[1])

        self.board[toY][toX] = self.board[fromY][fromX]
        self.board[fromY][fromX] = 0

        capturedX, capturedY = self.getPositionOfCapturedPiece(move)
        isCapture = (capturedX, capturedY) != (-1, -1)

        if isCapture:
            # set as captured but don't remove piece from board immediately
            self.board[capturedY][capturedX] = -1
            self.trackedPiecesForDrawing.append((capturedX, capturedY))

            if self.player == 1:
                self.blackPiecesCaptured += 1
            else:
                self.whitePiecesCaptured += 1

        self.game.move(move, isCapture)

        self.moveHistory.append(move)

        thisPlayer = self.player
        nextPlayer = 1 if self.game.whose_turn() == 2 else 2

        # move ends players turn, realize promotions and captures
        if nextPlayer != thisPlayer:

            for (capturedX, capturedY) in self.trackedPiecesForDrawing:
                self.board[capturedY][capturedX] = 0

            self.trackedPiecesForDrawing = []

            # reset capture sequences
            self.allMoveSequences = []
            self.forcedMoveSequences = []
            self.pieceMoves = []

            if isPromotionMove:
                self.board[toY][toX] += 1

        self.player = nextPlayer

    def setPieceMoves(self):

        x, y = self.selected
        fromPos = coordsToDraughts(x, y)
        pieceMoves = []

        # piece doesn't have to perform a multi capture
        if len(self.forcedMoveSequences) == 0:
            # add all first moves of all capture sequences of a piece
            for moveSequence in self.allMoveSequences:
                firstMove = moveSequence[0]

                if firstMove[0] == fromPos:
                    pieceMoves.append(firstMove)

        else:
            # piece has to perform a multi capture so add the first move of remaining sequence
            for forcedMoveSequence in self.forcedMoveSequences:
                firstMove = forcedMoveSequence[0]

                if firstMove[0] == fromPos:
                    pieceMoves.append(firstMove)

        self.pieceMoves = pieceMoves

    def getMove(self, toX, toY):

        fromPos = coordsToDraughts(self.selected[0], self.selected[1])
        toPos = coordsToDraughts(toX, toY)

        # no chosenMoveSequence ?
        if len(self.forcedMoveSequences) == 0:

            foundMove = False

            for moveSequence in self.allMoveSequences:
                firstMove = moveSequence[0]

                # making a move means choosing a move sequence
                if firstMove == [fromPos, toPos]:

                    foundMove = True

                    # first move is played, so set to next
                    if len(moveSequence) > 1:
                        # append since forcedMoveSequence hasn't been saved yet
                        self.forcedMoveSequences.append(moveSequence[1:])

            if foundMove:
                return [fromPos, toPos]

        else:

            foundMove = False

            for forcedMoveSequence in self.forcedMoveSequences:
                firstMove = forcedMoveSequence[0]

                if firstMove == [fromPos, toPos]:
                    foundMove = True

                    # remove first move
                    forcedMoveSequence.pop(0)

                    # empty lists are forbidden
                    if len(forcedMoveSequence) == 0:
                        self.forcedMoveSequences.remove(forcedMoveSequence)

            if foundMove:
                return [fromPos, toPos]

        return None

    def getPositionOfCapturedPiece(self, move):

        fromX, fromY = draughtsToCoords(move[0])
        toX, toY = draughtsToCoords(move[1])

        dirX = 1 if (toX - fromX) > 0 else -1
        dirY = 1 if (toY - fromY) > 0 else -1

        probX = fromX
        probY = fromY

        # walk along the diagonal
        while probX != toX and probY != toY:

            if (self.player == 1 and self.board[probY][probX] > 2) or \
                    (self.player == 2 and 1 <= self.board[probY][probX] <= 2):
                return probX, probY

            probX += dirX
            probY += dirY

        return -1, -1

    def isPromotion(self, move):

        fromX, fromY = draughtsToCoords(move[0])
        toX, toY = draughtsToCoords(move[1])

        return (self.board[fromY][fromX] == 1 and toY == 0) or \
               (self.board[fromY][fromX] == 3 and toY == (tilesPerRow - 1))

