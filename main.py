
# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws
from draughts import Game, Move, WHITE, BLACK
from draw_engine import *
from helpers import coordsToDraughts

pygame.init()

# Open a new window
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("CheckersBOT")

# The loop will carry on until the user exits the game (e.g. clicks the close button).
isRunning = True
refreshNeeded = True
gameBoardChanged = True

# player = 1 => WHITE
# player = 2 => BLACK

# WHITE BEGINS
game = Game(variant="standard", fen="startpos")

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
# 3 = black (normal)
# 4 = normal (king)

board = [
    [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
]

def setPieceMoves():

    x, y = info["selected"]
    fromPos = coordsToDraughts(x, y)
    pieceMoves = []

    for move in info["allMoves"]:

        fromPosMove, toPosMove = move

        if fromPos == fromPosMove:
            pieceMoves.append(move)

    info["pieceMoves"] = pieceMoves

def makeMove():
    pass



drawEngine = DrawEngine(screen, board)

# -------- Main Program Loop -----------
while isRunning:

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            isRunning = False  # Flag that we are done so we can exit the while loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            [mouseX, mouseY] = pygame.mouse.get_pos()

            # convert mousePosition to tilePosition
            tileX = int(mouseX / tileSize)
            tileY = int(mouseY / tileSize)

            info["mousex"] = tileX
            info["mousey"] = tileY

            if info["player"] == 1 and board[tileY][tileX] == 1 or board[tileY][tileX] == 2:
                info["selected"] = (tileX, tileY)
                setPieceMoves()

            elif info["player"] == 2 and board[tileY][tileX] == 3 or board[tileY][tileX] == 4:
                info["selected"] = (tileX, tileY)
                setPieceMoves()

            # TODO: make a valid move to the empty square
            elif board[tileY][tileX] == 0:
                pass

            refreshNeeded = True

    if gameBoardChanged:
        # TODO: calculate all valid moves using pydraughts
        info["allMoves"] = game.get_possible_moves()
        info["pieceMoves"] = []
        gameBoardChanged = False

    if refreshNeeded:
        # --- Drawing code should go here
        drawEngine.drawBackground()

        drawEngine.drawPieces()

        drawEngine.drawTileLabels()

        drawEngine.drawAvailableMoves(game.whose_turn(), info["pieceMoves"])

        drawEngine.drawSidebar(info)

        refreshNeeded = False

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
