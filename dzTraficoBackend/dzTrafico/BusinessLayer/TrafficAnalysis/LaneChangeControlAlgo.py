from dzTrafico.BusinessEntities.LCRecommendation import LCRecommendation

class LaneChange:
    def get_lc_nodes(self, sink, congested_node, congested_lanes):
        lc_nodes = []
        node = self.get_previous_node(sink, congested_node)

        while node is not None and len(lc_nodes)<2:
            recommendations = self.get_lane_change_recommendations(congested_lanes, node)
            node.set_current_recommendations(recommendations)
            lc_nodes.append(node)
            node = self.get_previous_node(sink, node)
        return lc_nodes

    def get_previous_node(self, sink, node):
        index = sink.nodes.count(node)
        if(index > 0):
            return sink.nodes[index - 1]
        else:
            return None

    def get_lane_change_recommendations(self, congested_lanes, node):
        recommendations = []
        lanes = len(node.sensors)
        for lane in range(0,lanes):
            # if lane is the most right lane
            # change to right if it's closed
            # else straight ahead
            if lane == 0:
                if congested_lanes.count(lane) > 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_LEFT
                        )
                    )
                else:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.STRAIGHT_AHEAD
                        )
                    )
            # if lane is the most left lane
            # change to left if it's closed
            # else straight ahead
            elif lane == lanes - 1:
                if congested_lanes.count(lane) > 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_RIGHT
                        )
                    )
                else:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.STRAIGHT_AHEAD
                        )
                    )
            # if lane is in the middle between most right and left lanes is closed
            elif congested_lanes.count(lane) > 0:
                # if the right and left lanes are opened, change to the left
                if congested_lanes.count(lane-1) == 0 and congested_lanes.count(lane+1) == 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_LEFT
                        )
                    )
                # elif the right lane is closed and the left one is opened, change to left
                elif congested_lanes.count(lane-1) > 0 and congested_lanes.count(lane+1) == 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_LEFT
                        )
                    )
                # elif the left lane is closed and the right one is opened, change to right
                elif congested_lanes.count(lane-1) == 0 and congested_lanes.count(lane+1) > 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_RIGHT
                        )
                    )
                # elif the right and left lanes are closed, straight ahead
                elif congested_lanes.count(lane-1) > 0 and congested_lanes.count(lane+1) > 0:
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.STRAIGHT_AHEAD
                        )
                    )
            # if lane is in the middle between most right and left lanes is opened
            elif congested_lanes.count(lane) == 0:
                recommendations.append(
                    LCRecommendation(
                        lane,
                        LCRecommendation.STRAIGHT_AHEAD
                    )
                )
        return recommendations