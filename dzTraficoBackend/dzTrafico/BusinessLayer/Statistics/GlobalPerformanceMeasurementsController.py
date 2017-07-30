from dzTrafico.BusinessEntities.Simulation import Simulation
import lxml.etree as etree

class GlobalPerformanceMeasurementsController:

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_results(self):
        gpms = []

        noControl_GPM = self.get_no_control_GPM()
        gpms.append(noControl_GPM)

        vsl_lc_GPM = self.get_vsl_lc_GPM()
        gpms.append(vsl_lc_GPM)

        return gpms

    def get_no_control_GPM(self):
        # Read values from summary files
        meanTravelTime = 0
        numStops = 0
        numLC = self.get_num_lanechange(
            self.simulation.lanechange_summary_filename
        )
        fuel = 0
        co2 = 0
        nox = 0

        return GlobalPerformanceMeasurement(
            GlobalPerformanceMeasurement.NoControl,
            meanTravelTime,
            numStops,
            numLC,
            fuel,
            co2,
            nox
        )

    def get_vsl_lc_GPM(self):
        # Read values from summary files
        meanTravelTime = 0
        numStops = 0
        numLC = self.get_num_lanechange(
            self.simulation.lanechange_summary_vsl_lc_filename
        )
        fuel = 0
        co2 = 0
        nox = 0

        return GlobalPerformanceMeasurement(
            GlobalPerformanceMeasurement.VSL_LC,
            meanTravelTime,
            numStops,
            numLC,
            fuel,
            co2,
            nox
        )

    def get_num_lanechange(self, lanechange_filename):
        root = self.get_root_node_file(lanechange_filename)
        return len(root.getchildren())

    def get_root_node_file(self, filename):
        tree = etree.parse(Simulation.project_directory + filename)
        return tree.getroot()

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