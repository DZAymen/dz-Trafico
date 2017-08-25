from dzTrafico.BusinessEntities.LCRecommendation import LCRecommendation

class LaneChange:

    EdgeLength = 200
    # A design parameter related to the capacity of bottleneck and the traffic demand
    Xi = 400

    def get_lc_nodes(self, sink, congested_node, congested_lanes):

        num_LC_controlled_sections = int(round(len(congested_lanes) * LaneChange.Xi / LaneChange.EdgeLength))

        lc_nodes = self.get_previous_nodes(sink, congested_node, num_LC_controlled_sections)

        for node in lc_nodes:
            recommendations = self.get_lane_change_recommendations(congested_lanes, node)
            node.set_current_recommendations(recommendations)

        # Set LCRecommendation for congested edge
        recommendations = self.get_lane_change_recommendations(congested_lanes, congested_node)
        congested_node.set_current_recommendations(recommendations)

        return lc_nodes

    def get_previous_nodes(self, sink, node, nodes_number):
        index = 0
        if sink.nodes.count(node):
            index = sink.nodes.index(node)
        nodes = []
        i = 0
        while i < nodes_number and i < index:
            nodes.append(sink.nodes[index - 1 - i])
            i += 1
        return nodes

    def get_lane_change_recommendations(self, congested_lanes, node):
        recommendations = []
        lanes = len(node.sensors)
        #1
        for lane in range(0,lanes):
            if not congested_lanes.count(lane):
                recommendations.append(
                    LCRecommendation(
                        lane,
                        LCRecommendation.STRAIGHT_AHEAD
                    )
                )
        #2
        if congested_lanes.count(0):
            recommendations.append(
                LCRecommendation(
                    0,
                    LCRecommendation.TURN_LEFT
                )
            )
        if congested_lanes.count(lanes-1):
            recommendations.append(
                LCRecommendation(
                    lanes-1,
                    LCRecommendation.TURN_RIGHT
                )
            )
        #3
        for lane in range(1,lanes-1):
            if congested_lanes.count(lane) and not congested_lanes.count(lane-1) and not congested_lanes.count(lane+1):
                recommendations.append(
                    LCRecommendation(
                        lane,
                        LCRecommendation.CHANGE_TO_EITHER_WAY
                    )
                )
        #4
        for lane in range(1, lanes - 1):
            if congested_lanes.count(lane):
                if congested_lanes.count(lane-1) and not congested_lanes.count(lane+1):
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_LEFT
                        )
                    )
                elif congested_lanes.count(lane+1) and not congested_lanes.count(lane-1):
                    recommendations.append(
                        LCRecommendation(
                            lane,
                            LCRecommendation.TURN_LEFT
                        )
                    )
        #5
        for lane in range(1, lanes - 1):
            if congested_lanes.count(lane) and congested_lanes.count(lane-1) and congested_lanes.count(lane+1):
                for recommendation in recommendations:
                    if recommendation.lane == lane+1:
                        left_recommendation = recommendation
                    if recommendation.lane == lane-1:
                        right_recommendation = recommendation

                if left_recommendation is not None and right_recommendation is not None:
                    if left_recommendation.recommendation == right_recommendation.recommendation:
                        recommendations.append(
                            LCRecommendation(
                                lane,
                                left_recommendation.recommendation
                            )
                        )
                    else:
                        recommendations.append((
                            LCRecommendation(
                                lane,
                                LCRecommendation.CHANGE_TO_EITHER_WAY
                            )
                        ))

                # # if lane is the most right lane
            # # change to right if it's closed
            # # else straight ahead
            # if lane == 0:
            #     if congested_lanes.count(lane) > 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.TURN_LEFT
            #             )
            #         )
            #     else:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.STRAIGHT_AHEAD
            #             )
            #         )
            # # if lane is the most left lane
            # # change to left if it's closed
            # # else straight ahead
            # elif lane == lanes - 1:
            #     if congested_lanes.count(lane) > 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.TURN_RIGHT
            #             )
            #         )
            #     else:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.STRAIGHT_AHEAD
            #             )
            #         )
            # # if lane is in the middle between most right and left lanes is closed
            # elif congested_lanes.count(lane) > 0:
            #     # if the right and left lanes are opened, change to either way
            #     if congested_lanes.count(lane-1) == 0 and congested_lanes.count(lane+1) == 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.CHANGE_TO_EITHER_WAY
            #             )
            #         )
            #     # elif the right lane is closed and the left one is opened, change to left
            #     elif congested_lanes.count(lane-1) > 0 and congested_lanes.count(lane+1) == 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.TURN_LEFT
            #             )
            #         )
            #     # elif the left lane is closed and the right one is opened, change to right
            #     elif congested_lanes.count(lane-1) == 0 and congested_lanes.count(lane+1) > 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.TURN_RIGHT
            #             )
            #         )
            #     # elif the right and left lanes are closed, straight ahead
            #     elif congested_lanes.count(lane-1) > 0 and congested_lanes.count(lane+1) > 0:
            #         recommendations.append(
            #             LCRecommendation(
            #                 lane,
            #                 LCRecommendation.STRAIGHT_AHEAD
            #             )
            #         )
            # # if lane is in the middle between most right and left lanes is opened
            # elif congested_lanes.count(lane) == 0:
            #     recommendations.append(
            #         LCRecommendation(
            #             lane,
            #             LCRecommendation.STRAIGHT_AHEAD
            #         )
            #     )
        return recommendations