from dzTrafico.Helpers.Converter import Converter
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
        self.initial_max_speed = Converter.tokmh(edge.getSpeed())
        self.current_max_speed = Converter.tokmh(self.initial_max_speed * 0.8)

    def add_sensors(self, sensors):
        self.sensors.append(sensors)

    def activate_VSL(self):
        self.VSL_is_activated = True
        traci.edge.setMaxSpeed(self.edge.getID(), Converter.toms(self.current_max_speed))

    def deactivate_VSL(self):
        self.VSL_is_activated = False
        traci.edge.setMaxSpeed(self.edge.getID(), Converter.toms(self.initial_max_speed))

    def set_current_max_speed(self, max_speed):
        self.current_max_speed = max_speed
        for sensor in self.sensors:
            sensor.set_high_level_speed(self.current_max_speed * 0.75)

    def check_congested_lanes(self):
        congested_lanes = []
        i = 0
        for sensor in self.sensors:
            if sensor.check_traffic_state():
                congested_lanes.append(i)
            i += 1
        return congested_lanes

    def check_if_discharged(self):
        is_discharged = False
        for sensor in self.sensors:
            is_discharged = is_discharged or sensor.check_discharged_area()
        return is_discharged

    def get_current_speed(self):
        return Converter.tokmh(traci.edge.getLastStepMeanSpeed(self.edge.getID()))

    def set_current_recommendations(self, recommendations):
        self.recommendations = recommendations

    def activate_LC(self):
        #self.LC_is_activated = True
        print "----------- Lane Change -----------"
        print self.edge.getID()

        self.change_lane()

    def change_lane(self):
        for recommendation in self.recommendations:
            if recommendation.change_lane:
                lane = self.edge.getLane(recommendation.lane)
                vehicles = traci.lane.getLastStepVehicleIDs(lane.getID())

                print "------recommendation------"
                print recommendation.target_lane

                for vehicle_id in vehicles:
                    traci.vehicle.changeLane(vehicle_id, recommendation.target_lane, 500000)