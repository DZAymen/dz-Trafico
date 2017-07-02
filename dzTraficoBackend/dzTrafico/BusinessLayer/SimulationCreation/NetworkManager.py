from dzTrafico.Helpers.MapManager import MapManager
import subprocess, os
import sumolib

class NetworkManager:

    __mapManager = MapManager()
    __network_file_path = ""
    net = None

    def convert_map_to_network_file(self, osm_file_path):
        #Return network file path
        self.__network_file_path = os.path.dirname(osm_file_path) + "\\map.net.xml"
        subprocess.call("netconvert --osm-files " + osm_file_path + " -o " + self.__network_file_path)
        return self.__network_file_path

    def get_network_file(self, map_box):
        osm_file_path = NetworkManager.__mapManager.download_map(map_box)
        return self.convert_map_to_network_file(osm_file_path)

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