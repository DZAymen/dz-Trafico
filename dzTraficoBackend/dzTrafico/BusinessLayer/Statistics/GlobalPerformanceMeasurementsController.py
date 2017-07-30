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
        meanTravelTime, meanWaitingTime = self.get_meanTravelAndWaintingTime(self.simulation.edge_dump_filename)
        numLC = self.get_numLaneChange(self.simulation.lanechange_summary_filename)
        fuel, co2, nox = self.get_FuelCo2Nox(self.simulation.emissions_edge_dump_filename)

        return GlobalPerformanceMeasurement(
            GlobalPerformanceMeasurement.NoControl,
            meanTravelTime,
            meanWaitingTime,
            numLC,
            fuel,
            co2,
            nox
        )

    def get_vsl_lc_GPM(self):
        # Read values from summary files
        meanTravelTime, meanWaitingTime = self.get_meanTravelAndWaintingTime(self.simulation.edge_dump_vsl_lc_filename)
        numLC = self.get_numLaneChange(self.simulation.lanechange_summary_vsl_lc_filename)
        fuel, co2, nox = self.get_FuelCo2Nox(self.simulation.emissions_edge_dump_vsl_lc_filename)

        return GlobalPerformanceMeasurement(
            GlobalPerformanceMeasurement.VSL_LC,
            meanTravelTime,
            meanWaitingTime,
            numLC,
            fuel,
            co2,
            nox
        )

    def get_root_node_file(self, filename):
        tree = etree.parse(Simulation.project_directory + filename)
        return tree.getroot()

    def get_numLaneChange(self, lanechange_filename):
        root = self.get_root_node_file(lanechange_filename)
        return len(root.getchildren())

    def get_meanTravelAndWaintingTime(self, edge_dump_filename):
        meanTravelTime = 0
        meanWaintingTime = 0

        root = self.get_root_node_file(edge_dump_filename)
        edges = root.getchildren()
        for edge in edges:
            meanTravelTime += edge.get("traveltime")
            meanWaintingTime += edge.get("waitingTime")

        return meanTravelTime, meanWaintingTime

    def get_FuelCo2Nox(self, emissions_edge_dump_filename):
        fuel, co2, nox = 0, 0, 0

        root = self.get_root_node_file(emissions_edge_dump_filename)
        edges = root.getchildren()
        for edge in edges:
            fuel += edge.get("fuel_abs")
            co2 += edge.get("CO2_abs")
            nox += edge.get("NOx_abs")

        return fuel, co2, nox

class GlobalPerformanceMeasurement(object):

    NoControl = "no control"
    VSL = "vsl"
    LC = "lc"
    VSL_LC = "vsl_lc"

    def __init__(self, type, meanTravelTime, meanWaitingTime, numLC, fuel, co2, nox):
        self.type = type
        self.meanTravelTime = meanTravelTime
        self.numStops = meanWaitingTime
        self.numLC = numLC
        self.fuel = fuel
        self.co2 = co2
        self.nox = nox