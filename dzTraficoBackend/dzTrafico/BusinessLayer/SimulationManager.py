from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer

class SimulationManager:

    __simulation = Simulation()
    __simulationCreator = SimulationCreator()
    __trafficAnalyzer = TrafficAnalyzer(__simulation)

    #Define a singleton SimulationManager class
    __simulationManager = None
    @staticmethod
    def get_instance():
        if SimulationManager.__simulationManager is None:
            SimulationManager.__simulationManager = SimulationManager()
        return SimulationManager.__simulationManager

    # -------------------------------- Net file creation ------------------------------------------------
    #Call SimulationCreator.set_map method to create the map
    def set_map(self, map_box):
        SimulationManager.__simulationCreator.create_network_file(map_box)
    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Flows definition -------------------------------------------------
    def add_inflow(self, inFlowPoint):
        SimulationManager.__simulation.add_inflows(inFlowPoint)

    def add_outflow(self, outFlowPoint):
        SimulationManager.__simulation.add_outflows(outFlowPoint)

    def generate_flows(self):
        if (len(SimulationManager.__simulation.inFlowPoints) > 0) and (
            len(SimulationManager.__simulation.outFlowPoints) > 0):
            SimulationManager.__simulationCreator.define_traffic_flows(
                SimulationManager.__simulation.inFlowPoints,
                SimulationManager.__simulation.outFlowPoints
            )

    def generate_routes(self):
        SimulationManager.__simulationCreator.create_route_file()

    def get_inflow_points(self):
        return SimulationManager.__simulation.get_inflows()

    def get_outflow_points(self):
        return SimulationManager.__simulation.get_outflows()

    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Incidents definition ---------------------------------------------
    # Call SimulationCreator.set_map method to create the map
    def add_incident(self, incident):
        SimulationManager.__simulationCreator.add_incidents(incident)

    def get_incidents(self):
        return SimulationManager.__simulation.get_incidents()
    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Vehicle types definition -----------------------------------------
    def add_vehicule_type(self, vehicle_type):
        SimulationManager.__simulationCreator.add_vehicle_type(vehicle_type)

    def set_vehicle_types_percentages(self, vehicle_types_percentages):
        SimulationManager.__simulationCreator.set_vehicle_types_percentages(vehicle_types_percentages)

    def get_vehicle_types(self):
        return SimulationManager.__simulationCreator.get_vehicle_types()
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Add sensors -------------------------------------------------
    def add_sensors(self, sensors_distance):
        Sink.trafficAnalyzer = SimulationManager.__trafficAnalyzer
        SimulationManager.__simulationCreator.create_sensors(sensors_distance)
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Simulation Creation -----------------------------------------
    # Split network edges
    # && update network file
    # && generate route file
    def split_network_edges(self, sensors_distance):
        self.generate_flows()
        SimulationManager.__simulationCreator.split_network_edges(sensors_distance)
        self.generate_flows()
        self.generate_routes()

    def create_simulation(self):
        SimulationManager.__simulation = SimulationManager.__simulationCreator.createSimulation()
        SimulationManager.__simulation.start_simulation()
    # ---------------------------------------------------------------------------------------------------