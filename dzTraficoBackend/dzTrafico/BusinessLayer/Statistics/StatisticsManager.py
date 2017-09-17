from GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementsController
from DataVisualizationController import DataVisualizationController
from FlowMeasurements import FlowMeasurementsController
from QueueMeasurements import QueueMeasurementsController

class StatisticsManager:

    def __init__(self, simulation):
        self.simulation = simulation
        self.gpmController = GlobalPerformanceMeasurementsController(simulation)
        self.dataVisualizationController = DataVisualizationController(simulation)
        self.flowMeasurementsController = FlowMeasurementsController(simulation)
        self.queueMeasurementsController = QueueMeasurementsController(simulation)

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

    def get_incident_density(self):
        density = dict()
        density["time"] = self.simulation.time
        density["density_control"] = self.simulation.densities
        density["density_no_control"] = self.simulation.nocontrol_densities
        return density

    def get_queue_measurements(self):
        self.queueMeasurementsController.get_queue_measurements()