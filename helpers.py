
# works
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
