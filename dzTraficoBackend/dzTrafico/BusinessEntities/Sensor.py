from dzTrafico.Helpers.Converter import Converter
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
        self.__critical_speed = Converter.tokmh(critical_speed)
        self.__high_level_speed = Converter.tokmh(high_level_speed)

    def check_traffic_state(self):
        speed = Converter.tokmh(traci.inductionloop.getLastStepMeanSpeed(str(self.__id)))
        self.add_measure(speed)
        return self.__check_measure(speed)

    def check_discharged_area(self):
        speed = Converter.tokmh(traci.inductionloop.getLastStepMeanSpeed(str(self.__id)))
        self.add_measure(speed)

        print "-------Check discharged Area--------"
        print speed
        print self.__high_level_speed
        print speed > self.__high_level_speed
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

    def set_high_level_speed(self, high_speed):
        self.__high_level_speed = high_speed

class Measure(object):

    __speed = 0
    #__time_step

    def __init__(self, speed):
        self.__speed = speed