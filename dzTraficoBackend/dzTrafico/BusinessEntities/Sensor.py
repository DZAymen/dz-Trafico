from dzTrafico.Helpers.Converter import Converter
import traci

class Sensor(object):

    id = 1
    __lane = ""
    __position = 0
    __measures_list = []
    __critical_speed = 0
    critical_density = 60
    __high_level_speed = 0

    previous_step_speed = 0
    last_step_speed = 0

    previous_step_density = 0
    last_step_density = 0

    def __init__(self, lane, position, critical_speed, high_level_speed):
        self.__id = Sensor.id
        Sensor.id += 1
        self.__lane = lane
        self.__position = position
        self.__critical_speed = Converter.tokmh(critical_speed)
        self.__high_level_speed = Converter.tokmh(high_level_speed)

    def check_traffic_state(self):
        speed = Converter.tokmh(traci.inductionloop.getLastStepMeanSpeed(str(self.__id)))
        density = self.get_density()
        self.add_measure(speed, density)
        return self.__check_measure_density(density)

    def check_clear_lane(self):
        density = self.get_density()
        speed = Converter.tokmh(traci.lane.getLastStepMeanSpeed(self.__lane))
        return (density == 0) or (speed > 15)

    def add_measure(self, speed, density):
        self.__measures_list.append(Measure(speed))

        self.previous_step_speed = self.last_step_speed
        self.last_step_speed = speed

        self.previous_step_density = self.last_step_density
        self.last_step_density = density

    def __check_measure_speed(self, speed):
        if (speed > 0) and (speed < self.__critical_speed):
            # Congestion
            return True
        return False

    def __check_measure_density(self, density):
        if density > self.critical_density and traci.lane.getLength(self.__lane)>200:
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

    def get_last_step_speed(self):
        return self.last_step_speed

    def get_previous_step_speed(self):
        return self.previous_step_speed

    def get_last_step_density(self):
        return self.last_step_density

    def get_previous_step_density(self):
        return self.previous_step_density

    def get_density(self):
        vehs_number = len(traci.lane.getLastStepVehicleIDs(self.__lane))
        lane_length = traci.lane.getLength(self.__lane)
        return (vehs_number * (1000 / lane_length))

    @staticmethod
    def set_critical_density(density):
        Sensor.critical_density = density/3


class Measure(object):

    __speed = 0
    #__time_step

    def __init__(self, speed):
        self.__speed = speed