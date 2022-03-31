
class InfoAI:

    def __init__(self):

        self.debugOn = True
        self.alphaBetaOn = True
        self.memoizationOn = False
        self.searchDepth = 5

        self.evaluatedPositions = 0
        # runtime since start of the analysis
        self.runtime = 0.0
        self.bestMoveSequence = None
        # 0 => neither is better, + => white is winning, - => black is winning
        self.estimation = 0


