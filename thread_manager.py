
import time
import threading

from constants import refreshTime


class ThreadManager:

    def __init__(self, appInfo, boardManager, aiEngine):

        self.appInfo = appInfo
        self.aiEngine = aiEngine
        self.boardManager = boardManager

        self.refreshThread = None
        self.timerThread = None
        self.minimaxThread = None

    def refreshSideBarPeriodically(self):

        while self.appInfo.analysisRunning:
            self.appInfo.sideBarRefreshNeeded = True
            time.sleep(refreshTime)

    def startThreads(self):

        self.refreshThread = threading.Thread(target=self.refreshSideBarPeriodically)
        self.timerThread = threading.Thread(target=self.aiEngine.runTimer)
        self.minimaxThread = threading.Thread(target=self.aiEngine.runMinimax, args=[self.boardManager.game])

        self.refreshThread.start()
        self.timerThread.start()
        self.minimaxThread.start()

    def joinThreads(self):

        self.minimaxThread.join()
        self.timerThread.join()
        self.refreshThread.join()
