# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws

import tkinter as tk
from tkinter import filedialog

from draughts import Game

from draw_engine import *
from helpers import getPositionOfCapturedPiece, isPromotion, setPieceMoves, getMove, outOfBounds


class App:

    def __init__(self):

        # hide tkinter's root window, only needed for the file dialog prompt
        root = tk.Tk()
        root.withdraw()

        # start pygame, open a new window
        pygame.init()
        self.screen = pygame.display.set_mode(windowSize)
        pygame.display.set_caption("CheckersBot")

        self.isRunning = True
        # triggered when something needs to be redrawn
        self.refreshNeeded = True
        # triggered when pieces have moved, have been captured
        self.gameBoardChanged = True

        # internal representation using pydraughts
        self.game = Game(variant="standard", fen="startpos")

        self.info = {
            # white: 1, black: 2
            "player": 1,
            # stored as indices from 0 to tilesPerRow - 1
            "mousex": 0,
            "mousey": 0,
            "selected": (-1, -1),
            "allMoves": [],
            "pieceMoves": [],
            # to record a capture sequence
            "capturedPieces": [],
            "isPromotion": False,
            "promotedPiece": (-1, -1),
            # to write out game to file
            "moveHistory": [],
            "isFlipped": False
        }

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.board = [row[:] for row in initial_board]

        self.drawEngine = DrawEngine(self.screen, self.board, self.info)

    def resetInfo(self):
        self.info["player"] = 1
        # stored as indices from 0 to tilesPerRow - 1
        self.info["mousex"] = 0
        self.info["mousey"] = 0
        self.info["selected"] = (-1, -1)
        self.info["allMoves"] = []
        self.info["pieceMoves"] = []
        # to record a capture sequence
        self.info["capturedPieces"] = []
        self.info["isPromotion"] = False
        self.info["promotedPiece"] = (-1, -1)
        # to write out game to file
        self.info["moveHistory"] = []

        self.info["isFlipped"] = False

    def makeMove(self, move):

        fromX, fromY = draughtsToCoords(move[0])
        toX, toY = draughtsToCoords(move[1])

        self.board[toY][toX] = self.board[fromY][fromX]
        self.board[fromY][fromX] = 0

        capturedX, capturedY = getPositionOfCapturedPiece(self.board, self.info, move)
        isCapture = (capturedX, capturedY) != (-1, -1)

        if isCapture:
            # set as captured but don't remove piece from board immediately
            self.board[capturedY][capturedX] = -1
            self.info["capturedPieces"].append((capturedX, capturedY))

        # save promotion for end of turn
        self.info["isPromotion"] = self.info["isPromotion"] or isPromotion(self.board, move)

        if self.info["isPromotion"]:
            self.info["promotedPiece"] = (toX, toY)

        self.game.move(move, isCapture)
        self.info["moveHistory"].append(move)

        thisPlayer = self.info["player"]
        nextPlayer = 1 if self.game.whose_turn() == 2 else 2

        # move ends players turn, realize promotions and captures
        if nextPlayer != thisPlayer:

            for (capturedX, capturedY) in self.info["capturedPieces"]:
                self.board[capturedY][capturedX] = 0

            if self.info["isPromotion"]:
                promotedX, promotedY = self.info["promotedPiece"]
                self.board[promotedY][promotedX] += 1

            self.info["capturedPieces"] = []
            self.info["isPromotion"] = False
            self.info["promotedPiece"] = (-1, -1)

        self.info["player"] = nextPlayer

    def writeMovesToFile(self, filename):

        output = ""

        for move in self.info["moveHistory"]:
            output += (str(move[0]) + "," + str(move[1]) + "\n")

        with open(filename, 'w') as f:
            f.write(output)

    def loadBoardFromFile(self, filename):

        file = open(filename, 'r')
        lines = file.readlines()

        self.game = Game(variant="standard", fen="startpos")
        self.board = [row[:] for row in initial_board]

        self.drawEngine.reloadBoard(self.board)
        self.resetInfo()

        for line in lines:
            components = line.split(",")
            draughtsFrom, draughtsTo = int(components[0]), int(components[1])
            self.makeMove([draughtsFrom, draughtsTo])

    def update(self):
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.isRunning = False  # Flag that we are done so we can exit the while loop

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    filepath = filedialog.askopenfilename()

                    # write out moves
                    if filepath is not None and filepath != () and filepath != "":
                        self.writeMovesToFile(filepath)

                elif event.key == pygame.K_l:

                    filepath = filedialog.askopenfilename()
                    # read in moves and replay the game
                    if filepath is not None and filepath != () and filepath != "":
                        self.loadBoardFromFile(filepath)
                        self.refreshNeeded = True
                        self.gameBoardChanged = True

                elif event.key == pygame.K_f:
                    self.info["isFlipped"] = True if not self.info["isFlipped"] else False
                    self.refreshNeeded = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                [mouseX, mouseY] = pygame.mouse.get_pos()

                # convert mousePosition to tilePosition
                tileX = int(mouseX / tileSize)
                tileY = int(mouseY / tileSize)

                # if flipped, translation is needed
                if self.info["isFlipped"]:
                    tileX = (tilesPerRow - 1) - tileX
                    tileY = (tilesPerRow - 1) - tileY

                # prevent that a click outside of the game window leads to an out of bounds exception
                if not outOfBounds(tileX, tileY):

                    self.info["mousex"] = tileX
                    self.info["mousey"] = tileY

                    if self.info["player"] == 1 and self.board[tileY][tileX] == 1 or self.board[tileY][tileX] == 2:
                        self.info["selected"] = (tileX, tileY)
                        setPieceMoves(self.info)

                    elif self.info["player"] == 2 and self.board[tileY][tileX] == 3 or self.board[tileY][tileX] == 4:
                        self.info["selected"] = (tileX, tileY)
                        setPieceMoves(self.info)

                    # TODO: make a valid move to the empty square
                    elif self.board[tileY][tileX] == 0:

                        move = getMove(self.info, tileX, tileY)

                        if move is not None:
                            self.makeMove(move)
                            self.gameBoardChanged = True

                    self.refreshNeeded = True

    def draw(self):
        # --- Drawing code should go here
        self.drawEngine.drawBackground()

        self.drawEngine.drawPieces()

        self.drawEngine.drawAvailableMoves()

        self.drawEngine.drawTileLabels()

        self.drawEngine.rotateIfFlipped()

        self.drawEngine.drawSidebar()

        self.drawEngine.combineSurfaces()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def run(self):

        while self.isRunning:

            self.update()

            if self.gameBoardChanged:
                self.info["allMoves"] = self.game.get_possible_moves()
                self.info["pieceMoves"] = []
                self.gameBoardChanged = False

            if self.refreshNeeded:
                self.draw()
                self.refreshNeeded = False

            # --- Limit to 60 frames per second
            self.clock.tick(60)

        # Once we have exited the main program loop we can stop the game engine:
        pygame.quit()
