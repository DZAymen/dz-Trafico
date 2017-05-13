
class Sensor(object):

    traffic_analyzer = None

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
        self.__check_measure(speed)
        self.__measures_list.append(Measure(speed))

    def __check_measure(self, speed):
        Sensor.traffic_analyzer.notify(self.__id)
        print speed
        if speed < self.__critical_speed:
            #Notify TrafficAnalyzer
            pass

    def get_sensor_id(self):
        return self.__id


class Measure(object):

    __speed = 0

    def __init__(self, speed):
        self.__speed = speed