
class AppInfo:

    def __init__(self):

        self.isRunning = True
        self.boardRefreshNeeded = True
        self.sideBarRefreshNeeded = True
        self.gameBoardChanged = True

        self.isFlipped = False
        self.analysisModeOn = False
        self.showMetrics = False
        self.analysisRunning = False

    def resetInfo(self):
        # don't reset 'isRunning' etc

        self.isFlipped = False
        self.analysisModeOn = False
        self.showMetrics = False
        self.analysisRunning = False
