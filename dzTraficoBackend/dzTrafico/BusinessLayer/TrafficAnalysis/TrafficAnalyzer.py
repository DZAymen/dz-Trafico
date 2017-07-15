import sumolib
from dzTrafico.BusinessLayer.TrafficAnalysis.JamTailProtectionControlAlgo import JamTailProtection

class TrafficAnalyzer:

    jamTailProtection = JamTailProtection()

    def __init__(self, simulation):
        self.__simulation = simulation
        self.__net = sumolib.net.readNet(simulation.get_network_file_path())

    def notify_congestion_detected(self, sink, node, congested_lanes):
        if len(node.sensors) == len(congested_lanes):
            print "jam"
        vsl_nodes = self.jamTailProtection.get_vsl_nodes(sink, node)
        self.activate_vsl(vsl_nodes)

        # nextNodeID = self.__net.getEdge(sumolib._laneID2edgeID(sensor_lane)).getToNode().getID()
        # print(nextNodeID)
        # traci.lane.setMaxSpeed(sensor_lane, 10)

    def activate_vsl(self, vsl_nodes):
        for node in vsl_nodes:
            node.activate_VSL()
        print vsl_nodes