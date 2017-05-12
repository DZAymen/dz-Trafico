from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator
from dzTrafico.BusinessEntities.Simulation import Simulation

class SimulationManager:

    __simulation = Simulation()
    __simulationCreator = SimulationCreator()

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
    def add_sensors(self, sensors):
        SimulationManager.__simulationCreator.create_sensors()

    # Call SimulationCreator.set_map method to create the map
    def set_traffic_flow(self, traffic_flow):
        return None

    # Call SimulationCreator.set_map method to create the map
    def add_incidents(self, incidents):
        return None

    # Call SimulationCreator.set_map method to create the map
    def create_simulation(self):
        SimulationManager.__simulation = SimulationManager.__simulationCreator.createSimulation()
        SimulationManager.__simulation.start_simulation()