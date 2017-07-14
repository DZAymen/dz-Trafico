from dzTrafico.BusinessEntities.Sensor import Sensor
import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class SensorsManager():

    sensors = []

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    def create_sensors(self, flows, sensors_distance):
        primary_edges = self.__networkManager.get_edges(flows)
        # Split edges into equal segments
        edges = self.__networkManager.split_edges(primary_edges, sensors_distance)
        # Add sensors for each edge
        for edge in edges:
            #Calculate sensors number in the same edge from 0,1,2,..
            sensors_num = int(edge.getLength() / sensors_distance)
            #Get lanes number
            lanes_num = edge.getLaneNumber()
            #for each sensor position in sensors_num
            for i in range(0,sensors_num):
                #for each lane
                for j in range(0,lanes_num):
                    #We create a sensor
                    self.sensors.append(
                        Sensor(
                            edge.getLane(j).getID(),
                            i * sensors_distance,
                            edge.getSpeed() * 0.5
                        ))
        self.sensors_filename = self.create_sensors_file(self.sensors)
        return self.sensors, self.sensors_filename



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
