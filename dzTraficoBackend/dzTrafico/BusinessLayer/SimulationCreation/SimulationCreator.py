from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager
from dzTrafico.BusinessEntities.Sensor import Sensor

class SimulationCreator:

    __networkManager = NetworkManager()
    __simulation = Simulation()

    #Call NetworkManager to create map.net.xml
    def create_network_file(self, map_box):
        self.network_file_path = SimulationCreator.__networkManager.get_network_file(map_box)
        SimulationCreator.__simulation.set_network_file(self.network_file_path)

    #
    def create_sensors(self):
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_0", -1, 50))
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_1", -1, 50))
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_2", -1, 50))

    #Create Simulation Config file 'map.sumocfg'
    def createSimulation(self):
        SimulationCreator.__simulation.create_sumo_config_file()
        return SimulationCreator.__simulation