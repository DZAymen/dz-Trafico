from GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementsController
from DataVisualizationController import DataVisualizationController

class StatisticsManager:

    def __init__(self, simulation):
        self.gpmController = GlobalPerformanceMeasurementsController(simulation)
        self.dataVisualizationController = DataVisualizationController(simulation)

    def get_GPMs(self):
        gpm_results = self.gpmController.get_results()
        return gpm_results

    def get_travel_time_results(self):
        return self.dataVisualizationController.get_travel_time_results()

    def get_waiting_time_results(self):
        return self.dataVisualizationController.get_waiting_time_results()

    def get_emissions_results(self):
        return self.dataVisualizationController.get_emissions_results()