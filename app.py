# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws

import tkinter as tk
from tkinter import filedialog

import pygame
from draughts import Game, WHITE as WHITE_PLAYER

from ai_engine import AIEngine
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
            "blackPiecesCaptured": 0,
            "whitePiecesCaptured": 0,
            "selected": (-1, -1),
            "allMoves": [],
            "pieceMoves": [],
            # to record a capture sequence
            "capturedPieces": [],
            "isPromotion": False,
            # to write out game to file
            "moveHistory": [],
            "isFlipped": False,

            "isGameOver": False,
            # 1 => player 1 won, 2 => player 2 won, 0 => draw, -1 => invalid entry
            "whoWon": -1,

            "analysisModeOn": False,
            "analysisRunning": False
        }

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.board = [row[:] for row in initial_board]

        self.aiEngine = AIEngine()
        # call explicitly so call doesn't get optimized away
        self.aiEngine.__int__()

        self.drawEngine = DrawEngine(self)

    def resetBoard(self):
        for y in range(tilesPerRow):
            for x in range(tilesPerRow):
                self.board[y][x] = initial_board[y][x]

    def resetGame(self):
        self.game = Game(variant="standard", fen="startpos")

    def resetInfo(self):
        self.info["player"] = 1
        # stored as indices from 0 to tilesPerRow - 1
        self.info["mousex"] = 0
        self.info["mousey"] = 0
        self.info["blackPiecesCaptured"] = 0
        self.info["whitePiecesCaptured"] = 0
        self.info["selected"] = (-1, -1)
        self.info["allMoves"] = []
        self.info["pieceMoves"] = []
        # to record a capture sequence
        self.info["capturedPieces"] = []
        self.info["isPromotion"] = False
        # to write out game to file
        self.info["moveHistory"] = []

        self.info["isFlipped"] = False
        self.info["isGameOver"] = False
        self.info["whoWon"] = -1
        self.info["analysisModeOn"] = False
        self.info["analysisRunning"] = False

    def setGameStatus(self):
        self.info["isGameOver"] = self.game.is_over()

        if self.info["isGameOver"]:
            if self.game.is_draw() or self.game.is_threefold():
                self.info["whoWon"] = 0
            else:
                self.info["whoWon"] = 1 if self.game.has_player_won(WHITE_PLAYER) else 2

    def makeMove(self, move):

        # use (now) old board position to determine if a promotion occurred
        # promotion moves are last moves, nothing happens when you get to the promotion square and jump away afterwards
        self.info["isPromotion"] = isPromotion(self.board, move)

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

            if self.info["player"] == 1:
                self.info["blackPiecesCaptured"] += 1
            else:
                self.info["whitePiecesCaptured"] += 1

        self.game.move(move, isCapture)

        self.info["moveHistory"].append(move)

        thisPlayer = self.info["player"]
        nextPlayer = 1 if self.game.whose_turn() == 2 else 2

        # move ends players turn, realize promotions and captures
        if nextPlayer != thisPlayer:

            for (capturedX, capturedY) in self.info["capturedPieces"]:
                self.board[capturedY][capturedX] = 0

            if self.info["isPromotion"]:
                self.board[toY][toX] += 1

            self.info["capturedPieces"] = []
            self.info["isPromotion"] = False

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

        self.resetGame()
        self.resetBoard()
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

                elif event.key == pygame.K_f and not self.info["isGameOver"]:
                    self.info["isFlipped"] = True if not self.info["isFlipped"] else False
                    self.refreshNeeded = True

                elif event.key == pygame.K_r:
                    self.resetGame()
                    self.resetBoard()
                    self.resetInfo()

                    self.gameBoardChanged = True
                    self.refreshNeeded = True

                # you can't quit the analysis mode while it's running
                elif event.key == pygame.K_a and not self.info["analysisRunning"]:
                    self.info["analysisModeOn"] = True if not self.info["analysisModeOn"] else False

                    self.refreshNeeded = True

                elif self.info["analysisModeOn"]:
                    # you can't change the parameters while the analysis is being performed
                    if not self.info["analysisRunning"]:
                        if event.key == pygame.K_PLUS:
                            self.aiEngine.infoAI["searchDepth"] += 1
                            self.refreshNeeded = True
                        elif event.key == pygame.K_MINUS:
                            self.aiEngine.infoAI["searchDepth"] -= 1 if self.aiEngine.infoAI["searchDepth"] > 1 else 0
                            self.refreshNeeded = True
                        elif event.key == pygame.K_1:
                            self.aiEngine.infoAI["alphaBetaOn"] = not self.aiEngine.infoAI["alphaBetaOn"]
                            self.refreshNeeded = True
                        elif event.key == pygame.K_2:
                            self.aiEngine.infoAI["moveSortingOn"] = not self.aiEngine.infoAI["moveSortingOn"]
                            self.refreshNeeded = True
                        elif event.key == pygame.K_RETURN:
                            self.info["analysisRunning"] = True
                            self.refreshNeeded = True
                    else:
                        # TODO: properly stop the analysis so that its output stays on screen
                        if event.key == pygame.K_RETURN:
                            self.info["analysisRunning"] = False
                            self.refreshNeeded = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.info["isGameOver"]:
                [mouseX, mouseY] = pygame.mouse.get_pos()

                # convert mousePosition to tilePosition
                tileX = int(mouseX / tileSize)
                tileY = int(mouseY / tileSize)

                # if flipped, translation is needed
                if self.info["isFlipped"]:
                    tileX = (tilesPerRow - 1) - tileX
                    tileY = (tilesPerRow - 1) - tileY

                # prevent that a click outside the game window leads to an out-of-bounds exception
                if not outOfBounds(tileX, tileY):

                    self.info["mousex"] = tileX
                    self.info["mousey"] = tileY

                    if self.info["player"] == 1 and self.board[tileY][tileX] == 1 or self.board[tileY][tileX] == 2:
                        self.info["selected"] = (tileX, tileY)
                        setPieceMoves(self.info)

                    elif self.info["player"] == 2 and self.board[tileY][tileX] == 3 or self.board[tileY][tileX] == 4:
                        self.info["selected"] = (tileX, tileY)
                        setPieceMoves(self.info)

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

        self.drawEngine.drawGameOverScreen()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def run(self):

        while self.isRunning:

            self.update()

            if self.gameBoardChanged:

                # check if game is over and if so, draw game over menu
                self.setGameStatus()

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
