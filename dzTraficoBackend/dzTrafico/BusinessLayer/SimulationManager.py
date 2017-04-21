from dzTrafico.BusinessLayer.SimulationCreation.SimulationCreator import SimulationCreator

class SimulationManager:

    __simulationCreator = SimulationCreator()

    #Define a singleton SimulationManager
    __simulationManager = None
    @staticmethod
    def get_instance():
        if SimulationManager.__simulationManager is None:
            SimulationManager.__simulationManager = SimulationManager()
        return SimulationManager.__simulationManager

    #Call SimulationCreator.set_map method to create the map
    def set_map(self, leftbottom, righttop):
        SimulationManager.__simulationCreator.set_map(leftbottom, righttop)

    # Call SimulationCreator.set_map method to create the map
    def add_sensors(self, sensors):
        return None

    # Call SimulationCreator.set_map method to create the map
    def set_traffic_flow(self, traffic_flow):
        return None

    # Call SimulationCreator.set_map method to create the map
    def add_incidents(self, incidents):
        return None

    # Call SimulationCreator.set_map method to create the map
    def createSimulation(self):
        SimulationManager.__simulationCreator.createSimulation()