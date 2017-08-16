from dzTrafico.BusinessEntities.Sensor import Sensor
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.Node import Node
import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class SensorsManager():

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    def create_sensors(self, flows, incidents):

        print "-------------- Create sensors ----------------"

        sinks = []
        sensors_list = []
        # Get splitted edges
        edges_list = self.__networkManager.get_edges(flows)

        print "-------------- Edges List ----------------"
        print len(edges_list)

        for edges in edges_list:

            print "-------------- Edges ----------------"
            print edges

            # Add sensors for each edge
            sink = Sink()
            for edge in edges:
                #Get lanes number
                lanes_num = edge.getLaneNumber()
                sensors = []
                #for each lane
                for j in range(0,lanes_num):
                    #We create a sensor
                    sensors.append(
                        Sensor(
                            edge.getLane(j).getID(),
                            -1,
                            edge.getSpeed() * 0.25,
                            edge.getSpeed() * 0.65
                        )
                    )
                sink.add_node(
                    Node(
                        edge,
                        sensors
                    )
                )
            sink_sensors = sink.get_sensors()
            if len(sink_sensors) > 0:
                sinks.append(sink)
                for sensor in sink_sensors:
                    sensors_list.append(sensor)

            print "---------- Sensors List ------------"
            print len(sensors_list)

            print "---------- Sinks ------------"
            print len(sinks)
            for sinkk in sinks:
                print len(sinkk.get_sensors())

        incident_sensors = self.get_incidents_sensors(incidents)

        self.sensors_filename = self.create_sensors_file(sensors_list, incident_sensors)
        return sinks, sensors_list, self.sensors_filename

    def create_sensors_file(self, sensors, incident_sensors):
        sensors_filename = "sensors.xml"
        root = etree.Element("additional")
        for sensor in sensors:
            sensor_node = etree.Element("inductionLoop",
                                        id=str(sensor.get_sensor_id()),
                                        lane=str(sensor.get_sensor_lane()),
                                        pos=str(sensor.get_sensor_position()),
                                        freq=str(1000),
                                        file="sensors.output.xml")
        for sensor in incident_sensors:
            sensor_node = etree.Element("inductionLoop",
                                        id=str(sensor.get_sensor_id()),
                                        lane=str(sensor.get_sensor_lane()),
                                        pos=str(sensor.get_sensor_position()),
                                        freq=str(30),
                                        file="incident.sensors.output.xml")
            root.append(sensor_node)
        et = etree.ElementTree(root)
        et.write(Simulation.project_directory + "\\" + sensors_filename, pretty_print=True)
        return sensors_filename

    def get_incidents_sensors(self, incidents):
        sensors = []
        for incident in incidents:
            edge = self.__networkManager.get_edge_by_laneID(incident.lane_id)
            lanes = edge.getLanes()
            lanes.remove(edge.getLane(incident.lane))
            for lane in lanes:
                sensors.append(
                    Sensor(
                        lane.getID(),
                        incident.lane_position,
                        0,
                        0
                    )
                )
        return sensors