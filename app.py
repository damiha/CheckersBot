# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws

import tkinter as tk
from tkinter import filedialog

import pygame
from draughts import Game, WHITE as WHITE_PLAYER

from ai_engine import AIEngine
from board_manager import BoardManager
from draw_engine import *
from helpers import outOfBounds

import time
import threading


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
        self.boardRefreshNeeded = True
        self.sideBarRefreshNeeded = True
        # triggered when pieces have moved, have been captured
        self.gameBoardChanged = True

        self.boardManager = BoardManager()

        self.info = {
            # stored as indices from 0 to tilesPerRow - 1
            "mousex": 0,
            "mousey": 0,

            "isFlipped": False,
            "analysisModeOn": False,
            "showMetrics": False,
            "analysisRunning": False
        }

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.aiEngine = AIEngine()
        # call explicitly so call doesn't get optimized away
        self.aiEngine.__int__(self.info)

        self.drawEngine = DrawEngine(self)

        # threads
        self.refreshThread = None
        self.timerThread = None
        self.minimaxThread = None

    def resetInfo(self):

        # stored as indices from 0 to tilesPerRow - 1
        self.info["mousex"] = 0
        self.info["mousey"] = 0

        self.info["isFlipped"] = False
        self.info["analysisModeOn"] = False
        self.info["showMetrics"] = False
        self.info["analysisRunning"] = False

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

    def update(self):
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.isRunning = False  # Flag that we are done so we can exit the while loop

                if self.info["analysisRunning"]:

                    self.info["analysisRunning"] = False
                    # closing window should also close the threads
                    self.minimaxThread.join()
                    self.timerThread.join()
                    self.refreshThread.join()

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

                        self.boardRefreshNeeded = True
                        self.sideBarRefreshNeeded = True
                        self.gameBoardChanged = True

                elif event.key == pygame.K_f and not self.boardManager.isGameOver:

                    self.info["isFlipped"] = not self.info["isFlipped"]
                    self.boardRefreshNeeded = True

                elif event.key == pygame.K_r:

                    self.boardManager.reset()

                    self.gameBoardChanged = True
                    self.boardRefreshNeeded = True

                # you can't quit the analysis mode while it's about to run
                elif event.key == pygame.K_a and not self.info["showMetrics"]:

                    self.info["analysisModeOn"] = not self.info["analysisModeOn"]
                    self.sideBarRefreshNeeded = True

                elif self.info["analysisModeOn"]:
                    # you can't change the parameters when the analysis is about to run
                    if not self.info["showMetrics"]:
                        if event.key == pygame.K_PLUS:
                            self.aiEngine.infoAI["searchDepth"] += 1
                            self.sideBarRefreshNeeded = True
                        elif event.key == pygame.K_MINUS:
                            self.aiEngine.infoAI["searchDepth"] -= 1 if self.aiEngine.infoAI["searchDepth"] > 1 else 0
                            self.sideBarRefreshNeeded = True
                        elif event.key == pygame.K_1:
                            self.aiEngine.infoAI["alphaBetaOn"] = not self.aiEngine.infoAI["alphaBetaOn"]
                            self.sideBarRefreshNeeded = True
                        elif event.key == pygame.K_2:
                            self.aiEngine.infoAI["moveSortingOn"] = not self.aiEngine.infoAI["moveSortingOn"]
                            self.sideBarRefreshNeeded = True
                        elif event.key == pygame.K_RETURN:
                            self.info["showMetrics"] = True
                            self.sideBarRefreshNeeded = True
                    else:
                        # showMetrics = true
                        if event.key == pygame.K_SPACE:
                            if not self.info["analysisRunning"]:

                                self.info["analysisRunning"] = True

                                self.refreshThread = threading.Thread(target=self.refreshSideBarPeriodically)
                                self.timerThread = threading.Thread(target=self.aiEngine.runTimer)
                                self.minimaxThread = threading.Thread(target=self.aiEngine.runMinimax)

                                self.refreshThread.start()
                                self.timerThread.start()
                                self.minimaxThread.start()
                            else:
                                self.info["analysisRunning"] = False

                                # is already running, so stop the threads
                                self.minimaxThread.join()
                                self.timerThread.join()
                                self.refreshThread.join()

                            self.sideBarRefreshNeeded = True

                        # you can only disable the metrics when the analysis is not running
                        # that way you avoid threads that run silently in the background
                        if event.key == pygame.K_RETURN and not self.info["analysisRunning"]:
                            self.info["showMetrics"] = False
                            self.sideBarRefreshNeeded = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.boardManager.isGameOver:

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

                    if self.boardManager.player == 1 and (self.boardManager.board[tileY][tileX] == 1 or self.boardManager.board[tileY][tileX] == 2):
                        self.boardManager.selected = (tileX, tileY)
                        self.boardManager.setPieceMoves()

                    elif self.boardManager.player == 2 and (self.boardManager.board[tileY][tileX] == 3 or self.boardManager.board[tileY][tileX] == 4):
                        self.boardManager.selected = (tileX, tileY)
                        self.boardManager.setPieceMoves()

                    elif self.boardManager.board[tileY][tileX] == 0:

                        move = self.boardManager.getMove(tileX, tileY)

                        if move is not None:
                            self.boardManager.makeMove(move)
                            self.gameBoardChanged = True

                    self.boardRefreshNeeded = True
                    self.sideBarRefreshNeeded = True

        if self.gameBoardChanged:
            # check if game is over and if so, draw game over menu
            self.boardManager.setGameStatus()

            self.boardManager.allMoves = self.boardManager.game.get_possible_moves()
            self.boardManager.pieceMoves = []
            self.gameBoardChanged = False

    def drawBoard(self):
        # --- Drawing code should go here
        self.drawEngine.drawBackground()

        self.drawEngine.drawPieces()

        self.drawEngine.drawAvailableMoves()

        self.drawEngine.drawTileLabels()

        self.drawEngine.rotateIfFlipped()

        self.drawEngine.drawGameOverScreen()

    def drawSideBar(self):
        self.drawEngine.drawSidebar()

    def refreshSideBarPeriodically(self):
        while self.info["analysisRunning"]:
            self.sideBarRefreshNeeded = True
            time.sleep(0.01)

    def draw(self):
        if self.boardRefreshNeeded:
            self.drawBoard()

        if self.sideBarRefreshNeeded:
            self.drawSideBar()

        if self.boardRefreshNeeded or self.sideBarRefreshNeeded:

            self.drawEngine.combineSurfaces()
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            self.sideBarRefreshNeeded = False
            self.boardRefreshNeeded = False
