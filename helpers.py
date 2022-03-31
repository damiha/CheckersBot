
# works
from constants import tilesPerRow


def outOfBounds(x, y):
    return x < 0 or y < 0 or x >= tilesPerRow or y >= tilesPerRow


def draughtsToCoords(tileNumber):
    y = int((tileNumber - 1) / 5)
    x = -1

    if y % 2 == 1:
        x = 2 * ((tileNumber - 1) % 5)
    else:
        x = 2 * ((tileNumber - 1) % 5) + 1

    return x, y


# works
def coordsToDraughts(x, y):
    offsetTroughRow = y * 5
    offsetThroughCol = -1

    if y % 2 == 0:
        offsetThroughCol = int((x + 1) / 2)
    else:
        offsetThroughCol = int(x / 2) + 1

    return offsetTroughRow + offsetThroughCol


# FEN of starting position
# B:W29,31,32,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50:B1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
# doesn't work when 0 pieces on board, but staticEvaluation() handles this case
def getBlackPiecesFromFEN(fenString):

    colStrings = fenString.split(":")
    blackFenString = colStrings[2]

    return len(blackFenString.split(","))


def getWhitePiecesFromFEN(fenString):
    colStrings = fenString.split(":")
    whiteFenString = colStrings[1]

    return len(whiteFenString.split(","))


def flatten(t):
    return [item for sublist in t for item in sublist]
