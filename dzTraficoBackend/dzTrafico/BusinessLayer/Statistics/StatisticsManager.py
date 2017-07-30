from GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementsController

class StatisticsManager:

    def __init__(self, simulation):
        self.gpmController = GlobalPerformanceMeasurementsController(simulation)

    def get_GPMs(self):
        gpm_results = self.gpmController.get_results()
        for gpm in gpm_results:
            print gpm.type, gpm.meanTravelTime