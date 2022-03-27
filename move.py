
class Move:

    # fromPos = [x, y]

    def __init__(self, board, player, fromPos, toPos):

        self.player = player
        self.fromPos = fromPos
        self.toPos = toPos

        fromX, fromY = self.fromPos
        toX, toY = self.toPos

        self.isCapture = abs(toX - fromX) > 1

        if player == 1:
            self.isPromotion = board[fromY][fromX] == 1 and toY == 0
        else:
            self.isPromotion = board[fromY][fromX] == 3 and toY == 7

    def __str__(self):
        return f"({self.fromPos}) -> ({self.toPos})"
