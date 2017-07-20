
class LCRecommendation:

    TURN_LEFT = -1
    TURN_RIGHT = 1
    GO_AHEAD = 0

    def __init__(self, lane, recommendation):
        self.lane = lane
        self.recommendation = recommendation