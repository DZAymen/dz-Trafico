from EdgeState import EdgeState
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer

class Sink(object):

    id = 0
    trafficAnalyzer = None
    incidents = []

    def __init__(self):
        self.id = Sink.id
        Sink.id += 1
        self.nodes = []

        #print "--------nodes----------"
        #print len(nodes)

    def add_node(self, node):
        self.nodes.append(node)

    def get_sensors(self):
        sensors = []
        for node in self.nodes:
            for sensor in node.sensors:
                sensors.append(sensor)
        return sensors

    def change_lane(self):
        for node in self.nodes:
            if node.LC_is_activated:
                node.change_lane()

    def incident_change_lane(self):
        for node in self.nodes:
            if node.isCongested:
                node.incident_change_lane()

    def update_vsl(self):
        for node in self.nodes:
            if node.VSL_is_activated:
                Sink.trafficAnalyzer.update_vsl(self, node)

    def deactivate_vsl(self):
        for node in self.nodes:
            node.deactivate_VSL()

    def deactivate_lc(self):
        for node in self.nodes:
            node.deactivate_LC()

    def set_sumo_LC_Model(self, mode):
        for node in self.nodes:
            if node.LC_is_activated:
                node.set_sumo_LC_Model(mode)

    def read_traffic_state(self):
        traffic_state = []
        for node in self.nodes:

            congested_lanes = node.check_congested_lanes()
            for incident in self.incidents:
                congestion_detected = len(congested_lanes) > 0 and node.edge.getID() == incident.edge.getID()
                if congestion_detected:
                    congested_lanes = [incident.lane]
                    break

            if congestion_detected and not TrafficAnalyzer.isCongestionDetected:
                print "--------notify_congestion_detected----------"
                print node.edge.getID()
                print congested_lanes
                node.isCongested = True
                node.set_congested_lanes(congested_lanes)
                if TrafficAnalyzer.isLCControlActivated:
                    node.close_incident_lanes()
                Sink.trafficAnalyzer.notify_congestion_detected(self, node, congested_lanes)

            elif TrafficAnalyzer.congestionExists and node.isCongested and TrafficAnalyzer.isLCControlActivated:
                if node.check_if_discharged():
                    Sink.trafficAnalyzer.clear_congestion()
                    node.isCongested = False

            traffic_state.append(
                EdgeState(
                    node.edge.getID(),
                    node.get_current_speed(),
                    node.get_current_vsl(),
                    node.get_current_density(),
                    node.VSL_is_activated,
                    congestion_detected
                )
            )
        return traffic_state

    def get_node_by_edgeID(self, edge_id):
        for node in self.nodes:
            if node.edge.getID() == edge_id:
                return node
        return None