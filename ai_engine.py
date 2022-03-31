
import time

from info_ai import InfoAI


class AIEngine:

    def __init__(self, appInfo):

        # get app info to receive commands
        self.appInfo = appInfo
        self.infoAI = InfoAI()

    def runTimer(self):

        startTime = time.perf_counter()

        while self.appInfo.analysisRunning:

            endTime = time.perf_counter()
            self.infoAI.runtime = round(endTime - startTime, 2)

            # sleep to prevent time measuring from becoming a performance drainer
            time.sleep(0.01)

    def runMinimax(self):

        # reset before running
        self.infoAI.evaluatedPositions = 0
        self.infoAI.estimation = 0

        # dummy code to check how it looks on the sidebar
        while self.appInfo.analysisRunning:

            self.infoAI.evaluatedPositions += 1
            self.infoAI.estimation += 1




