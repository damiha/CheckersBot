# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws

import tkinter as tk
from tkinter import filedialog
from ai_engine import AIEngine
from app_info import AppInfo
from board_manager import BoardManager
from draw_engine import *
from file_manager import FileManager
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

        self.appInfo = AppInfo()
        self.boardManager = BoardManager()
        self.fileManager = FileManager(self.boardManager)

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.aiEngine = AIEngine()
        # call explicitly so call doesn't get optimized away
        self.aiEngine.__int__(self.appInfo)

        self.drawEngine = DrawEngine(self)

        # threads
        self.refreshThread = None
        self.timerThread = None
        self.minimaxThread = None

    def isRunning(self):
        return self.appInfo.isRunning

    def update(self):
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close

                self.appInfo.isRunning = False  # Flag that we are done, so we can exit the while loop

                if self.appInfo.analysisRunning:

                    self.appInfo.analysisRunning = False
                    # closing window should also close the threads
                    self.minimaxThread.join()
                    self.timerThread.join()
                    self.refreshThread.join()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    filepath = filedialog.askopenfilename()

                    # write out moves
                    if filepath is not None and filepath != () and filepath != "":
                        self.fileManager.writeMovesToFile(filepath)

                elif event.key == pygame.K_l:

                    filepath = filedialog.askopenfilename()
                    # read in moves and replay the game
                    if filepath is not None and filepath != () and filepath != "":

                        self.fileManager.loadBoardFromFile(filepath)

                        self.appInfo.boardRefreshNeeded = True
                        self.appInfo.sideBarRefreshNeeded = True
                        self.appInfo.gameBoardChanged = True

                elif event.key == pygame.K_f and not self.boardManager.isGameOver:

                    self.appInfo.isFlipped = not self.appInfo.isFlipped
                    self.appInfo.boardRefreshNeeded = True

                elif event.key == pygame.K_r:

                    self.boardManager.reset()

                    self.appInfo.gameBoardChanged = True
                    self.appInfo.boardRefreshNeeded = True

                # you can't quit the analysis mode while it's about to run
                elif event.key == pygame.K_a and not self.appInfo.showMetrics:

                    self.appInfo.analysisModeOn = not self.appInfo.analysisModeOn
                    self.appInfo.sideBarRefreshNeeded = True

                elif self.appInfo.analysisModeOn:
                    # you can't change the parameters when the analysis is about to run
                    if not self.appInfo.showMetrics:
                        if event.key == pygame.K_PLUS:
                            self.aiEngine.infoAI["searchDepth"] += 1

                        elif event.key == pygame.K_MINUS:
                            self.aiEngine.infoAI["searchDepth"] -= 1 if self.aiEngine.infoAI["searchDepth"] > 1 else 0

                        elif event.key == pygame.K_1:
                            self.aiEngine.infoAI["alphaBetaOn"] = not self.aiEngine.infoAI["alphaBetaOn"]

                        elif event.key == pygame.K_2:
                            self.aiEngine.infoAI["moveSortingOn"] = not self.aiEngine.infoAI["moveSortingOn"]

                        elif event.key == pygame.K_RETURN:
                            self.appInfo.showMetrics = True

                        self.appInfo.sideBarRefreshNeeded = True
                    else:
                        # showMetrics = true
                        if event.key == pygame.K_SPACE:
                            if not self.appInfo.analysisRunning:

                                self.appInfo.analysisRunning = True

                                self.refreshThread = threading.Thread(target=self.refreshSideBarPeriodically)
                                self.timerThread = threading.Thread(target=self.aiEngine.runTimer)
                                self.minimaxThread = threading.Thread(target=self.aiEngine.runMinimax)

                                self.refreshThread.start()
                                self.timerThread.start()
                                self.minimaxThread.start()
                            else:
                                self.appInfo.analysisRunning = False

                                # is already running, so stop the threads
                                self.minimaxThread.join()
                                self.timerThread.join()
                                self.refreshThread.join()

                            self.appInfo.sideBarRefreshNeeded = True

                        # you can only disable the metrics when the analysis is not running
                        # that way you avoid threads that run silently in the background
                        if event.key == pygame.K_RETURN and not self.appInfo.analysisRunning:
                            self.appInfo.showMetrics = False
                            self.appInfo.sideBarRefreshNeeded = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.boardManager.isGameOver:

                [mouseX, mouseY] = pygame.mouse.get_pos()
                # convert mousePosition to tilePosition
                tileX = int(mouseX / tileSize)
                tileY = int(mouseY / tileSize)

                # if flipped, translation is needed
                if self.appInfo.isFlipped:
                    tileX = (tilesPerRow - 1) - tileX
                    tileY = (tilesPerRow - 1) - tileY

                # prevent that a click outside the game window leads to an out-of-bounds exception
                if not outOfBounds(tileX, tileY):

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
                            self.appInfo.gameBoardChanged = True

                    self.appInfo.boardRefreshNeeded = True
                    self.appInfo.sideBarRefreshNeeded = True

        if self.appInfo.gameBoardChanged:
            # check if game is over and if so, draw game over menu
            self.boardManager.setGameStatus()

            self.boardManager.allMoves = self.boardManager.game.get_possible_moves()
            self.boardManager.pieceMoves = []
            self.appInfo.gameBoardChanged = False

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
        while self.appInfo.analysisRunning:
            self.appInfo.sideBarRefreshNeeded = True
            time.sleep(0.01)

    def draw(self):
        if self.appInfo.boardRefreshNeeded:
            self.drawBoard()

        if self.appInfo.sideBarRefreshNeeded:
            self.drawSideBar()

        if self.appInfo.boardRefreshNeeded or self.appInfo.sideBarRefreshNeeded:

            self.drawEngine.combineSurfaces()
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            self.appInfo.sideBarRefreshNeeded = False
            self.appInfo.boardRefreshNeeded = False
