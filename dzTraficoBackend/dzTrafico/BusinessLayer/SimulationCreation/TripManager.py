from dzTrafico.BusinessEntities.Flow import Flow
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.VehicleType import VehicleType
import subprocess, os
import lxml.etree as etree

class TripManager:

    __inflowPoints = []
    __outflowPoints = []
    flows_filename = "flows.xml"
    vehicle_types_filename = "vehicle.types.xml"

    def __init__(self, networkManager):
        self.__networkManager = networkManager
        self.vehicle_types_file_path = Simulation.project_directory + "..\\..\\data\\" + self.vehicle_types_filename

    # -------------------------------- Flows definition -------------------------------------------------
    # This method defines flows from flowPoints
    # and then generate the flow file which will be used
    # to generate route file
    def generate_flows_file(self, inFlowPoints, outFlowPoints):
        self.flows = self.generate_flows(inFlowPoints, outFlowPoints)
        return self.save_flows_xml_file(self.flows), self.flows

    #Define Flows from FlowPoints
    def generate_flows(self, inFlowPoints, outFlowPoints):
        flows = []
        outflows_sum = 0

        # Calculate outflow sum
        for outflowPoint in outFlowPoints:
            outflows_sum += outflowPoint.flow

        for inflowPoint in inFlowPoints:
            for outflowPoint in outFlowPoints:
                # set the start and end edges for a new flow
                flows.append(
                    Flow(
                        self.__networkManager.get_edgeId_from_geoCoord(inflowPoint.lon, inflowPoint.lat),
                        self.__networkManager.get_edgeId_from_geoCoord(outflowPoint.lon, outflowPoint.lat),
                        inflowPoint.departTime,
                        inflowPoint.flow * outflowPoint.flow / outflows_sum
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
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Incident lanes definition --------------------------------------
    def set_incident_lanes(self, incidents):
        for incident in incidents:
            edge = self.__networkManager.get_edge(self.__networkManager.get_edgeId_from_geoCoord(incident.lon, incident.lat))
            lane = edge.getLane(incident.lane)
            incident.set_lane(lane.getID())
            incident.set_lane_position(lane.getLength() - 20)
        return incidents
    # ---------------------------------------------------------------------------------------------------

    # ---------------------------------- Vehicle types defintion ----------------------------------------
    def add_vehicle_type(self, vehicle_type):
        current_type_id = vehicle_type.id
        #if it is already created, we append the new vehicle type
        if os.path.isfile(self.vehicle_types_file_path):
            # load vehicle.types.xml file
            tree = etree.parse(self.vehicle_types_file_path)
            root = tree.getroot()
            # Get the last element id
            if len(root.getchildren())>0:
                current_type_id = int(root.getchildren().pop().get('id')) + 1
                vehicle_type.id = current_type_id

        else:
            #else, we create a new root and we append the vehicle types
            root = etree.Element("vTypeDistribution", id="vtypedist")

        type_node = etree.Element("vType",
                                  accel=str(vehicle_type.accel),
                                  decel=str(vehicle_type.decel),
                                  length=str(vehicle_type.length),
                                  maxSpeed=str(vehicle_type.maxSpeed),
                                  minGap=str(vehicle_type.minGap),
                                  speedFactor=str(vehicle_type.speedFactor),
                                  sigma=str(vehicle_type.sigma),
                                  tau=str(vehicle_type.tau)
                                  )
        type_node.set("id",str(current_type_id))
        root.append(type_node)
        et = etree.ElementTree(root)
        et.write(self.vehicle_types_file_path, pretty_print=True)
        return self.vehicle_types_filename

    def set_vehicle_types_percentages(self, vehicle_types_percentages):
        if os.path.isfile(self.vehicle_types_file_path):
            # load vehicle.types.xml file
            tree = etree.parse(self.vehicle_types_file_path)
            root = tree.getroot()
            for vtype_percentage in vehicle_types_percentages:
                vtype = root.findall("*[@id='"+ vtype_percentage["id"] +"']")
                if len(vtype) > 0:
                    vtype[0].set("probability", str(vtype_percentage["percentage"]))
            et = etree.ElementTree(root)
            et.write(self.vehicle_types_file_path, pretty_print=True)

    def set_vehicle_types_in_route_file(self, route_filename):
        #load vehicle.types.xml file
        if os.path.isfile(self.vehicle_types_file_path) and os.path.isfile(Simulation.project_directory + "\\" + route_filename):
            # load vehicle.types.xml file
            tree = etree.parse(self.vehicle_types_file_path)
            vtypesdist = tree.getroot()
            vtypesdist_id = vtypesdist.get("id")

            #load map.route.xml file
            tree = etree.parse(Simulation.project_directory + "\\" + route_filename)
            map_route_root_node = tree.getroot()

            vtypesdistribution_node = map_route_root_node.findall("vTypeDistribution")
            if len(vtypesdistribution_node) > 0:
                vtypesdistribution_node[0].clear()
                for vtypes in vtypesdist.getchildren():
                    vtypesdistribution_node[0].append(vtypes)
            else:
                map_route_root_node.insert(0,vtypesdist)

            vehicles = map_route_root_node.findall("vehicle")

            for vehicle in vehicles:
                vehicle.set("type", vtypesdist_id)
                vehicle.set("departSpeed", "random")
                vehicle.set("departLane", "random")

            et = etree.ElementTree(map_route_root_node)
            et.write(Simulation.project_directory + "\\" + route_filename, pretty_print=True)

    def get_vehicle_types(self):
        if os.path.isfile(self.vehicle_types_file_path):
            # load vehicle.types.xml file
            tree = etree.parse(self.vehicle_types_file_path)
            root = tree.getroot()
            vtypes = root.getchildren()
            vehicle_types = []
            for vtype in vtypes:
                vehicleType = VehicleType(
                        float(vtype.get('maxSpeed')),
                        float(vtype.get('length')),
                        float(vtype.get('minGap')),
                        vtype.get('speedFactor'),
                        float(vtype.get('accel')),
                        float(vtype.get('decel')),
                        float(vtype.get('sigma')),
                        float(vtype.get('tau')),
                    )
                vehicleType.set_type_id(vtype.get('id'))
                vehicle_types.append(vehicleType)
            return vehicle_types
        else:
            return []
