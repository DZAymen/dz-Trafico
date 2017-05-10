from dzTrafico.Helpers.MapManager import MapManager
from dzTrafico.BusinessEntities.Simulation import Simulation

class SimulationCreator:

    __map_manager = MapManager()
    __simulation = Simulation()

    def set_map(self, map_box):
        SimulationCreator.__simulation.set_osm_file(SimulationCreator.__map_manager.download_map(map_box))

    def createSimulation(self):
        return SimulationCreator.__simulation