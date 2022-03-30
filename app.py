# --- IMPORTANT ---
# 1. this bot plays according to the rules of international draughts on lidraughts.org
# 2. it uses the pydraughts package to generate valid moves & check for wins/draws

import tkinter as tk
from ai_engine import AIEngine
from app_info import AppInfo
from board_manager import BoardManager
from draw_engine import *
from file_manager import FileManager
from input_manager import InputManager
from thread_manager import ThreadManager


class App:

    def __init__(self):

        # hide tkinter's root window, only needed for the file dialog prompt
        # this code fragment can't be moved to input manager (moving it there causes the app to lag)
        root = tk.Tk()
        root.withdraw()

        # start pygame, open a new window
        pygame.init()
        self.screen = pygame.display.set_mode(windowSize)
        pygame.display.set_caption("CheckersBot")

        self.appInfo = AppInfo()

        self.aiEngine = AIEngine(self.appInfo)

        self.boardManager = BoardManager()
        self.fileManager = FileManager(self.boardManager)
        self.threadManager = ThreadManager(self.appInfo, self.aiEngine)
        self.inputManager = InputManager(self.appInfo, self.aiEngine, self.fileManager, self.boardManager, self.threadManager)

        # The clock will be used to control how fast the screen updates
        self.clock = pygame.time.Clock()

        self.drawEngine = DrawEngine(self)

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
                    self.threadManager.joinThreads()

            elif event.type == pygame.KEYDOWN:
                self.inputManager.manageKeyEvent(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.boardManager.isGameOver:
                self.inputManager.manageMouseEvent()

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
