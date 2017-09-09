from dzTrafico.BusinessEntities.Simulation import Simulation
import lxml.etree as etree

class DataVisualizationController(object):

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_emissions_results(self):
        pass

    def get_travel_time_results(self):
        travel_time_results = []


    def get_waiting_time_results(self):
        pass

    def get_root_node_file(self, filename):
        tree = etree.parse(Simulation.project_directory + filename)
        return tree.getroot()

class DataVisualization(object):

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def add_data(self, data):
        for value in data:
            self.data.append(value)
