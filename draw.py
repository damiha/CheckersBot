
import pygame

from constants import *
from main import sideBarFont, promotionFont


def drawSidebar(screen, font, info):
    # Sidebar has dimensions 400 x 800 and is positioned at 800, 0
    # padding is 5, 5
    offsetX, offsetY = [805, 5]

    playerText = "player: " + ("red" if info["player"] == 1 else "white")
    playerLabel = sideBarFont.render(playerText, 1, WHITE)

    mouseText = f"mouse: x = {info['mousex']}, y = {info['mousey']}"
    mouseLabel = font.render(mouseText, 1, WHITE)

    screen.blit(playerLabel, (offsetX, offsetY))
    screen.blit(mouseLabel, (offsetX, offsetY + 1 * lineHeight))


def drawAvailableMoves(screen, moves):

    for move in moves:

        destX = move.toPos[0] * tileSize + cursorOffset
        destY = move.toPos[1] * tileSize + cursorOffset

        if move.player == 1:
            pygame.draw.ellipse(screen, RED, [destX, destY, cursorDiameter, cursorDiameter], 0)
        else:
            pygame.draw.ellipse(screen, WHITE, [destX, destY, cursorDiameter, cursorDiameter], 0)


def drawBackground(screen, board):

    screen.fill(BLACK)
    # draw the checkers board
    for i in range(81):
        tileX = (i % 8) * tileSize
        tileY = (int(i / 8)) * tileSize

        evenRow = (int(i / 8)) % 2

        if (evenRow and i % 2 == 1) or (not evenRow and i % 2 == 0):
            pygame.draw.rect(screen, WHITE, [tileX, tileY, tileSize, tileSize], 0)


# draw the pieces
def drawPieces(screen, board):

    redPromotionLabel = promotionFont.render("K", 1, DARK_RED)
    whitePromotionLabel = promotionFont.render("K", 1, LIGHT_GREY)

    for y in range(8):
        for x in range(8):

            board_content = board[y][x]

            # draw inner and outer ellipse to visualize the checker piece
            tileOffset = 5

            if board_content == 1 or board_content == 2:
                pygame.draw.ellipse(screen, RED, [x * tileSize, y * tileSize, tileSize, tileSize], 0)
                pygame.draw.ellipse(screen, DARK_RED, [x * tileSize + tileOffset, y * tileSize + tileOffset,
                                                       tileSize - 2 * tileOffset, tileSize - 2 * tileOffset], 0)

                # draw promoted
                if board_content == 2:
                    pass

            elif board_content == 3 or board_content == 4:
                pygame.draw.ellipse(screen, WHITE, [x * tileSize, y * tileSize, tileSize, tileSize], 0)
                pygame.draw.ellipse(screen, LIGHT_GREY, [x * tileSize + tileOffset, y * tileSize + tileOffset,
                                                         tileSize - 2 * tileOffset, tileSize - 2 * tileOffset], 0)
