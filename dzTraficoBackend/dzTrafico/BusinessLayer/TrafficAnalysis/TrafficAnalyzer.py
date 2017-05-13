import sumolib, traci

class TrafficAnalyzer:

    def __init__(self, simulation):
        self.__simulation = simulation
        self.__net = sumolib.net.readNet(simulation.get_network_file_path())

    def notify_congestion_detected(self, sensor_lane):
        nextNodeID = self.__net.getEdge(sumolib._laneID2edgeID(sensor_lane)).getToNode().getID()
        print(nextNodeID)
        traci.lane.setMaxSpeed(sensor_lane, 10)
