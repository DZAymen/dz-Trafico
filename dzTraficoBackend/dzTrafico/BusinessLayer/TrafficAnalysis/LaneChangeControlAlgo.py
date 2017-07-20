
class LaneChange:
    def get_lc_nodes(self, sink, congested_node, congested_lanes):
        lc_nodes = []
        node = self.get_previous_node(sink, congested_node)
        while node is not None or len(lc_nodes)<2:
            recommendation = self.get_lane_change_recommendation(congested_lanes, node)
            node.set_current_recommendation(recommendation)
            lc_nodes.append(node)
            node = self.get_previous_node(sink, node)
        return lc_nodes

    def get_previous_node(self, sink, node):
        index = sink.nodes.count(node)
        if(index > 0):
            return sink.nodes[index - 1]
        else:
            return None

    def get_lane_change_recommendation(self, congested_lanes, node):
        pass