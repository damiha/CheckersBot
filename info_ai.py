
class InfoAI:

    def __init__(self):

        self.debugOn = False
        self.alphaBetaOn = True
        self.memoizationOn = True
        self.searchDepth = 5

        self.evaluatedPositions = 0
        # runtime since start of the analysis
        self.runtime = 0.0
        self.bestMoveSequence = None
        # 0 => neither is better, + => white is winning, - => black is winning
        self.estimation = 0.0


