from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager

class SimulationCreator:

    __networkManager = NetworkManager()
    __simulation = Simulation()

    def create_network_file(self, map_box):
        self.network_file_path = SimulationCreator.__networkManager.get_network_file(map_box)
        SimulationCreator.__simulation.set_network_file(self.network_file_path)

    def createSimulation(self):
        return SimulationCreator.__simulation