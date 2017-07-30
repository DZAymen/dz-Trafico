
class GlobalPerformanceMeasurementsController:

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_results(self):
        pass

class GlobalPerformanceMeasurement(object):

    NoControl = "no control"
    VSL = "vsl"
    LC = "lc"
    VSL_LC = "vsl_lc"

    def __init__(self, type, meanTravelTime, numStops, numLC, fuel, co2, nox):
        self.type = type
        self.meanTravelTime = meanTravelTime
        self.numStops = numStops
        self.numLC = numLC
        self.fuel = fuel
        self.co2 = co2
        self.nox = nox