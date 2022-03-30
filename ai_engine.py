
import time


class AIEngine:

    def __init__(self, appInfo):

        self.startTime = -1.0
        self.endTime = -1.0

        # get app info to receive commands
        self.appInfo = appInfo

        self.infoAI = {
            "alphaBetaOn": False,
            "moveSortingOn": False,
            "searchDepth": 5,


            "evaluatedPositions": 0,
            # runtime since start of the analysis
            "runtime": 0.0,
            "bestMove": None,
            # 0 => neither is better, + => white is winning, - => black is winning
            "estimation": 0
        }

    def runTimer(self):
        self.startTime = time.perf_counter()

        while self.appInfo.analysisRunning:

            self.endTime = time.perf_counter()
            self.infoAI["runtime"] = round(self.endTime - self.startTime, 2)

            # sleep to prevent time measuring from becoming a performance drainer
            time.sleep(0.01)

    def runMinimax(self):

        # reset before running
        self.infoAI["evaluatedPositions"] = 0
        self.infoAI["estimation"] = 0

        # dummy code to check how it looks on the sidebar
        while self.appInfo.analysisRunning:

            self.infoAI["evaluatedPositions"] += 1
            self.infoAI["estimation"] += 1




