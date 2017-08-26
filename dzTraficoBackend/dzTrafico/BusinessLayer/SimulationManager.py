from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.Sensor import Sensor
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer
from dzTrafico.BusinessLayer.Statistics.StatisticsManager import StatisticsManager
from dzTrafico.BusinessLayer.TrafficAnalysis.LaneChangeControlAlgo import LaneChange
from dzTrafico.BusinessLayer.TrafficAnalysis.VirtualRampMeteringControlAlgo import VirtualRampMetering

class SimulationManager:

    __simulation = Simulation()
    __simulationCreator = SimulationCreator()
    __trafficAnalyzer = TrafficAnalyzer(__simulation)
    __statisticsManager = StatisticsManager(__simulation)

    incidents = []

    #Define a singleton SimulationManager class
    __simulationManager = None
    @staticmethod
    def get_instance():
        if SimulationManager.__simulationManager is None:
            SimulationManager.__simulationManager = SimulationManager()
        return SimulationManager.__simulationManager

    def get_simulation(self):
        return SimulationManager.__simulation

    # -------------------------------- Net file creation ------------------------------------------------
    #Call SimulationCreator.set_map method to create the map
    def set_map(self, map_box):
        self.__simulation = Simulation()
        self.__simulationCreator = SimulationCreator()
        self.__trafficAnalyzer = TrafficAnalyzer(self.__simulation)
        self.__statisticsManager = StatisticsManager(self.__simulation)
        # self.__simulationCreator.create_network_file(map_box)
        self.__simulationCreator.set_map_box(map_box)

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
        SimulationManager.incidents.append(incident)
        #SimulationManager.__simulationCreator.add_incidents(SimulationManager.incident)

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
        LaneChange.EdgeLength = sensors_distance

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
        SimulationManager.__simulationCreator.add_incidents(SimulationManager.incidents)
        self.generate_flows()
        self.generate_routes()

    def create_simulation(self, sim_duration):
        SimulationManager.__simulation = SimulationManager.__simulationCreator.createSimulation()
        SimulationManager.__simulation.set_duration(sim_duration)
    # ---------------------------------------------------------------------------------------------------

    # ----------------------------------------- Simulation Config ---------------------------------------
    def update_config(self, data):
        LaneChange.Xi = data["xi"]
        VirtualRampMetering.num_vsl_controlled_sections = data["num_vsl_sections"]
        VirtualRampMetering.V_min = data["v_min"]
        VirtualRampMetering.Ki = data["ki"]
        VirtualRampMetering.Cv = data["cv"]
        VirtualRampMetering.critical_density = data["critical_density"]
        Sensor.critical_density = data["critical_density_sensor"]
        Simulation.sim_step_duration = data["sim_step_duration"]

        TrafficAnalyzer.isVSLControlActivated = data["vslControl"]
        TrafficAnalyzer.isLCControlActivated = data["lcControl"]
        TrafficAnalyzer.isCongestionDetected = False
        TrafficAnalyzer.congestionExists = False

    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------ Simulation Results -------------------------------------------
    def get_simulation_gpm_results(self):
        return SimulationManager.__statisticsManager.get_GPMs()
    # ---------------------------------------------------------------------------------------------------