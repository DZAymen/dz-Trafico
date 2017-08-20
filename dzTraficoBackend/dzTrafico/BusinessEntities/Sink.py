from EdgeState import EdgeState

class Sink(object):

    id = 0
    trafficAnalyzer = None

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
            node.change_lane()

    def update_vsl(self):
        for node in self.nodes:
            if node.VSL_is_activated:
                Sink.trafficAnalyzer.update_vsl(self, node)

    def deactivate_vsl(self):
        for node in self.nodes:
            node.deactivate_VSL()

    def read_traffic_state(self):
        traffic_state = []
        congestion_detected = False
        for node in self.nodes:
            # if node.VSL_is_activated:
            #
            #     print "--------VSL_is_activated----------"
            #     print node.edge.getID()
            #
            #     if node.check_if_discharged():
            #         node.deactivate_VSL()
            #
            #         print "--------deactivate_VSL----------"
            #         print node.edge.getID()
            # else:

            congested_lanes = node.check_congested_lanes()
            # congestion_detected = len(congested_lanes)>0
            # if congestion_detected and Sink.flag:
            #     print "--------notify_congestion_detected----------"
            #     print node.edge.getID()
            #     print congested_lanes
            #
            #     Sink.trafficAnalyzer.notify_congestion_detected(self, node, congested_lanes)
            #     Sink.flag = False

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