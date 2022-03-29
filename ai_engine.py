
class AIEngine:

    def __int__(self):

        self.infoAI = {
            "alphaBetaOn": False,
            "moveSortingOn": False,
            "searchDepth": 5,


            "evaluatedPositions": 0,
            # runtime since start of the analysis
            "runtime": 0,
            "bestMove": None,
            # 0 => neither is better, + => white is winning, - => black is winning
            "estimation": 0
        }

