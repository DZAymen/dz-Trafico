
class LCRecommendation:

    TURN_LEFT = -1
    TURN_RIGHT = 1
    STRAIGHT_AHEAD = 0

    change_lane = True

    def __init__(self, lane, recommendation):
        self.lane = lane
        if recommendation == self.TURN_RIGHT:
            self.target_lane = lane - 1
        elif recommendation == self.TURN_LEFT:
            self.target_lane = lane + 1
        elif recommendation == self.STRAIGHT_AHEAD:
            self.change_lane = False