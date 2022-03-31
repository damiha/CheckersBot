from draughts import Game, WHITE as WHITE_PLAYER

from constants import initial_board, tilesPerRow
from helpers import draughtsToCoords, coordsToDraughts, getBlackPiecesFromFEN


class BoardManager:

    def __init__(self):

        self.board = [row[:] for row in initial_board]

        # internal representation using pydraughts
        self.game = Game(variant="standard", fen="startpos")

        # info concerning game
        self.isGameOver = False
        self.whoWon = -1
        # to track a capture sequence
        self.capturedPieces = []
        self.player = 1

        self.blackPiecesCaptured = 0
        self.whitePiecesCaptured = 0

        self.moveHistory = []

        self.allMoves = []
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
        self.capturedPieces = []
        self.player = 1

        self.blackPiecesCaptured = 0
        self.whitePiecesCaptured = 0

        self.moveHistory = []

        self.allMoves = []
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
            self.capturedPieces.append((capturedX, capturedY))

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

            for (capturedX, capturedY) in self.capturedPieces:
                self.board[capturedY][capturedX] = 0

            self.capturedPieces = []

            if isPromotionMove:
                self.board[toY][toX] += 1

        self.player = nextPlayer

    def setPieceMoves(self):

        x, y = self.selected
        fromPos = coordsToDraughts(x, y)
        pieceMoves = []

        for move in self.allMoves:

            fromPosMove, toPosMove = move

            if fromPos == fromPosMove:
                pieceMoves.append(move)

        self.pieceMoves = pieceMoves

    def getMove(self, toX, toY):
        toPos = coordsToDraughts(toX, toY)

        for move in self.pieceMoves:
            if move[1] == toPos:
                return move
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
