import pygame

from constants import *
from helpers import draughtsToCoords

class DrawEngine:

    def __init__(self, screen, board):

        self.screen = screen
        self.board = board

        self.sideBarFont = pygame.font.SysFont("monospace", sideBarFontSize)
        self.numberingFont = pygame.font.SysFont("monospace", numberingFontSize)
        self.promotionFont = pygame.font.SysFont("monospace", promotionFontSize)

    def reloadBoard(self, board):
        self.board = board

    def drawSidebar(self, info):
        # Sidebar has dimensions 400 x 800 and is positioned at 800, 0
        # padding is 5, 5
        offsetX, offsetY = [boardSize[0] + 5, 5]

        playerText = "player: " + ("white" if info["player"] == 1 else "black")
        playerLabel = self.sideBarFont.render(playerText, 1, WHITE)

        mouseText = f"mouse: x = {info['mousex']}, y = {info['mousey']}"
        mouseLabel = self.sideBarFont.render(mouseText, 1, WHITE)

        loadStoreText = "load [L], store [S]"
        loadStoreLabel = self.sideBarFont.render(loadStoreText, 1, WHITE)

        flipAnalyzeText = "flip [F], analyze [A]"
        flipAnalyzeLabel = self.sideBarFont.render(flipAnalyzeText, 1, WHITE)

        pygame.draw.rect(self.screen, BLACK, [boardSize[0] + 5, 5, windowSize[0] - boardSize[0], windowSize[1] - boardSize[1]], 0)
        self.screen.blit(playerLabel, (offsetX, offsetY))
        self.screen.blit(mouseLabel, (offsetX, offsetY + 1 * lineHeight))
        self.screen.blit(loadStoreLabel, (offsetX, offsetY + 3 * lineHeight))
        self.screen.blit(flipAnalyzeLabel, (offsetX, offsetY + 4 * lineHeight))

    def drawAvailableMoves(self, player, moves):

        for move in moves:

            toPos = draughtsToCoords(move[1])

            destX = toPos[0] * tileSize + cursorOffset
            destY = toPos[1] * tileSize + cursorOffset

            # chess lib starts with player 2 so translation is needed
            if player == 2:
                pygame.draw.ellipse(self.screen, WHITE, [destX, destY, cursorDiameter, cursorDiameter], 0)
            else:
                pygame.draw.ellipse(self.screen, BLACK, [destX, destY, cursorDiameter, cursorDiameter], 0)

    def drawBackground(self):

        # required for refreshing the screen
        self.screen.fill(BLACK)

        pygame.draw.rect(self.screen, DARK_BROWN, [0, 0, boardSize[0], boardSize[1]], 0)
        # draw the checkers board
        for i in range(tilesPerRow * tilesPerRow):
            tileX = (i % tilesPerRow) * tileSize
            tileY = (int(i / tilesPerRow)) * tileSize

            evenRow = (int(i / tilesPerRow)) % 2

            if (evenRow and i % 2 == 1) or (not evenRow and i % 2 == 0):
                pygame.draw.rect(self.screen, LIGHT_BROWN, [tileX, tileY, tileSize, tileSize], 0)

    # draw the pieces
    def drawPieces(self):

        blackPromotionLabel = self.promotionFont.render("K", 1, WHITE)
        whitePromotionLabel = self.promotionFont.render("K", 1, BLACK)

        for y in range(tilesPerRow):
            for x in range(tilesPerRow):

                board_content = self.board[y][x]

                # draw inner and outer ellipse to visualize the checker piece
                tileOffset = 5

                # pieces that were captured but remain on the board
                if board_content == -1:
                    pygame.draw.ellipse(self.screen, GREY, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                if board_content == 1 or board_content == 2:
                    pygame.draw.ellipse(self.screen, WHITE, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                    # draw promoted
                    if board_content == 2:
                        self.screen.blit(whitePromotionLabel, (x * tileSize + tileSize / 3, y * tileSize + tileSize / 5))

                elif board_content == 3 or board_content == 4:
                    pygame.draw.ellipse(self.screen, BLACK, [x * tileSize + pieceOffset, y * tileSize + pieceOffset, pieceSize, pieceSize], 0)

                    # draw promoted
                    if board_content == 4:
                        self.screen.blit(blackPromotionLabel, (x * tileSize + tileSize / 3, y * tileSize + tileSize / 5))

    def drawTileLabels(self):

        counter = 1

        # draw the checkers board
        for i in range(tilesPerRow * tilesPerRow):

            tileX = (i % tilesPerRow) * tileSize
            tileY = (int(i / tilesPerRow)) * tileSize

            evenRow = (int(i / tilesPerRow)) % 2

            if (evenRow and i % 2 == 0) or (not evenRow and i % 2 == 1):

                label = self.numberingFont.render(str(counter), True, WHITE)
                counter = counter + 1

                self.screen.blit(label, (tileX, tileY))

