
class FileManager:

    def __init__(self, boardManager):

        self.boardManager = boardManager

    def writeMovesToFile(self, filename):

        output = ""

        for move in self.boardManager.moveHistory:
            output += (str(move[0]) + "," + str(move[1]) + "\n")

        with open(filename, 'w') as f:
            f.write(output)

    def loadBoardFromFile(self, filename):

        file = open(filename, 'r')
        lines = file.readlines()

        self.boardManager.reset()

        for line in lines:
            components = line.split(",")
            draughtsFrom, draughtsTo = int(components[0]), int(components[1])
            self.boardManager.makeMove([draughtsFrom, draughtsTo])
