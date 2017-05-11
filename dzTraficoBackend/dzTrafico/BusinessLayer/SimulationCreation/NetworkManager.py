from dzTrafico.Helpers.MapManager import MapManager
import subprocess
import os

class NetworkManager:

    __map_manager = MapManager()

    def convert_map_to_network_file(self, osm_file_path):
        #Return network file path
        network_file_path = os.path.dirname(osm_file_path) + "\\map.net.xml"
        subprocess.call("netconvert --osm-files " + osm_file_path + " -o " + network_file_path)
        return network_file_path

    def get_network_file(self, map_box):
        self.osm_file_path = NetworkManager.__map_manager.download_map(map_box)
        return self.convert_map_to_network_file(self.osm_file_path)
