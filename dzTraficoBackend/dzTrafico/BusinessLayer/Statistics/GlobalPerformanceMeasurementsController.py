from dzTrafico.BusinessEntities.Simulation import Simulation
from rest_framework import serializers
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

        edges = []
        root = self.get_root_node_file(edge_dump_filename)
        # Get edges
        intervals = root.getchildren()
        for interval in intervals:
            for edge in interval.getchildren():
                edges.append(edge)

        for edge in edges:
            meanTravelTime += float(edge.get("traveltime"))
            meanWaintingTime += float(edge.get("waitingTime"))

        return meanTravelTime, meanWaintingTime

    def get_FuelCo2Nox(self, emissions_edge_dump_filename):
        fuel, co2, nox = 0, 0, 0
        edges = []
        # Get edges
        root = self.get_root_node_file(emissions_edge_dump_filename)
        intervals = root.getchildren()
        for interval in intervals:
            for edge in interval.getchildren():
                edges.append(edge)

        for edge in edges:
            fuel += float(edge.get("fuel_abs"))
            co2 += float(edge.get("CO2_abs"))
            nox += float(edge.get("NOx_abs"))

        return fuel, co2, nox

    "-------------------------- Trip Infos --------------------------------------------"

    def get_trip_infos(self):
        gpms = []

        noControl_GPM = self.get_trip_infos_GPM(
            self.simulation.trip_output,
            GlobalPerformanceMeasurement.NoControl
        )
        gpms.append(noControl_GPM)

        vsl_lc_GPM = self.get_trip_infos_GPM(
            self.simulation.trip_output_vsl_lc,
            GlobalPerformanceMeasurement.VSL_LC
        )
        gpms.append(vsl_lc_GPM)

        return gpms

    def get_trip_infos_GPM(self, trip_output_filename, type):
        meanTravelTime, meanWaitingTime, numLC, fuel, co2, nox = 0,0,0,0,0,0

        root = self.get_root_node_file(trip_output_filename)
        trip_infos = root.getchildren()

        depart = self.get_incident_depart_time(root)
        i = 0
        for trip_info in trip_infos:
            if float(trip_info.get("depart")) > depart:
                meanTravelTime += float(trip_info.get("duration"))
                meanWaitingTime += float(trip_info.get("waitSteps"))
                emissions_info = trip_info.getchildren()[0]
                fuel += float(emissions_info.get("fuel_abs"))
                co2 += float(emissions_info.get("CO2_abs"))
                nox += float(emissions_info.get("NOx_abs"))
                i += 1

        print "----------- trips: " + str(type) + "-------------"
        print i

        meanTravelTime /= len(trip_infos)
        meanWaitingTime /= len(trip_infos)

        return GlobalPerformanceMeasurement(
            type,
            meanTravelTime,
            meanWaitingTime,
            numLC,
            fuel,
            co2,
            nox
        )

    def get_incident_depart_time(self, root):
        trip_info = root.findall("*[@id='" + str(Simulation.incident_veh) + "']")[0]

        print "------------ depart ---------------------"
        print float(trip_info.get("depart"))

        return float(trip_info.get("depart"))


class GlobalPerformanceMeasurement(object):

    NoControl = "no control"
    VSL = "vsl"
    LC = "lc"
    VSL_LC = "vsl_lc"

    def __init__(self, type, meanTravelTime, meanWaitingTime, numLC, fuel, co2, nox):
        self.type = type
        self.meanTravelTime = meanTravelTime
        self.meanWaitingTime = meanWaitingTime
        self.numLC = numLC
        self.fuel = fuel
        self.co2 = co2
        self.nox = nox

class GlobalPerformanceMeasurementSerializer(serializers.Serializer):

    type = serializers.CharField()
    meanTravelTime = serializers.FloatField()
    meanWaitingTime = serializers.FloatField()
    numLC = serializers.FloatField()
    fuel = serializers.FloatField()
    co2 = serializers.FloatField()
    nox = serializers.FloatField()