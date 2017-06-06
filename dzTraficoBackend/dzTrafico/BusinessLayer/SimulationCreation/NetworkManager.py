from dzTrafico.Helpers.MapManager import MapManager
import subprocess, os
import sumolib

class NetworkManager:

    __map_manager = MapManager()
    __network_file_path = ""
    net = None

    def convert_map_to_network_file(self, osm_file_path):
        #Return network file path
        self.__network_file_path = os.path.dirname(osm_file_path) + "\\map.net.xml"
        subprocess.call("netconvert --osm-files " + osm_file_path + " -o " + self.__network_file_path)
        return self.__network_file_path

    def get_network_file(self, map_box):
        self.osm_file_path = NetworkManager.__map_manager.download_map(map_box)
        return self.convert_map_to_network_file(self.osm_file_path)

    def initialize_net(self):
        if self.net is None:
            self.net = sumolib.net.readNet(self.__network_file_path)

    def get_edgeId_from_geoCoord(self, lon, lat):
        #self.initialize_net()
        #x, y = self.net.convertLonLat2XY(lon, lat)
        #self.net.getNeighboringEdges(x,y,0.1, False)
        return str(lon)
