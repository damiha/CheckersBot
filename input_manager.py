from tkinter import filedialog

import pygame

from constants import tileSize, tilesPerRow
from helpers import outOfBounds


class InputManager:

    def __init__(self, appInfo, aiEngine, fileManager, boardManager, threadManager):

        self.appInfo = appInfo
        self.aiEngine = aiEngine
        self.fileManager = fileManager
        self.boardManager = boardManager
        self.threadManager = threadManager

    def manageKeyEvent(self, event):
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
            self.appInfo.sideBarRefreshNeeded = True

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
                        self.threadManager.startThreads()

                    else:

                        self.appInfo.analysisRunning = False
                        self.threadManager.joinThreads()

                    self.appInfo.sideBarRefreshNeeded = True

                # you can only disable the metrics when the analysis is not running
                # that way you avoid threads that run silently in the background
                if event.key == pygame.K_RETURN and not self.appInfo.analysisRunning:
                    self.appInfo.showMetrics = False
                    self.appInfo.sideBarRefreshNeeded = True

    def manageMouseEvent(self):

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

            if self.boardManager.player == 1 and (
                    self.boardManager.board[tileY][tileX] == 1 or self.boardManager.board[tileY][tileX] == 2):
                self.boardManager.selected = (tileX, tileY)
                self.boardManager.setPieceMoves()

            elif self.boardManager.player == 2 and (
                    self.boardManager.board[tileY][tileX] == 3 or self.boardManager.board[tileY][tileX] == 4):
                self.boardManager.selected = (tileX, tileY)
                self.boardManager.setPieceMoves()

            elif self.boardManager.board[tileY][tileX] == 0:

                move = self.boardManager.getMove(tileX, tileY)

                if move is not None:
                    self.boardManager.makeMove(move)
                    self.appInfo.gameBoardChanged = True

            self.appInfo.boardRefreshNeeded = True
            self.appInfo.sideBarRefreshNeeded = True

