from dzTrafico.BusinessLayer.TrafficAnalysis.JamTailProtectionControlAlgo import JamTailProtection
from dzTrafico.BusinessLayer.TrafficAnalysis.LaneChangeControlAlgo import LaneChange
from dzTrafico.BusinessLayer.TrafficAnalysis.VirtualRampMeteringControlAlgo import VirtualRampMetering

class TrafficAnalyzer:

    jamTailProtectionController = JamTailProtection()
    laneChangeController = LaneChange()
    virtualRampMeteringController = VirtualRampMetering()

    isVSLControlActivated = False
    isLCControlActivated = False
    isCongestionDetected = False
    congestionExists = False

    def __init__(self, simulation):
        self.__simulation = simulation

    def notify_congestion_detected(self, sink, node, congested_lanes):

        lc_nodes = []
        vsl_nodes = []

        TrafficAnalyzer.isCongestionDetected = True
        TrafficAnalyzer.congestionExists = True

        # vsl_nodes = self.jamTailProtectionController.get_vsl_nodes(sink, node)
        # self.activate_vsl_control(vsl_nodes)

        # if there is a free lane
        if len(node.sensors) > len(congested_lanes):

            if TrafficAnalyzer.isLCControlActivated or TrafficAnalyzer.isVSLControlActivated:
                lc_nodes = self.laneChangeController.get_lc_nodes(sink, node, congested_lanes)

            if TrafficAnalyzer.isLCControlActivated:
                self.activate_lc_control(lc_nodes)

            if TrafficAnalyzer.isVSLControlActivated:
                vsl_nodes = self.virtualRampMeteringController.get_vsl_nodes(sink, node, len(lc_nodes))
                self.activate_vsl_control(vsl_nodes)

            return lc_nodes


    def activate_lc_control(self, lc_nodes):

        print "-------Activate LC CONTROL-------"

        for node in lc_nodes:
            node.activate_LC()

    def activate_vsl_control(self, vsl_nodes):

        print "-------Activate VSL CONTROL-------"

        for node in vsl_nodes:
            node.activate_VSL()

    def update_vsl(self, sink, node):
        self.virtualRampMeteringController.update_vsl(sink, node)

    def clear_congestion(self):
        TrafficAnalyzer.congestionExists = False