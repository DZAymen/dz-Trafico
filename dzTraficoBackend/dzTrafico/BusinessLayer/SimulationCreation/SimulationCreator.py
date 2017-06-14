from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager
from dzTrafico.BusinessEntities.Sensor import Sensor
from TripManager import TripManager
from dzTrafico.BusinessLayer.SimulationCreation.SensorsManager import SensorsManager

class SimulationCreator:

    __networkManager = NetworkManager()
    __sensorsManager = SensorsManager(__networkManager)
    __tripManager = TripManager(__networkManager)
    __simulation = Simulation()

    #Call NetworkManager to create map.net.xml
    def create_network_file(self, mapBox):
        self.network_file_path = SimulationCreator.__networkManager.get_network_file(mapBox)
        SimulationCreator.__simulation.set_network_file(self.network_file_path)

    #
    def create_sensors(self, sensors_distance):
        self.sensors, self.sensors_file = SimulationCreator.__sensorsManager.create_sensors(SimulationCreator.__simulation.get_flows(), sensors_distance)
        SimulationCreator.__simulation.add_sensors(self.sensors)
        SimulationCreator.__simulation.set_sensors_file(self.sensors_file)

    def define_traffic_flows(self, inFlowPoints, outFlowPoints):
        self.flows_file_path, self.flows = SimulationCreator.__tripManager.generate_flows_file(inFlowPoints, outFlowPoints)
        self.route_file = SimulationCreator.__tripManager.generate_route_file(self.flows_file_path)
        SimulationCreator.__simulation.set_flows(self.flows)
        SimulationCreator.__simulation.set_route_file(self.route_file)

    def define_vehicle_types(self, vehicle_types):
        SimulationCreator.__tripManager.add_vehicle_types(vehicle_types)

    #Create Simulation Config file 'map.sumocfg'
    def createSimulation(self):
        SimulationCreator.__simulation.create_sumo_config_file()
        return SimulationCreator.__simulation