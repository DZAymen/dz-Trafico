
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