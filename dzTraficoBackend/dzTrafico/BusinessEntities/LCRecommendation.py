
class LCRecommendation:

    TURN_LEFT = -1
    TURN_RIGHT = 1
    STRAIGHT_AHEAD = 0
    CHANGE_TO_EITHER_WAY = 2

    change_lane = True
    change_to_either_way = False
    recommendation = 0

    def __init__(self, lane, recommendation):
        self.lane = lane
        self.recommendation = recommendation
        if recommendation == self.TURN_RIGHT:
            self.target_lane = lane - 1
        elif recommendation == self.TURN_LEFT:
            self.target_lane = lane + 1
        elif recommendation == self.CHANGE_TO_EITHER_WAY:
            self.change_to_either_way = True
        elif recommendation == self.STRAIGHT_AHEAD:
            self.change_lane = False