from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.Sensor import Sensor
from dzTrafico.BusinessEntities.Node import Node
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
        SimulationManager.incidents = []
        self.__simulation = Simulation()
        self.__simulationCreator = SimulationCreator()
        self.__trafficAnalyzer = TrafficAnalyzer(self.__simulation)
        self.__statisticsManager = StatisticsManager(self.__simulation)
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

    def delete_traffic_outflow(self, id):
        SimulationManager.__simulation.delete_outflow(id)

    def delete_traffic_inflow(self, id):
        SimulationManager.__simulation.delete_inflow(id)

    # ---------------------------------------------------------------------------------------------------

    # -------------------------------- Incidents definition ---------------------------------------------
    # Call SimulationCreator.set_map method to create the map
    def add_incident(self, incident):
        SimulationManager.incidents.append(incident)
        #SimulationManager.__simulationCreator.add_incidents(SimulationManager.incident)

    def get_incidents(self):
        return SimulationManager.incidents

    def delete_incident(self, id):
        for incident in SimulationManager.incidents:
            if incident.id == int(id):
                SimulationManager.incidents.remove(incident)
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
    def set_sensors_distance(self, distance):
        SimulationManager.__simulationCreator.set_sensors_distance(distance)

    def add_sensors(self):
        Sink.trafficAnalyzer = SimulationManager.__trafficAnalyzer
        SimulationManager.__simulationCreator.create_sensors()
    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------- Simulation Creation -----------------------------------------
    # Split network edges
    # && update network file
    # && generate route file
    def split_network_edges(self):
        self.generate_flows()
        SimulationManager.__simulationCreator.split_network_edges()
        SimulationManager.__simulationCreator.add_incidents(SimulationManager.incidents)
        self.generate_flows()
        self.generate_routes()

    def create_simulation(self, consumer):
        print "download map"
        consumer.send("download map")
        self.__simulationCreator.create_network_file()
        consumer.send("map is downloaded")
        print "map downloaded"
        self.split_network_edges()
        consumer.send("Network is splitted")
        self.add_sensors()
        consumer.send("Sensors are added correctly")
        SimulationManager.__simulation = SimulationManager.__simulationCreator.createSimulation()
        consumer.send("Simulation is created successfully")
    # ---------------------------------------------------------------------------------------------------

    # ----------------------------------------- Simulation Config ---------------------------------------
    def update_config(self, data):
        LaneChange.Xi = data["xi"]
        VirtualRampMetering.num_vsl_controlled_sections = data["num_vsl_sections"]
        VirtualRampMetering.V_min = data["v_min"]
        VirtualRampMetering.Ki = data["ki"]
        VirtualRampMetering.Cv = data["cv"]
        VirtualRampMetering.critical_density = data["critical_density"]
        Sensor.set_critical_density(data["critical_density"])
        Simulation.sim_step_duration = data["sim_step_duration"]
        SimulationManager.__simulationCreator.set_sim_duration(data["simDuration"])

        TrafficAnalyzer.isVSLControlActivated = True
        TrafficAnalyzer.isLCControlActivated = True
        TrafficAnalyzer.isCongestionDetected = False
        TrafficAnalyzer.congestionExists = False

        self.set_sensors_distance(data["distance"])

        Node.COMPLIANCE_PERCENTAGE = data["driver_compliance"] / 100

        if Node.COMPLIANCE_PERCENTAGE < 1:
            Simulation.LCMode_vsl_lc = 597
        else:
            Simulation.LCMode_vsl_lc = 512

    # ---------------------------------------------------------------------------------------------------

    # ------------------------------------ Simulation Results -------------------------------------------
    def get_simulation_gpm_results(self):
        return SimulationManager.__statisticsManager.get_GPMs()

    def get_incident_flow(self):
        return SimulationManager.__statisticsManager.get_incident_flow()

    def get_incident_density(self):
        return SimulationManager.__statisticsManager.get_incident_density()

    def get_queue_measurements(self):
        return SimulationManager.__statisticsManager.get_queue_measurements()
    # ---------------------------------------------------------------------------------------------------