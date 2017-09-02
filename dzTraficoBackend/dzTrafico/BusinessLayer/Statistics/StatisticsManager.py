from GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementsController
from DataVisualizationController import DataVisualizationController
from FlowMeasurements import FlowMeasurementsController

class StatisticsManager:

    def __init__(self, simulation):
        self.gpmController = GlobalPerformanceMeasurementsController(simulation)
        self.dataVisualizationController = DataVisualizationController(simulation)
        self.flowMeasurementsController = FlowMeasurementsController(simulation)

    def get_GPMs(self):
        return self.gpmController.get_trip_infos()

    def get_travel_time_results(self):
        return self.dataVisualizationController.get_travel_time_results()

    def get_waiting_time_results(self):
        return self.dataVisualizationController.get_waiting_time_results()

    def get_emissions_results(self):
        return self.dataVisualizationController.get_emissions_results()

    def get_incident_flow(self):
        return self.flowMeasurementsController.get_incident_flow_measurements()