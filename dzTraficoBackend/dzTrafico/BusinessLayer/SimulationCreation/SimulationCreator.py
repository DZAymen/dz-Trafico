from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager
from dzTrafico.BusinessEntities.Sensor import Sensor
from TripManager import TripManager

class SimulationCreator:

    __networkManager = NetworkManager()
    __tripManager = TripManager(__networkManager)
    __simulation = Simulation()

    #Call NetworkManager to create map.net.xml
    def create_network_file(self, mapBox):
        self.network_file_path = SimulationCreator.__networkManager.get_network_file(mapBox)
        SimulationCreator.__simulation.set_network_file(self.network_file_path)

    #
    def create_sensors(self):
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_0", -1, 50))
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_1", -1, 50))
        SimulationCreator.__simulation.add_sensors(Sensor("196547668#0_2", -1, 50))

    def define_traffic_flows(self, flowPoints):
        self.flows_file_path = SimulationCreator.__tripManager.generate_flows_file(flowPoints)
        self.route_file = SimulationCreator.__tripManager.generate_route_file(self.flows_file_path)
        SimulationCreator.__simulation.set_route_file(self.route_file)

    #Create Simulation Config file 'map.sumocfg'
    def createSimulation(self):
        SimulationCreator.__simulation.create_sumo_config_file()
        return SimulationCreator.__simulation