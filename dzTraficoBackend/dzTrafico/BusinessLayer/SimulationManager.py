from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.Sensor import Sensor
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

    #Call SimulationCreator.set_map method to create the map
    def set_map(self, map_box):
        SimulationManager.__simulationCreator.create_network_file(map_box)

    # Call SimulationCreator.set_map method to create the map
    def add_sensors(self, sensors_distance):
        Sensor.trafficAnalyzer = SimulationManager.__trafficAnalyzer
        SimulationManager.__simulationCreator.create_sensors(sensors_distance)

    # Call SimulationCreator.set_map method to create the map
    def set_traffic_flow(self, inFlowPoints, outFlowPoints):
        SimulationManager.__simulationCreator.define_traffic_flows(inFlowPoints, outFlowPoints)

    # Call SimulationCreator.set_map method to create the map
    def add_incidents(self, incidents):
        return None

    def add_vehicule_types(self, vehicle_types):
        SimulationManager.__simulationCreator.add_vehicle_types(vehicle_types)

    # Call SimulationCreator.set_map method to create the map
    def create_simulation(self):
        SimulationManager.__simulation = SimulationManager.__simulationCreator.createSimulation()
        SimulationManager.__simulation.start_simulation()