from dzTrafico.Helpers.MapManager.MapManager import MapManager

class SimulationCreator:

    __map_manager = MapManager()
    def set_map(self, map_box):
        return SimulationCreator.__map_manager.downloadMap(map_box)

    def createSimulation(self):
        pass