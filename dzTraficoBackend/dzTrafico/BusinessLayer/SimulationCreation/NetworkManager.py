from dzTrafico.Helpers.MapManager import MapManager
from dzTrafico.BusinessEntities.Simulation import Simulation
from sumolib.net.generator.network import Split
import subprocess, os, sumolib
import lxml.etree as etree

class NetworkManager:

    __mapManager = MapManager()
    __network_file_path = ""
    net = None

    def convert_map_to_network_file(self, osm_file_path):
        #Return network file path
        self.__network_file_path = os.path.dirname(osm_file_path) + "\\map.net.xml"
        subprocess.call("netconvert --osm-files " + osm_file_path + " -o " + self.__network_file_path)
        return self.__network_file_path

    def convert_map_to_network_file_with_splitted_edges(self, splitted_edges_file):
        #Return network file path
        subprocess.call(
            "netconvert --osm-files " + self.osm_file_path
            + " -e " + splitted_edges_file
            + " -o " + self.__network_file_path)
        self.net = None
        return self.__network_file_path

    def get_network_file(self, map_box):
        self.osm_file_path = NetworkManager.__mapManager.download_map(map_box)
        return self.convert_map_to_network_file(self.osm_file_path)

    def initialize_net(self):
        if self.net is None:
            self.net = sumolib.net.readNet(self.__network_file_path)

    def get_edgeId_from_geoCoord(self, lon, lat):
        self.initialize_net()
        radius = 1000
        x, y = self.net.convertLonLat2XY(lon, lat)
        edges = self.net.getNeighboringEdges(x,y,radius, False)
        if len(edges)>0:
            distancesAndEdges = sorted([(dist, edge) for edge, dist in edges])
            dist, closestEdge = distancesAndEdges[0]
            return closestEdge.getID()
        return 0

    def get_edge(self, edge_id):
        self.initialize_net()
        return self.net.getEdge(edge_id)

    def generate_network_file_with_splitted_edges(self, flows, distance):
        # Get primary edges
        primary_edges = self.get_edges(flows)
        # Split edges by sensors_distance
        splitted_edges = self.split_edges(primary_edges, distance)
        # Generate edges definition xml file to include in netconvert command line
        splitted_edges_file = self.create_splitted_edges_file(splitted_edges)
        # Generate the new net xml file with the splitted edges
        self.convert_map_to_network_file_with_splitted_edges(splitted_edges_file)

    # Returns edges situated between start_edge and end_edge for each flow
    # We should fix the case of multi next edges
    def get_edges(self, flows):
        edges_list = []
        for flow in flows:

            # get source edges from which we can reach the flow.end_edge
            cands = self.get_source_edges(self.get_edge(flow.end_edge))

            current_edge = self.get_edge(flow.start_edge)
            edges = [current_edge]

            print "not current_edge.getID() == flow.end_edge"
            print not current_edge.getID() == flow.end_edge
            print current_edge
            while not current_edge.getID() == flow.end_edge:
                current_edges = current_edge.getToNode().getOutgoing()
                if len(current_edges) > 1:
                    current_edge = self.choose_next_edge(current_edges, cands)
                    print "len(current_edges) > 1"
                    print current_edge
                else:
                    current_edge = current_edges[0]
                    print "len(current_edges) == 0"
                    print current_edge
                edges.append(current_edge)

            edges_list.append(edges)

            print "------------flow------------"
            print flow

            print "------------edges------------"
            print edges

        print "------------edges_list------------"
        print edges_list

        return edges_list

    # returns edges from which the destination is reachable
    def get_source_edges(self, destination):
        fringe = [destination]
        found = set()
        found.add(destination)
        while len(fringe) > 0:
            new_fringe = []
            for edge in fringe:
                cands = edge.getIncoming()
                for reachable in cands:
                    if not reachable in found:
                        found.add(reachable)
                        new_fringe.append(reachable)
            fringe = new_fringe
        return found

    # returns the first next edge found
    def choose_next_edge(self, current_edges, cands):
        for edge in current_edges:
            if edge in cands:
                return edge

    # Split edges into equal segments
    # each one's length is almost equal sensors_distance
    def split_edges(self, primary_edges, sensors_distance):
        splitted_edges = []
        already_splitted_edges = set()

        print "------------primary_edges------------"
        print primary_edges

        for edges in primary_edges:
            for edge in edges:
                if not edge in already_splitted_edges:
                    splits = []
                    sub_edges_num = int(edge.getLength() / sensors_distance)
                    for i in range(0, sub_edges_num):
                        splits.append(
                            Split(
                                distance = i * sensors_distance,
                                lanes = []
                            )
                        )
                    if len(splits) > 0:
                        splitted_edges.append(
                            SplittedEdge(
                                edge.getID(),
                                edge.getLaneNumber(),
                                splits
                            )
                        )
                    already_splitted_edges.add(edge)
        return splitted_edges

    def create_splitted_edges_file(self, splitted_edges):
        splitted_edges_filename = "edges.xml"
        edges_node = etree.Element("edges")
        for splitted_edge in splitted_edges:
            edge_node = etree.Element("edge",
                                      id=str(splitted_edge.edge_id),
                                      numLanes=str(splitted_edge.num_lanes)
                                      )
            # Add splits to the concerned edge
            for split in splitted_edge.splits:
                split_node = etree.Element("split",
                                           pos=str(split.distance)
                                           )
                edge_node.append(split_node)

            edges_node.append(edge_node)
        et = etree.ElementTree(edges_node)
        et.write(Simulation.project_directory + "\\" + splitted_edges_filename, pretty_print=True)
        return Simulation.project_directory + "\\" + splitted_edges_filename


class SplittedEdge:

    def __init__(self, edge_id, num_lanes, splits):
        self.edge_id = edge_id
        self.num_lanes = num_lanes
        self.splits = splits