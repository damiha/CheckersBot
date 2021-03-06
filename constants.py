
# Define some colors
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

LIGHT_BROWN = (255, 230, 170)
DARK_BROWN = (120, 70, 40)

OVERLAY_ALPHA = 192

# Define some sizes
windowSize = (1200, 800)
boardSize = (800, 800)

gameOverSize = (480, 320)
gameOverOffset = ((boardSize[0] - gameOverSize[0]) / 2, (boardSize[1] - gameOverSize[1]) / 2)

tilesPerRow = 10
tileSize = boardSize[0] / tilesPerRow

pieceSize = tileSize * 0.75
pieceOffset = (tileSize - pieceSize) / 2

numberingFontSize = 16
sideBarFontSize = 16
restartFontSize = 24
promotionFontSize = 40
gameOverFontSize = 56

barLength = 40

# measured in pixels
lineHeight = 20

cursorDiameter = 25
cursorOffset = (tileSize - cursorDiameter) / 2

# define initial game step (white on the bottom, black on top)
# 0 = empty
# 1 = white (normal)
# 2 = white (king)
# 3 = black (normal)
# 4 = black (king)

initial_board = [
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

# 0.05 = 50ms
# when analysis is running
refreshTime = 0.05

# weights for heuristic function
valuePerMan = 1.0
valuePerKing = 5.0

# board is divided into five rings (2x2 center is ring 1 etc)
# center ring: +1 for each piece, second ring: 0.8

lossPerRing = 0.2

# center of board to calculate manhatten distance
boardCenter = 4.5
