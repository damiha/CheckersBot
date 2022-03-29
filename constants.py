
# Define some colors
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

LIGHT_BROWN = (255, 230, 170)
DARK_BROWN = (80, 50, 0)

# Define some sizes
windowSize = (1200, 800)
boardSize = (800, 800)

tilesPerRow = 10
tileSize = boardSize[0] / tilesPerRow

pieceSize = tileSize * 0.75
pieceOffset = (tileSize - pieceSize) / 2

numberingFontSize = 16
sideBarFontSize = 16
promotionFontSize = 40

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
