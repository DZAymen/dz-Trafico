import traci

class Sensor(object):

    __id = 1
    __lane = ""
    __position = 0
    __measures_list = []
    __critical_speed = 0
    __high_level_speed = 0

    def __init__(self, lane, position, critical_speed, high_level_speed):
        self.__id = Sensor.__id
        Sensor.__id += 1
        self.__lane = lane
        self.__position = position
        self.__critical_speed = critical_speed
        self.__high_level_speed = high_level_speed

    def check_traffic_state(self):
        speed = traci.inductionloop.getLastStepMeanSpeed(str(self.__id))
        self.add_measure(speed)
        return self.__check_measure(speed)

    def check_discharged_area(self):
        speed = traci.inductionloop.getLastStepMeanSpeed(str(self.__id))
        self.add_measure(speed)
        if speed > self.__high_level_speed:
            return True
        return False

    def add_measure(self, speed):
        self.__measures_list.append(Measure(speed))

    def __check_measure(self, speed):

        # print "-------- Edge ID --------"
        # print self.__id
        # print "-------- Speed --------"
        # print speed
        # print "-------- Critical_speed --------"
        # print self.__critical_speed

        if (speed > 0) and (speed < self.__critical_speed):
            # Congestion
            return True
        return False

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
        self.sensors.append(sensors)

    def activate_VSL(self):
        self.VSL_is_activated = True
        traci.edge.setMaxSpeed(self.edge.getID(), self.current_max_speed)

    def deactivate_VSL(self):
        self.VSL_is_activated = False
        traci.edge.setMaxSpeed(self.edge.getID(), self.initial_max_speed)

    def set_current_max_speed(self, max_speed):
        self.current_max_speed = max_speed

    def check_congested_lanes(self):
        congested_lanes = []
        i = 0
        for sensor in self.sensors:
            if sensor.check_traffic_state():
                congested_lanes.append(i)
            i += 1
        return congested_lanes

    def check_if_discharged(self):
        is_discharged = True
        for sensor in self.sensors:
            is_discharged = is_discharged and sensor.check_discharged_area()
        return is_discharged

class Sink(object):

    id = 0
    trafficAnalyzer = None
    nodes = []

    def __init__(self):
        self.id = Sink.id
        Sink.id += 1

        #print "--------nodes----------"
        #print len(nodes)

    def add_node(self, node):
        self.nodes.append(node)

    def get_sensors(self):
        sensors = []
        for node in self.nodes:
            for sensor in node.sensors:
                sensors.append(sensor)
        return sensors

    def read_traffic_state(self):
        for node in self.nodes:
            if node.VSL_is_activated:

                print "--------VSL_is_activated----------"
                print node.edge.getID()

                if node.check_if_discharged():
                    node.deactivate_VSL()

                    print "--------deactivate_VSL----------"
                    print node.edge.getID()
            else:
                congested_lanes = node.check_congested_lanes()
                if len(congested_lanes)>0:

                    print "--------notify_congestion_detected----------"
                    print node.edge.getID()
                    print congested_lanes

                    Sink.trafficAnalyzer.notify_congestion_detected(self, node, congested_lanes)