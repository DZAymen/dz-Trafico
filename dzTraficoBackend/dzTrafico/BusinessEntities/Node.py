import traci

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