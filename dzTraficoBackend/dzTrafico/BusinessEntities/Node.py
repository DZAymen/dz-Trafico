from dzTrafico.Helpers.Converter import Converter
import traci

class Node(object):

    sensors = []
    edge = None
    initial_max_speed = 0
    current_vsl = 0
    previous_vsl = 0

    VSL_is_activated = False

    def __init__(self, edge, sensors):
        self.edge = edge
        self.sensors = sensors
        self.initial_max_speed = Converter.tokmh(edge.getSpeed())
        self.current_vsl = self.initial_max_speed
        self.previous_vsl = self.initial_max_speed

    def add_sensors(self, sensors):
        self.sensors.append(sensors)

    # ----------- Return previous and last step speed/density--------------------------------
    def get_current_speed(self):
        # print "--------------current speed ----------------------------"
        # print self.edge.getID()
        # print Converter.tokmh(traci.edge.getLastStepMeanSpeed(self.edge.getID()))
        # return Converter.tokmh(traci.edge.getLastStepMeanSpeed(self.edge.getID()))
        speed = 0
        for sensor in self.sensors:
            speed += sensor.get_last_step_speed()
        #     print Converter.tokmh(sensor.get_last_step_speed())
        # print speed
        # print (speed / len(self.sensors))
        return (speed / len(self.sensors))

    def get_previous_speed(self):
        #return Converter.tokmh(traci.edge.getLastStepMeanSpeed(self.edge.getID()))
        speed = 0
        for sensor in self.sensors:
            speed += sensor.get_previous_step_speed()
        return (speed / len(self.sensors))

    def get_current_density(self):
        density = 0
        for sensor in self.sensors:
            density += sensor.get_last_step_density()
        return density

    def get_previous_density(self):
            density = 0
            for sensor in self.sensors:
                density += sensor.get_previous_step_density()
            return density

    def get_current_vsl(self):
        # return Converter.tokmh(traci.edge.getMaxSpeed(self.edge.getID()))
        return self.current_vsl

    def get_previous_vsl(self):
        return self.previous_vsl

    # --------------- Check congestion state ------------------------------------------
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

    # --------------- VSL Control ------------------------------------------
    def activate_VSL(self):
        self.VSL_is_activated = True
        traci.edge.setMaxSpeed(self.edge.getID(), Converter.toms(self.current_vsl))

    def deactivate_VSL(self):
        self.VSL_is_activated = False
        traci.edge.setMaxSpeed(self.edge.getID(), Converter.toms(self.initial_max_speed))

    def set_current_vsl(self, max_speed):
        self.previous_vsl = self.current_vsl
        self.current_vsl = max_speed
        for sensor in self.sensors:
                sensor.set_high_level_speed(self.current_vsl * 0.75)

    #--------------- Lane Change Control ------------------------------------------
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
                # Change either way
                if recommendation.change_to_either_way:
                    # Calculate the percentage of vehicles to change to left
                    right_lane_occupancy = traci.lane.getLastStepOccupancy(
                        self.edge.getLane(recommendation.lane - 1).getID()
                    )
                    left_lane_occupancy = traci.lane.getLastStepOccupancy(
                        self.edge.getLane(recommendation.lane + 1).getID()
                    )
                    vehicles_number_turn_left = int(round(
                        len(vehicles) * right_lane_occupancy / (left_lane_occupancy + right_lane_occupancy)
                    ))
                    i = 0
                    for vehicle_id in vehicles:
                        if i < vehicles_number_turn_left:
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                            i += 1
                        else:
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                # Change vehicles position to target lane
                else:
                    print "------recommendation------"
                    print recommendation.target_lane
                    print "------Vehicles number------"
                    print len(vehicles)

                    for vehicle_id in vehicles:
                        traci.vehicle.changeLane(vehicle_id, recommendation.target_lane, 500000)
                        #traci.vehicle.changeSublane(vehicle_id, recommendation.target_lane - recommendation.lane)