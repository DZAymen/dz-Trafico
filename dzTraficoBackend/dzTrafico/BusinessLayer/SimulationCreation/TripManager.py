from dzTrafico.BusinessEntities.Flow import FlowPoint, Flow
from dzTrafico.BusinessEntities.Simulation import Simulation
import os, subprocess
import lxml.etree as etree

class TripManager:

    __inflowPoints = []
    __outflowPoints = []
    flows_filename = "flows.xml"

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    # The goal of this method is to define flows from flowPoints
    # and then generate the flow file which will be included in
    # the simulation config file
    def generate_flows_file(self, flowPoints):
        self.flows = self.generate_flows(flowPoints)
        return self.save_flows_xml_file(self.flows)

    #Define Flows from FlowPoints
    def generate_flows(self, flowPoints):
        self.__inflowPoints = []
        self.__outflowPoints = []
        for flowPoint in flowPoints:
            if flowPoint.type == FlowPoint.startType:
                self.__inflowPoints.append(flowPoint)
            elif flowPoint.type == FlowPoint.endType:
                self.__outflowPoints.append(flowPoint)
        return self.define_flow_combinations(self.__inflowPoints, self.__outflowPoints)

    def define_flow_combinations(self, inflowPoints, outflowPoints):
        flows = []
        outflows_sum = 0

        #Calculate outflow sum
        for outflowPoint in outflowPoints:
            outflows_sum += outflowPoint.value

        for inflowPoint in inflowPoints:
            for outflowPoint in outflowPoints:
                # set the start and end edges for a new flow
                flows.append(
                    Flow(
                        self.__networkManager.get_edgeId_from_geoCoord(inflowPoint.lon, inflowPoint.lat),
                        self.__networkManager.get_edgeId_from_geoCoord(outflowPoint.lon, outflowPoint.lat),
                        inflowPoint.value * outflowPoint.value / outflows_sum
                    ))
        return flows

    def generate_route_file(self, flows_file_path):
        network_file = "map.net.xml"
        route_file = "map.rou.xml"

        subprocess.call(
            "duarouter -n " + Simulation.project_directory + "\\" + network_file
            + " -f " + flows_file_path
            + " -o " + Simulation.project_directory + "\\" + route_file
        )
        return route_file

    def save_flows_xml_file(self, flows):
        root = etree.Element("flowdefs")
        i = 0
        for flow in flows:
            flow_node = etree.Element("flow", id=str(i), to=str(flow.end_edge), vehsPerHour=str(flow.vehicles_per_hour))
            flow_node.set("from",str(flow.start_edge))
            root.append(flow_node)
            i += 1
        et = etree.ElementTree(root)
        et.write(Simulation.project_directory + "\\" + self.flows_filename, pretty_print=True)
        return Simulation.project_directory + "\\" + self.flows_filename
