
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
