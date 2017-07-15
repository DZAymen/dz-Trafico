
class Sensor(object):

    trafficAnalyzer = None

    __id = 1
    __lane = ""
    __position = 0
    __measures_list = []
    __critical_speed = 50

    def __init__(self, lane, position, critical_speed):
        self.__id = Sensor.__id
        Sensor.__id += 1
        self.__lane = lane
        self.__position = position
        self.__critical_speed = critical_speed

    def add_measure(self, speed):
        self.__measures_list.append(Measure(speed))
        self.__check_measure(speed)

    def __check_measure(self, speed):
        if speed < self.__critical_speed:
            #Notify TrafficAnalyzer
            Sensor.trafficAnalyzer.notify_congestion_detected(self.__lane)

    def get_sensor_id(self):
        return self.__id

    def get_sensor_lane(self):
        return self.__lane

    def get_sensor_position(self):
        return self.__position

class Measure(object):

    __speed = 0
    #__time_step

    def __init__(self, speed):
        self.__speed = speed

class Node(object):

    sensors = []
    edge = None
    initial_max_speed = 0
    current_max_speed = 0

    VSL_is_activated = False

    def __init__(self, edge, sensors):
        self.edge = edge
        self.sensors = sensors
        self.initial_max_speed = edge.getSpeed()

    def add_sensors(self, sensors):
        for sensor in sensors:
            self.sensors.append(sensor)

    def activate_VSL(self, max_speed):
        self.VSL_is_activated = True
        self.current_max_speed = max_speed

class Sink(object):

    nodes = []

    def __init__(self, nodes):
        self.nodes = nodes

    def add_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)

    def get_sensors(self):
        sensors = []
        for node in self.nodes:
            for sensor in node.sensors:
                sensors.append(sensor)
        return sensors