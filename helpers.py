
# works
from constants import tilesPerRow

def outOfBounds(x,y):
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
def coordsToDraughts(x,y):
    offsetTroughRow = y * 5
    offsetThroughCol = -1

    if y % 2 == 0:
        offsetThroughCol = int((x + 1) / 2)
    else:
        offsetThroughCol = int(x / 2) + 1

    return offsetTroughRow + offsetThroughCol

def setPieceMoves(info):
    x, y = info["selected"]
    fromPos = coordsToDraughts(x, y)
    pieceMoves = []

    for move in info["allMoves"]:

        fromPosMove, toPosMove = move

        if fromPos == fromPosMove:
            pieceMoves.append(move)

    info["pieceMoves"] = pieceMoves


def getMove(info, toX, toY):
    toPos = coordsToDraughts(toX, toY)

    for move in info["pieceMoves"]:
        if move[1] == toPos:
            return move
    return None


def getPositionOfCapturedPiece(board, info, move):
    fromX, fromY = draughtsToCoords(move[0])
    toX, toY = draughtsToCoords(move[1])

    dirX = 1 if (toX - fromX) > 0 else -1
    dirY = 1 if (toY - fromY) > 0 else -1

    probX = fromX
    probY = fromY

    # walk along the diagonal
    while probX != toX and probY != toY:

        if (info["player"] == 1 and board[probY][probX] > 2) or (info["player"] == 2 and 1 <= board[probY][probX] <= 2):
            return probX, probY

        probX += dirX
        probY += dirY

    return -1, -1


def isPromotion(board, move):
    fromX, fromY = draughtsToCoords(move[0])
    toX, toY = draughtsToCoords(move[1])

    return (board[fromY][fromX] == 1 and toY == 0) or (board[fromY][fromX] == 3 and toY == (tilesPerRow - 1))
