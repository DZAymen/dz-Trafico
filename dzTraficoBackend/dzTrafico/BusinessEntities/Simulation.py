
class Simulation:
    __sensors_list = []
    __incidents_list = []
    __traffic_flows = []

    def set_osm_file(self, file_path):
        self.__osm_file = file_path

    def set_network_file(self, file_path):
        self.__network_file = file_path