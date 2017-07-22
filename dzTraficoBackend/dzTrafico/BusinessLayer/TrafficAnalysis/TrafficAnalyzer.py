import sumolib
from dzTrafico.BusinessLayer.TrafficAnalysis.JamTailProtectionControlAlgo import JamTailProtection
from dzTrafico.BusinessLayer.TrafficAnalysis.LaneChangeControlAlgo import LaneChange

class TrafficAnalyzer:

    jamTailProtectionController = JamTailProtection()
    laneChangeController = LaneChange()

    def __init__(self, simulation):
        self.__simulation = simulation

    def notify_congestion_detected(self, sink, node, congested_lanes):

        vsl_nodes = self.jamTailProtectionController.get_vsl_nodes(sink, node)
        self.activate_vsl_control(vsl_nodes)

        # if there is a free lane
        if len(node.sensors) > len(congested_lanes):
            lc_nodes = self.laneChangeController.get_lc_nodes(sink, node, congested_lanes)
            self.activate_lc_control(lc_nodes)
        # nextNodeID = self.__net.getEdge(sumolib._laneID2edgeID(sensor_lane)).getToNode().getID()

    def activate_vsl_control(self, vsl_nodes):

        print "-------Activate VSL CONTROL-------"

        for node in vsl_nodes:
            node.activate_VSL()

    def activate_lc_control(self, lc_nodes):

        print "-------Activate LC CONTROL-------"

        for node in lc_nodes:
            node.activate_LC()