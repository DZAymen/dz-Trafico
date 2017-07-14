from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager
from dzTrafico.BusinessEntities.Sensor import Sensor
from TripManager import TripManager
from dzTrafico.BusinessLayer.SimulationCreation.SensorsManager import SensorsManager

class SimulationCreator:

    __simulation = Simulation()
    __networkManager = NetworkManager()
    __sensorsManager = SensorsManager(__networkManager)
    __tripManager = TripManager(__networkManager)

    # -------------------------------- Net file creation ------------------------------------------------
    #Call NetworkManager to create map.net.xml
    def create_network_file(self, mapBox):
        network_file_path = SimulationCreator.__networkManager.get_network_file(mapBox)
        SimulationCreator.__simulation.set_network_file(network_file_path)

    # Generate a new network file including splitted edges
    def split_network_edges(self, distance):
        SimulationCreator.__networkManager.generate_network_file_with_splitted_edges(
            SimulationCreator.__simulation.get_flows(),
            distance
        )
    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Flows definition -------------------------------------------------
    def define_traffic_flows(self, inFlowPoints, outFlowPoints):
        self.flows_file_path, self.flows = SimulationCreator.__tripManager.generate_flows_file(inFlowPoints, outFlowPoints)
        SimulationCreator.__simulation.set_flows(self.flows)

    def create_route_file(self):
        self.route_file = SimulationCreator.__tripManager.generate_route_file(self.flows_file_path)
        SimulationCreator.__simulation.set_route_file(self.route_file)
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Incident lanes definition --------------------------------------
    def add_incidents(self, incident):
        #Calculate each incident edge_id before setting them in simulation instance
        incident_updated_lanes = SimulationCreator.__tripManager.set_incident_lanes(incident)
        SimulationCreator.__simulation.add_incidents(incident_updated_lanes)
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Vehicle types defintion ----------------------------------------
    def add_vehicle_type(self, vehicle_type):
        SimulationCreator.__tripManager.add_vehicle_type(vehicle_type)

    def set_vehicle_types_percentages(self, vehicle_types_percentages):
        SimulationCreator.__tripManager.set_vehicle_types_percentages(vehicle_types_percentages)
        SimulationCreator.__tripManager.set_vehicle_types_in_route_file(SimulationCreator.__simulation.get_route_file())

    def get_vehicle_types(self):
        return SimulationCreator.__tripManager.get_vehicle_types()
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Add sensors -------------------------------------------------
    def create_sensors(self, sensors_distance):
        self.sensors, self.sensors_file = SimulationCreator.__sensorsManager.create_sensors(SimulationCreator.__simulation.get_flows())
        SimulationCreator.__simulation.add_sensors(self.sensors)
        SimulationCreator.__simulation.set_sensors_file(self.sensors_file)
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Simulation Creation -----------------------------------------
    #Create Simulation Config file 'map.sumocfg'
    def createSimulation(self):
        SimulationCreator.__simulation.create_sumo_config_file()
        return SimulationCreator.__simulation
    # ---------------------------------------------------------------------------------------------------
