import pygame

from constants import *
from helpers import draughtsToCoords

class DrawEngine:

    def __init__(self, screen, board, info):

        self.screen = screen
        self.board = board
        self.info = info

        # draw everything game related on to here to rotate easily (if whole screen is rotated, then sidebar is as well)
        self.boardSurface = pygame.Surface(boardSize)
        self.sideBarSurface = pygame.Surface((windowSize[0] - boardSize[0], boardSize[1]))

        self.sideBarFont = pygame.font.SysFont("monospace", sideBarFontSize)
        self.numberingFont = pygame.font.SysFont("monospace", numberingFontSize)
        self.promotionFont = pygame.font.SysFont("monospace", promotionFontSize)

    def reloadBoard(self, board):
        self.board = board

    def drawSidebar(self):
        # Sidebar has dimensions 400 x 800 and is positioned at 800, 0
        # padding is 5, 5
        offsetX, offsetY = (5, 5)

        playerText = "player: " + ("white" if self.info["player"] == 1 else "black")
        playerLabel = self.sideBarFont.render(playerText, 1, WHITE)

        mouseText = f"mouse: x = {self.info['mousex']}, y = {self.info['mousey']}"
        mouseLabel = self.sideBarFont.render(mouseText, 1, WHITE)

        loadStoreText = "load [L], store [S]"
        loadStoreLabel = self.sideBarFont.render(loadStoreText, 1, WHITE)

        flipAnalyzeText = "flip [F], analyze [A]"
        flipAnalyzeLabel = self.sideBarFont.render(flipAnalyzeText, 1, WHITE)

        self.sideBarSurface.fill(BLACK)
        self.sideBarSurface.blit(playerLabel, (offsetX, offsetY))
        self.sideBarSurface.blit(mouseLabel, (offsetX, offsetY + 1 * lineHeight))
        self.sideBarSurface.blit(loadStoreLabel, (offsetX, offsetY + 3 * lineHeight))
        self.sideBarSurface.blit(flipAnalyzeLabel, (offsetX, offsetY + 4 * lineHeight))

    def drawAvailableMoves(self):

        for move in self.info["pieceMoves"]:

            toPos = draughtsToCoords(move[1])

            destX = toPos[0] * tileSize + cursorOffset
            destY = toPos[1] * tileSize + cursorOffset

            if self.info["player"] == 1:
                pygame.draw.ellipse(self.boardSurface, WHITE, [destX, destY, cursorDiameter, cursorDiameter], 0)
            else:
                pygame.draw.ellipse(self.boardSurface, BLACK, [destX, destY, cursorDiameter, cursorDiameter], 0)

    def rotateIfFlipped(self):
        if self.info["isFlipped"]:
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

        blackPromotionLabel = self.promotionFont.render("K", 1, WHITE)
        whitePromotionLabel = self.promotionFont.render("K", 1, BLACK)

        # if flipped, rotate so that when you rotate the boardSurface, labels remain readable
        if self.info["isFlipped"]:
            blackPromotionLabel = pygame.transform.rotate(blackPromotionLabel, 180)
            whitePromotionLabel = pygame.transform.rotate(whitePromotionLabel, 180)

        for y in range(tilesPerRow):
            for x in range(tilesPerRow):

                board_content = self.board[y][x]

                # draw inner and outer ellipse to visualize the checker piece
                tileOffset = 5

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
                if self.info["isFlipped"]:
                    label = pygame.transform.rotate(label, 180)

                counter = counter + 1

                self.boardSurface.blit(label, (tileX, tileY))

