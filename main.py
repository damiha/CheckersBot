
# Import the pygame library and initialise the game engine
import pygame

from constants import *
from draw import *
from engine import Engine
from move import Move

pygame.init()

# Open a new window
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("CheckersBOT")

# Define side bar font
sideBarFont = pygame.font.SysFont("monospace", sideBarFontSize)
promotionFont = pygame.font.SysFont("monospace", promotionFontSize)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
isRunning = True
refreshNeeded = True
gameBoardChanged = True

# player = 1 => RED
# player = 2 => WHITE

info = {
    "player": 1,
    "mousex": 0,
    "mousey": 0,
    "selected": (-1, -1),
    "allMoves": [],
    "pieceMoves": []
}

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# define initial game step (white on top, red on bottom)
# 0 = empty
# 1 = white (normal)
# 2 = white (king)
# 3 = red (normal)
# 4 = red (king)

board = [
    [0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

engine = Engine()


def filterMoves():

    pieceMoves = []

    for move in info["allMoves"]:

        if move.fromPos == info["selected"]:
            pieceMoves.append(move)

    return pieceMoves


def makeMove(board, move):

    # non capture
    fromX, fromY = move.fromPos
    toX, toY = move.toPos

    if not move.isCapture:
        board[toY][toX] = board[fromY][fromX]
        board[fromY][fromX] = 0

    # capture
    else:
        board[toY][toX] = board[fromY][fromX]
        board[fromY][fromX] = 0

        capturedX = int((fromX + toX) / 2)
        capturedY = int((fromY + toY) / 2)

        board[capturedY][capturedX] = 0

    # check promotion after non capture or capture have been processed
    if move.isPromotion:
        board[toY][toX] = board[toY][toX] + 1

    # promotions and non captures are the only way so that the other player gets his turn
    if move.isPromotion or not move.isCapture:
        info["player"] = 2 if info["player"] == 1 else 1


# -------- Main Program Loop -----------
while isRunning:

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            isRunning = False  # Flag that we are done so we can exit the while loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            [mouseX, mouseY] = pygame.mouse.get_pos()
            info["mousex"] = mouseX
            info["mousey"] = mouseY

            # convert mousePosition to tilePosition
            tileX = int(mouseX / tileSize)
            tileY = int(mouseY / tileSize)

            if info["player"] == 1 and board[tileY][tileX] == 1 or board[tileY][tileX] == 2:
                info["selected"] = (tileX, tileY)
                info["pieceMoves"] = filterMoves()

            elif info["player"] == 2 and board[tileY][tileX] == 3 or board[tileY][tileX] == 4:
                info["selected"] = (tileX, tileY)
                info["pieceMoves"] = filterMoves()

            elif board[tileY][tileX] == 0:
                for move in info["allMoves"]:
                    if move.fromPos == info["selected"] and move.toPos == (tileX, tileY):
                        makeMove(board, move)
                        gameBoardChanged = True

            refreshNeeded = True

    if gameBoardChanged:
        info["allMoves"] = engine.showValidMoves(board, info["player"])
        info["pieceMoves"] = []
        gameBoardChanged = False

    if refreshNeeded:
        # --- Drawing code should go here
        drawBackground(screen, board)

        drawPieces(screen, board)

        drawAvailableMoves(screen, info["pieceMoves"])

        drawSidebar(screen, sideBarFont, info)

        refreshNeeded = False

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
