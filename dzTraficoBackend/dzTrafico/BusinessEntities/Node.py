from dzTrafico.Helpers.Converter import Converter
import traci

class Node(object):

    sensors = []
    edge = None
    initial_max_speed = 0
    current_vsl = 0
    previous_vsl = 0

    recommendations = []
    previous_nodes_of_discharged_area = []

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
        speed = 0
        for sensor in self.sensors:
            speed += sensor.get_last_step_speed()
        return (speed / len(self.sensors))

    def get_previous_speed(self):
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
        return self.current_vsl

    def get_previous_vsl(self):
        return self.previous_vsl

    def reset_previous_speed(self):
        self.previous_vsl = self.initial_max_speed

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
        is_discharged = True
        for sensor in self.sensors:
            is_discharged = is_discharged and sensor.check_discharged_area()
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
                edge_vehicles = traci.edge.getLastStepVehicleIDs(self.edge.getID())

                for veh_id in edge_vehicles:
                    traci.vehicle.setLaneChangeMode(veh_id, 512)

                vehicles = traci.lane.getLastStepVehicleIDs(lane.getID())
                # Change either way
                if recommendation.change_to_either_way:
                    # Calculate the percentage of vehicles to change to left

                    i = 0
                    j = 0

                    print "------recommendation------"
                    print recommendation.change_to_either_way
                    print "------Vehicles number------"
                    print len(vehicles)
                    
                    for vehicle_id in vehicles:
                        # Turn Left
                        print "----Change to left? " + str(traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane + 1)) + "   veh_id-->" +str(vehicle_id)
                        print "----Change to right? " + str(traci.vehicle.couldChangeLane(vehicle_id,recommendation.lane - 1)) + "   veh_id-->" + str(vehicle_id)

                        if traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane + 1):
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                            # traci.vehicle.changeSublane(vehicle_id, 100)
                            print "--------Change to Left--------> " + str(vehicle_id)
                            i +=1
                        # Turn Right
                        elif traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane - 1):
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                            # traci.vehicle.changeSublane(vehicle_id, -100)
                            j +=1
                            print "--------Change to Right--------> " + str(vehicle_id)
                        else:
                            right_lane_occupancy = traci.lane.getLastStepOccupancy(
                                self.edge.getLane(recommendation.lane - 1).getID()
                            )
                            left_lane_occupancy = traci.lane.getLastStepOccupancy(
                                self.edge.getLane(recommendation.lane + 1).getID()
                            )

                            print "--- occup:" + str(right_lane_occupancy>left_lane_occupancy)
                            if right_lane_occupancy>left_lane_occupancy:
                                traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                                print "--------Change to Left--------> " + str(vehicle_id)
                            else:
                                traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                                print "--------Change to Right--------> " + str(vehicle_id)
                            # if i>j:
                            #     traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                            # else:
                            #     traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                        # print "------------------vehicles_number_turn_left--------------"
                        # print vehicles_number_turn_left
                        # # if i == vehicles_number_turn_left:
                        #     # print "-------left-----"
                        #     # print j
                        #     # j = 0
                        # if i < vehicles_number_turn_left:
                        #     # if traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane + 1):
                        #     traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                        #     # j += 1
                        #     i += 1
                        # else:
                        #     # if traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane - 1):
                        #     traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)

                    print "-------left-----"
                    print i
                    print "-------right------"
                    print j
                # Change vehicles position to target lane
                else:
                    print "------recommendation------"
                    print recommendation.target_lane
                    print "------Vehicles number------"
                    print len(vehicles)
                    j=0
                    for vehicle_id in vehicles:
                        if traci.vehicle.couldChangeLane(vehicle_id, recommendation.target_lane - recommendation.lane):
                            traci.vehicle.changeLane(vehicle_id, recommendation.target_lane, 500000)
                            # traci.vehicle.changeSublane(vehicle_id, recommendation.target_lane - recommendation.lane)
                            print "--------Change to target--------> " \
                                  + "from " +str(recommendation.lane) \
                                  + " to " + str(recommendation.target_lane) \
                                  + str(vehicle_id)
                        # j+=1
                        #traci.vehicle.changeSublane(vehicle_id, recommendation.target_lane - recommendation.lane)
                    # print "number of vehicles changed position to target lane"
                    # print j