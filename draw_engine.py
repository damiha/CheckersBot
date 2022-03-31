import pygame

from constants import *
from helpers import draughtsToCoords


class DrawEngine:

    def __init__(self, app):

        self.screen = app.screen
        self.boardManager = app.boardManager
        self.appInfo = app.appInfo
        self.infoAI = app.aiEngine.infoAI

        # draw everything game related on to here to rotate easily (if whole screen is rotated, then sidebar is as well)
        self.boardSurface = pygame.Surface(boardSize)
        self.sideBarSurface = pygame.Surface((windowSize[0] - boardSize[0], boardSize[1]))

        # lay a transparent gray rect over the screen to indicate that the board doesn't accept user input at the moment
        self.overlaySurface = pygame.Surface(boardSize)
        self.overlaySurface.fill(GREY)
        self.overlaySurface.set_alpha(OVERLAY_ALPHA)

        self.sideBarFont = pygame.font.SysFont("monospace", sideBarFontSize)
        self.numberingFont = pygame.font.SysFont("monospace", numberingFontSize)
        self.promotionFont = pygame.font.SysFont("monospace", promotionFontSize)
        self.gameOverFont = pygame.font.SysFont("monospace", gameOverFontSize)
        self.restartFont = pygame.font.SysFont("monospace", restartFontSize)

        # predefined labels to make layouts easier
        barText = "-" * barLength
        self.barLabel = self.sideBarFont.render(barText, True, WHITE)

        blankText = " " * barLength
        self.blankLabel = self.sideBarFont.render(blankText, True, WHITE)

    def drawLabels(self, labels, lineNumber):

        # Sidebar has dimensions 400 x 800 and is positioned at 800, 0
        # padding is 5, 5
        offsetX, offsetY = (5, 5)

        for label in labels:
            self.sideBarSurface.blit(label, (offsetX, offsetY + lineNumber * lineHeight))
            lineNumber += 1

    def drawSidebar(self):

        playerText = "player: " + ("white" if self.boardManager.player == 1 else "black")
        playerLabel = self.sideBarFont.render(playerText, True, WHITE)

        piecesText = f"white captured: {self.boardManager.blackPiecesCaptured}, black captured: {self.boardManager.whitePiecesCaptured}"
        piecesLabel = self.sideBarFont.render(piecesText, True, WHITE)

        loadStoreText = "load [L], store [S]"
        loadStoreLabel = self.sideBarFont.render(loadStoreText, True, WHITE)

        flipAnalyzeText = "flip [F], analyze [A]"
        flipAnalyzeLabel = self.sideBarFont.render(flipAnalyzeText, True, WHITE)

        self.sideBarSurface.fill(BLACK)

        labels = [
            playerLabel,
            piecesLabel,
            self.blankLabel,
            loadStoreLabel,
            flipAnalyzeLabel
        ]

        self.drawLabels(labels, 0)

        if self.appInfo.analysisModeOn:

            searchDepthText = f"[+/-] search-depth: {self.infoAI.searchDepth}"
            searchDepthLabel = self.sideBarFont.render(searchDepthText, True, WHITE)

            alphaBetaText = f"[1] alpha-beta-pruning: {self.infoAI.alphaBetaOn}"
            alphaBetaLabel = self.sideBarFont.render(alphaBetaText, True, WHITE)

            memoizationText = f"[2] memoization: {self.infoAI.memoizationOn}"
            memoizationLabel = self.sideBarFont.render(memoizationText, True, WHITE)

            enterText = f"[ENTER] to show/hide metrics"
            enterLabel = self.sideBarFont.render(enterText, True, WHITE)

            leaveAnalysisText = f"[A] to leave analysis mode"
            leaveAnalysisLabel = self.sideBarFont.render(leaveAnalysisText, True, WHITE)

            analysisLabels = [
                self.barLabel,
                self.blankLabel,
                searchDepthLabel,
                alphaBetaLabel,
                memoizationLabel,
                self.blankLabel,
                enterLabel,
                leaveAnalysisLabel
            ]

            self.drawLabels(analysisLabels, 6)

            if self.appInfo.showMetrics:

                evaluatedText = f"evaluated positions: {self.infoAI.evaluatedPositions}"
                evaluatedLabel = self.sideBarFont.render(evaluatedText, True, WHITE)

                runtimeText = f"runtime: {self.infoAI.runtime}"
                runtimeLabel = self.sideBarFont.render(runtimeText, True, WHITE)

                bestMoveText = f"best move: {self.infoAI.bestMoveSequence}"
                bestMoveLabel = self.sideBarFont.render(bestMoveText, True, WHITE)

                estimationText = f"estimation: {self.infoAI.estimation}"
                estimationLabel = self.sideBarFont.render(estimationText, True, WHITE)

                runText = f"[SPACE] to start/stop analysis"
                runLabel = self.sideBarFont.render(runText, True, WHITE)

                metricsLabels = [
                    self.barLabel,
                    self.blankLabel,
                    evaluatedLabel,
                    runtimeLabel,
                    bestMoveLabel,
                    estimationLabel,
                    runLabel
                ]

                self.drawLabels(metricsLabels, 15)

    def drawAvailableMoves(self):

        for move in self.boardManager.pieceMoves:

            toPos = draughtsToCoords(move[1])

            destX = toPos[0] * tileSize + cursorOffset
            destY = toPos[1] * tileSize + cursorOffset

            if self.boardManager.player == 1:
                pygame.draw.ellipse(self.boardSurface, WHITE, [destX, destY, cursorDiameter, cursorDiameter], 0)
            else:
                pygame.draw.ellipse(self.boardSurface, BLACK, [destX, destY, cursorDiameter, cursorDiameter], 0)

    def rotateIfFlipped(self):
        if self.appInfo.isFlipped:
            self.boardSurface = pygame.transform.rotate(self.boardSurface, 180)

    def combineSurfaces(self):
        self.screen.blit(self.boardSurface, (0, 0))
        self.screen.blit(self.sideBarSurface, (boardSize[0], 0))

    def drawBackground(self):

        # required for refreshing the screen
        self.screen.fill(BLACK)
        self.boardSurface.fill(BLACK)

        pygame.draw.rect(self.boardSurface, DARK_BROWN, [0, 0, boardSize[0], boardSize[1]], 0)
        # draw the checkers board
        for i in range(tilesPerRow * tilesPerRow):
            tileX = (i % tilesPerRow) * tileSize
            tileY = (int(i / tilesPerRow)) * tileSize

            evenRow = (int(i / tilesPerRow)) % 2

            if (evenRow and i % 2 == 1) or (not evenRow and i % 2 == 0):
                pygame.draw.rect(self.boardSurface, LIGHT_BROWN, [tileX, tileY, tileSize, tileSize], 0)

    # draw the pieces
    def drawPieces(self):

        blackPromotionLabel = self.promotionFont.render("K", True, WHITE)
        whitePromotionLabel = self.promotionFont.render("K", True, BLACK)

        # if flipped, rotate so that when you rotate the boardSurface, labels remain readable
        if self.appInfo.isFlipped:
            blackPromotionLabel = pygame.transform.rotate(blackPromotionLabel, 180)
            whitePromotionLabel = pygame.transform.rotate(whitePromotionLabel, 180)

        for y in range(tilesPerRow):
            for x in range(tilesPerRow):

                board_content = self.boardManager.board[y][x]

                # pieces that were captured but remain on the board
                if board_content == -1:
                    pygame.draw.ellipse(self.boardSurface, GREY, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                if board_content == 1 or board_content == 2:
                    pygame.draw.ellipse(self.boardSurface, WHITE, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                    # draw promoted
                    if board_content == 2:
                        self.boardSurface.blit(whitePromotionLabel, (x * tileSize + tileSize / 3, y * tileSize + tileSize / 5))

                elif board_content == 3 or board_content == 4:
                    pygame.draw.ellipse(self.boardSurface, BLACK, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                    # draw promoted
                    if board_content == 4:
                        self.boardSurface.blit(blackPromotionLabel, (x * tileSize + tileSize / 3, y * tileSize + tileSize / 5))

    def drawTileLabels(self):

        counter = 1

        # draw the checkers board
        for i in range(tilesPerRow * tilesPerRow):

            tileX = (i % tilesPerRow) * tileSize
            tileY = (int(i / tilesPerRow)) * tileSize

            evenRow = (int(i / tilesPerRow)) % 2

            if (evenRow and i % 2 == 0) or (not evenRow and i % 2 == 1):

                label = self.numberingFont.render(str(counter), True, WHITE)

                # rotate as well when boardSurface is rotated so that text remains readable
                if self.appInfo.isFlipped:
                    label = pygame.transform.rotate(label, 180)

                counter = counter + 1

                self.boardSurface.blit(label, (tileX, tileY))

    def drawGameOverScreen(self):

        if self.boardManager.isGameOver:
            self.boardSurface.blit(self.overlaySurface, (0, 0))

            if self.boardManager.whoWon == 1:
                hasWonText = "White has won"
            elif self.boardManager.whoWon == 2:
                hasWonText = "Black has won"
            else:
                hasWonText = "It's a draw"

            gameOverLabel = self.gameOverFont.render("Game Over!", True, BLACK)
            hasWonLabel = self.gameOverFont.render(hasWonText, True, BLACK)
            restartLabel = self.restartFont.render("Press [R] to restart", True, BLACK)

            # draw the game over box
            gameOverSurface = pygame.Surface(gameOverSize)
            gameOverSurface.fill(GREY)

            # divide the rect into three vertical segments
            # top for "Game Over!" (40% height)
            gameOverLabelX = (gameOverSize[0] - gameOverLabel.get_width()) / 2
            topHeight = gameOverSize[1] * 0.4

            gameOverLabelY = (topHeight - gameOverLabel.get_height()) / 2

            # mid for "White has won" or "Black has won (40% height)
            hasWonLabelX = (gameOverSize[0] - hasWonLabel.get_width()) / 2
            midHeight = topHeight

            hasWonLabelY = topHeight + (midHeight - hasWonLabel.get_height()) / 2

            # bottom for "R to restart the game" (10% height)
            bottomHeight = gameOverSize[1] * 0.2
            restartLabelX = (gameOverSize[0] - restartLabel.get_width()) / 2

            restartLabelY = topHeight + midHeight + (bottomHeight - restartLabel.get_height()) / 2

            gameOverSurface.blit(gameOverLabel, (gameOverLabelX, gameOverLabelY))
            gameOverSurface.blit(hasWonLabel, (hasWonLabelX, hasWonLabelY))
            gameOverSurface.blit(restartLabel, (restartLabelX, restartLabelY))

            self.boardSurface.blit(gameOverSurface, gameOverOffset)
