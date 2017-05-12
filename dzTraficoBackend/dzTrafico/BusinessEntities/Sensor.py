
class Sensor(object):

    __id = 0
    __lane = 0
    __position = 0
    __measures_list = []
    __critical_speed = 50

    def __init__(self, lane, position, critical_speed):
        Sensor.__id += 1
        self.__lane = lane
        self.__position = position
        self.__critical_speed = critical_speed

    def add_measure(self, speed):
        self.__check_measure(speed)
        Sensor.__measures_list.append(Measure(speed))

    def __check_measure(self, speed):
        if speed < Sensor.__critical_speed:
            #Notify TrafficAnalyzer
            pass

class Measure(object):

    __speed = 0

    def __init__(self, speed):
        Measure.__speed = speed