
class Simulation:
    __osm_file = ""
    __network_file = ""
    __sensors_list = []
    __incidents_list = []
    __traffic_flows = []

    def set_osm_file(self, file_path):
        Simulation.__osm_file = file_path

    def set_network_file(self, file_path):
        Simulation.__network_file = file_path