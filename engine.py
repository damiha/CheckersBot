from move import Move


class Engine:

    def outOfBounds(self, x, y):
        return x < 0 or y < 0 or x >= 8 or y >= 8

    def calculateForwardSteps(self, board, player):

        forwardSteps = []

        for y in range(8):
            for x in range(8):

                # red moves "up"
                if player == 1 and (board[y][x] == 1 or board[y][x] == 2):

                    nextX = x - 1
                    nextY = y - 1

                    # add left
                    if not self.outOfBounds(nextX, nextY) and board[nextY][nextX] == 0:
                        forwardSteps.append(Move(board, player, (x, y), (nextX, nextY)))

                    nextX = x + 1
                    nextY = y - 1

                    # add right
                    if not self.outOfBounds(nextX, nextY) and board[nextY][nextX] == 0:

                        forwardSteps.append(Move(board, player, (x, y), (nextX, nextY)))

                # white moves "down"
                elif player == 2 and (board[y][x] == 3 or board[y][x] == 4):

                    nextX = x - 1
                    nextY = y + 1

                    # add left
                    if not self.outOfBounds(nextX, nextY) and board[nextY][nextX] == 0:
                        forwardSteps.append(Move(board, player, (x, y), (nextX, nextY)))

                    nextX = x + 1
                    nextY = y + 1

                    # add right
                    if not self.outOfBounds(nextX, nextY) and board[nextY][nextX] == 0:
                        forwardSteps.append(Move(board, player, (x, y), (nextX, nextY)))

        return forwardSteps

    def calculateForwardCaptures(self, board, player):

        forwardCaptures = []

        for y in range(8):
            for x in range(8):

                # white moves "down"
                if player == 2 and (board[y][x] == 3 or board[y][x] == 4):

                    # capture left
                    nextX = x - 1
                    nextY = y + 1

                    destX = nextX - 1
                    destY = nextY + 1

                    if not self.outOfBounds(nextX, nextY) and (board[nextY][nextX] == 1 or board[nextY][nextX] == 2) \
                            and not self.outOfBounds(destX, destY) and board[destY][destX] == 0:
                        forwardCaptures.append(Move(board, player, (x, y), (destX, destY)))

                    # capture right
                    nextX = x + 1
                    nextY = y + 1

                    destX = nextX + 1
                    destY = nextY + 1

                    if not self.outOfBounds(nextX, nextY) and (board[nextY][nextX] == 1 or board[nextY][nextX] == 2) \
                            and not self.outOfBounds(destX, destY) and board[destY][destX] == 0:
                        forwardCaptures.append(Move(board, player, (x, y), (destX, destY)))

                # red moves "up"
                elif player == 1 and (board[y][x] == 1 or board[y][x] == 2):

                    # capture left
                    nextX = x - 1
                    nextY = y - 1

                    destX = nextX - 1
                    destY = nextY - 1

                    if not self.outOfBounds(nextX, nextY) and (board[nextY][nextX] == 3 or board[nextY][nextX] == 4) \
                            and not self.outOfBounds(destX, destY) and board[destY][destX] == 0:
                        forwardCaptures.append(Move(board, player, (x, y), (destX, destY)))

                    # capture right
                    nextX = x + 1
                    nextY = y - 1

                    destX = nextX + 1
                    destY = nextY - 1

                    if not self.outOfBounds(nextX, nextY) and (board[nextY][nextX] == 3 or board[nextY][nextX] == 4) \
                            and not self.outOfBounds(destX, destY) and board[destY][destX] == 0:
                        forwardCaptures.append(Move(board, player, (x, y), (destX, destY)))

        return forwardCaptures

    # player = 1 => white
    # player = 2 => red
    def showValidMoves(self, board, player):

        forwardSteps = self.calculateForwardSteps(board, player)
        forwardCaptures = self.calculateForwardCaptures(board, player)

        return [*forwardSteps, *forwardCaptures]




