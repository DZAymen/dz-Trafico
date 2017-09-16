from EdgeState import EdgeState
from rest_framework import serializers
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer, VirtualRampMetering
from dzTrafico.BusinessEntities.Location import LocationSerializer
from dzTrafico.BusinessLayer.SimulationCreation.NetworkManager import NetworkManager

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
        vsl = []
        index = 1
        for node in self.nodes:
            if node.VSL_is_activated:
                Sink.trafficAnalyzer.update_vsl(self, node)
                vsl_node = dict()
                vsl_node["id"] = index
                vsl_node["vsl"] = node.get_current_vsl()
                vsl.append(vsl_node)
                index += 1
        return  vsl

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
            congestion_detected = len(congested_lanes) > 0
            if congestion_detected:
                for incident in Sink.incidents:
                    print "incident ===> ", incident.edge.getID()
                    congestion_detected = node.edge.getID() == incident.edge.getID()
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
            edge_coords = dict()
            start, end = NetworkManager.get_edge_coords(node.edge)
            edge_coords["start"] = LocationSerializer(start).data
            edge_coords["end"] = LocationSerializer(end).data
            traffic_state.append(
                EdgeState(
                    node.edge.getID(),
                    edge_coords,
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

    def get_LC_recommendations(self):
        lc_recommendations = []
        index = VirtualRampMetering.num_vsl_controlled_sections + 1
        for node in self.nodes:
            lanes = []
            if node.LC_is_activated:
                for r in node.recommendations:
                    lanes.append(
                        NodeLanesRcmd(
                            r.lane,
                            r.recommendation
                        )
                    )
                lc_recommendations.extend(
                    [
                        NodeLCRcmd(
                            index,
                            lanes
                        )
                    ]
                )
                index += 1
        nodeLCRcmdSerializer = NodeLCRcmdSerializer(lc_recommendations, many=True)
        return nodeLCRcmdSerializer.data

class NodeLCRcmd(object):
    def __init__(self, id, lanes):
        self.id = id
        self.lanes = lanes

class NodeLanesRcmd(object):
    def __init__(self, lane, recommendation):
        self.lane = lane
        self.recommendation = recommendation

class NodeLanesRcmdSerializer(serializers.Serializer):
    lane = serializers.IntegerField()
    recommendation = serializers.IntegerField()

class NodeLCRcmdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    lanes = NodeLanesRcmdSerializer(many=True)


