from dzTrafico.BusinessEntities.Sensor import Sensor
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.Node import Node
import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class SensorsManager():

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    def create_sensors(self, flows):
        sinks = []
        # Get splitted edges
        edges = self.__networkManager.get_edges(flows)
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
                        edge.getSpeed() * 0.5,
                        edge.getSpeed() * 0.65
                    )
                )
            sink.add_node(
                Node(
                    edge,
                    sensors
                )
            )
        sinks.append(sink)
        sensors = sink.get_sensors()
        self.sensors_filename = self.create_sensors_file(sensors)
        return sinks, sensors, self.sensors_filename

    def create_sensors_file(self, sensors):
        sensors_filename = "sensors.xml"
        root = etree.Element("additional")
        for sensor in sensors:
            sensor_node = etree.Element("inductionLoop",
                                        id=str(sensor.get_sensor_id()),
                                        lane=str(sensor.get_sensor_lane()),
                                        pos=str(sensor.get_sensor_position()),
                                        freq=str(1000),
                                        file="sensors.output.xml")
            root.append(sensor_node)
        et = etree.ElementTree(root)
        et.write(Simulation.project_directory + "\\" + sensors_filename, pretty_print=True)
        return sensors_filename
