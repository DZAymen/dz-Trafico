from dzTrafico.BusinessEntities.Simulation import Simulation
from NetworkManager import NetworkManager
from dzTrafico.BusinessLayer.TrafficAnalysis.LaneChangeControlAlgo import LaneChange
from TripManager import TripManager
from dzTrafico.BusinessLayer.SimulationCreation.SensorsManager import SensorsManager

class SimulationCreator:

    __simulation = Simulation()
    __networkManager = NetworkManager()
    __sensorsManager = SensorsManager(__networkManager)
    __tripManager = TripManager(__networkManager)

    # -------------------------------- Net file creation ------------------------------------------------
    def set_map_box(self, mapBox):
        SimulationCreator.__simulation.set_map_box(mapBox)

    #Call NetworkManager to create map.net.xml
    def create_network_file(self):
        project_directory = SimulationCreator.__networkManager.create_project_directory()
        network_file_path = SimulationCreator.__networkManager.get_network_file(
            SimulationCreator.__simulation.get_map_box()
        )
        SimulationCreator.__simulation.set_project_directory_path(project_directory)
        SimulationCreator.__simulation.set_network_file(network_file_path)

    # Generate a new network file including splitted edges
    def split_network_edges(self):
        SimulationCreator.__networkManager.generate_network_file_with_splitted_edges(
            SimulationCreator.__simulation.get_flows(),
            SimulationCreator.__simulation.get_sensors_distance()
        )
    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Flows definition -------------------------------------------------
    def define_traffic_flows(self, inFlowPoints, outFlowPoints):
        self.flows_file_path, self.flows = SimulationCreator.__tripManager.generate_flows_file(inFlowPoints, outFlowPoints)
        SimulationCreator.__simulation.set_flows(self.flows)

    def create_route_file(self):
        self.route_file = SimulationCreator.__tripManager.generate_route_file(self.flows_file_path)
        SimulationCreator.__tripManager.set_vehicle_types_in_route_file(self.route_file)
        SimulationCreator.__simulation.set_route_file(self.route_file)
        SimulationCreator.__simulation.add_vehicle_types(self.get_vehicle_types())

    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Incident lanes definition --------------------------------------
    def add_incidents(self, incidents):
        #Calculate each incident edge_id before setting them in simulation instance
        incident_updated_lanes = SimulationCreator.__tripManager.set_incident_lanes(incidents)
        SimulationCreator.__simulation.add_incidents(incident_updated_lanes)
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Vehicle types defintion ----------------------------------------
    def add_vehicle_type(self, vehicle_type):
        SimulationCreator.__tripManager.add_vehicle_type(vehicle_type)
        SimulationCreator.__simulation.add_vehicle_types(vehicle_type)

    def set_vehicle_types_percentages(self, vehicle_types_percentages):
        SimulationCreator.__tripManager.set_vehicle_types_percentages(vehicle_types_percentages)

    def get_vehicle_types(self):
        return SimulationCreator.__tripManager.get_vehicle_types()
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Add sensors -------------------------------------------------
    def set_sensors_distance(self, distance):
        SimulationCreator.__simulation.set_sensors_distance(distance)

    def create_sensors(self):
        LaneChange.EdgeLength = SimulationCreator.__simulation.get_sensors_distance()

        self.sinks, self.sensors, self.sensors_file = SimulationCreator.__sensorsManager.create_sensors(
            SimulationCreator.__simulation.get_flows(),
            SimulationCreator.__simulation.get_incidents()
        )
        SimulationCreator.__simulation.add_sensors(self.sensors)
        SimulationCreator.__simulation.add_sinks(self.sinks)
        SimulationCreator.__simulation.set_sensors_file(self.sensors_file)
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Simulation Creation -----------------------------------------
    def set_sim_duration(self, duration):
        SimulationCreator.__simulation.set_duration(duration)

    #Create Simulation Config file 'map.sumocfg'
    def createSimulation(self):
        SimulationCreator.__simulation.create_sumo_config_file()
        return SimulationCreator.__simulation
    # ---------------------------------------------------------------------------------------------------
