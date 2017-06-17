from dzTrafico.BusinessEntities.Flow import Flow
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.VehicleType import VehicleType
import subprocess
import lxml.etree as etree

class TripManager:

    __inflowPoints = []
    __outflowPoints = []
    flows_filename = "flows.xml"
    vehicle_types_filename = "vehicle.types.xml"

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    # The goal of this method is to define flows from flowPoints
    # and then generate the flow file which will be included in
    # the simulation config file
    def generate_flows_file(self, inFlowPoints, outFlowPoints):
        self.flows = self.generate_flows(inFlowPoints, outFlowPoints)
        return self.save_flows_xml_file(self.flows), self.flows

    #Define Flows from FlowPoints
    def generate_flows(self, inFlowPoints, outFlowPoints):
        flows = []
        outflows_sum = 0

        # Calculate outflow sum
        for outflowPoint in outFlowPoints:
            outflows_sum += outflowPoint.value

        for inflowPoint in inFlowPoints:
            for outflowPoint in outFlowPoints:
                # set the start and end edges for a new flow
                flows.append(
                    Flow(
                        self.__networkManager.get_edgeId_from_geoCoord(inflowPoint.lon, inflowPoint.lat),
                        self.__networkManager.get_edgeId_from_geoCoord(outflowPoint.lon, outflowPoint.lat),
                        inflowPoint.depart_time,
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
            flow_node = etree.Element("flow",
                                      id=str(i),
                                      to=str(flow.end_edge),
                                      begin=str(flow.depart_time),
                                      end=str(flow.end_depart_time),
                                      vehsPerHour=str(flow.vehicles_per_hour)
                                      )
            flow_node.set("from",str(flow.start_edge))
            root.append(flow_node)
            i += 1
        et = etree.ElementTree(root)
        et.write(Simulation.project_directory + "\\" + self.flows_filename, pretty_print=True)
        return Simulation.project_directory + "\\" + self.flows_filename

    def add_vehicle_types(self, vehicle_types):
        #load vehicle.types.xml file
        root = None
        #if it is already created, we append the new vehicle types
        #else, we create a new file and we append the vehicle types
        for vehicle_type in vehicle_types:
            type_node = etree.Element("vType",
                                      id=str(vehicle_type.type_id),
                                      accel=str(vehicle_type.acceleration),
                                      decel=str(vehicle_type.deceleration),
                                      length=str(vehicle_type.length),
                                      maxSpeed=str(vehicle_type.max_speed),
                                      minGap=str(vehicle_type.min_gap),
                                      speedFactor=str(vehicle_type.speed_factor),
                                      speedDev=str(vehicle_type.speed_dev),
                                      sigma=str(vehicle_type.sigma),
                                      tau=str(vehicle_type.tau)
                                      )
            root.append(type_node)
        et = etree.ElementTree(root)
        et.write(Simulation.project_directory + "\\..\\" + self.vehicle_types_filename, pretty_print=True)
        return self.vehicle_types_filename
