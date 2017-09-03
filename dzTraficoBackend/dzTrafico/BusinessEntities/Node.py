from dzTrafico.Helpers.Converter import Converter
import traci
from random import randint

class Node(object):

    sensors = []
    edge = None
    initial_max_speed = 0
    current_vsl = 0
    previous_vsl = 0

    recommendations = []
    previous_nodes_of_discharged_area = []

    VSL_is_activated = False
    LC_is_activated = False

    isCongested = False

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
        for lane in self.congested_lanes:
            lane_id = self.edge.getLane(lane).getID()
            for sensor in self.sensors:
                if lane_id == sensor.get_sensor_lane():
                    return sensor.check_clear_lane()
        return False

    def set_congested_lanes(self, congested_lanes):
        self.congested_lanes = congested_lanes

    def close_incident_lanes(self):
        # Set disallowed vehicles to enter lane incident
        for lane in self.congested_lanes:
            traci.lane.setDisallowed(self.edge.getLane(lane).getID(), "passenger")

    # --------------- VSL Control ------------------------------------------
    def activate_VSL(self):
        self.VSL_is_activated = True
        traci.edge.setMaxSpeed(self.edge.getID(), Converter.toms(self.current_vsl))

    def deactivate_VSL(self):
        self.VSL_is_activated = False
        self.reset_previous_speed()
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
        self.LC_is_activated = True
        print "----------- Lane Change -----------"
        print self.edge.getID()

        self.change_lane()

    def deactivate_LC(self):
        self.LC_is_activated = False

    def set_sumo_LC_Model(self, mode):
        for veh_id in traci.edge.getLastStepVehicleIDs(self.edge.getID()):
            traci.vehicle.setLaneChangeMode(veh_id, mode)

    def incident_change_lane(self):
        three = 1
        for recommendation in self.recommendations:
            if recommendation.change_lane:
                lane = self.edge.getLane(recommendation.lane)

                vehicles = traci.lane.getLastStepVehicleIDs(lane.getID())

                if len(vehicles)>0:
                    vehicles.remove(vehicles[-1])
                if len(vehicles) > 0:
                    traci.vehicle.changeLane(vehicles[-1], recommendation.lane, 1500)
                    vehicles.remove(vehicles[-1])

                # Change either way
                if recommendation.change_to_either_way:
                    for vehicle_id in vehicles:
                        # Turn Left
                        right_lane_occupancy = traci.lane.getLastStepOccupancy(
                            self.edge.getLane(recommendation.lane - 1).getID()
                        )
                        left_lane_occupancy = traci.lane.getLastStepOccupancy(
                            self.edge.getLane(recommendation.lane + 1).getID()
                        )
                        if right_lane_occupancy > left_lane_occupancy:
                            if traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane + 1):
                                traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                            elif three == 20:
                                traci.vehicle.changeLane(vehicle_id, recommendation.lane + 1, 500000)
                                three = 1
                            else:
                                three += 1

                        # Turn Right
                        elif traci.vehicle.couldChangeLane(vehicle_id, recommendation.lane - 1):
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                        elif three == 20:
                            traci.vehicle.changeLane(vehicle_id, recommendation.lane - 1, 500000)
                            three = 1
                        else:
                            three += 1

                # Change vehicles position to target lane
                else:
                    if len(self.edge.getLanes())>2:
                        ten = 1
                        right_lane = self.edge.getLane(recommendation.target_lane-1)
                        left_lane = self.edge.getLane(recommendation.target_lane+1)
                        target_lane = self.edge.getLane(recommendation.target_lane)
                    for veh in vehicles:
                        # if traci.vehicle.couldChangeLane(vehicle_id, recommendation.target_lane - recommendation.lane):
                        #     traci.vehicle.changeLane(vehicle_id, recommendation.target_lane, 500000)
                        if len(self.edge.getLanes()) > 2:
                            current_lane_occupancy = traci.lane.getLastStepOccupancy(
                                target_lane.getID()
                            )
                            right_lane_occupancy = traci.lane.getLastStepOccupancy(
                                right_lane.getID()
                            )
                            left_lane_occupancy = traci.lane.getLastStepOccupancy(
                                left_lane.getID()
                            )
                            # Turn to left
                            if recommendation.target_lane - recommendation.lane > 0:
                                # Get current lane vehicles
                                if current_lane_occupancy > left_lane_occupancy:
                                    if traci.vehicle.couldChangeLane(veh, recommendation.target_lane + 1):
                                        traci.vehicle.changeLane(veh, recommendation.target_lane + 1, 500000)
                                    # elif three == 20:
                                    #     traci.vehicle.changeLane(veh, recommendation.lane + 1, 500000)
                                    #     three = 1
                                    # else:
                                    #     three += 1
                            elif current_lane_occupancy > right_lane_occupancy:
                                if traci.vehicle.couldChangeLane(veh, recommendation.target_lane - 1):
                                    traci.vehicle.changeLane(veh, recommendation.target_lane - 1, 500000)
                                # elif three == 20:
                                #     traci.vehicle.changeLane(veh, recommendation.lane - 1, 500000)
                                #     three = 1
                                # else:
                                #     three += 1

                        elif traci.vehicle.couldChangeLane(veh, recommendation.target_lane + 1):
                            traci.vehicle.changeLane(veh, recommendation.target_lane, 500000)

    def change_lane(self):
        for recommendation in self.recommendations:
            if recommendation.change_lane:
                lane = self.edge.getLane(recommendation.lane)

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
                    if len(self.edge.getLanes())>2:
                        ten = 1
                        right_lane = self.edge.getLane(recommendation.target_lane-1)
                        left_lane = self.edge.getLane(recommendation.target_lane+1)
                        target_lane = self.edge.getLane(recommendation.target_lane)
                    vehicles = traci.lane.getLastStepVehicleIDs(lane.getID())

                    for vehicle_id in vehicles:
                        if traci.vehicle.couldChangeLane(vehicle_id, recommendation.target_lane - recommendation.lane):
                            traci.vehicle.changeLane(vehicle_id, recommendation.target_lane, 500000)
                        # traci.vehicle.changeSublane(vehicle_id, recommendation.target_lane - recommendation.lane)
                        print "--------Change to target--------> " \
                              + "from " +str(recommendation.lane) \
                              + " to " + str(recommendation.target_lane) \
                              + str(vehicle_id)
                        # Check the lane with less occupancy to

                        vehs = traci.lane.getLastStepVehicleIDs(target_lane.getID())
                        for veh in vehs:
                            if len(self.edge.getLanes()) > 2:
                                current_lane_occupancy = traci.lane.getLastStepOccupancy(
                                    target_lane.getID()
                                )
                                right_lane_occupancy = traci.lane.getLastStepOccupancy(
                                    right_lane.getID()
                                )
                                left_lane_occupancy = traci.lane.getLastStepOccupancy(
                                    left_lane.getID()
                                )
                                # Turn to left
                                if recommendation.target_lane - recommendation.lane>0:
                                    # Get current lane vehicles
                                    if current_lane_occupancy> left_lane_occupancy:
                                        if traci.vehicle.couldChangeLane(veh, recommendation.target_lane + 1):
                                            traci.vehicle.changeLane(veh, recommendation.target_lane + 1, 500000)
                                elif current_lane_occupancy> right_lane_occupancy:
                                    if traci.vehicle.couldChangeLane(veh, recommendation.target_lane - 1):
                                        traci.vehicle.changeLane(veh, recommendation.target_lane - 1, 500000)
                                    elif ten == 10:
                                        traci.vehicle.changeLane(veh, recommendation.lane - 1, 500000)
                                        ten = 1
                                    else:
                                        ten += 1

                            elif traci.vehicle.couldChangeLane(veh, recommendation.target_lane + 1):
                                traci.vehicle.changeLane(veh, recommendation.target_lane + 1, 500000)

                                    # if len(self.edge.getLanes())>2:
                        #     current_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #         target_lane.getID()
                        #     )
                        #     right_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #         right_lane.getID()
                        #     )
                        #     left_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #         left_lane.getID()
                        #     )
                        #     # Turn to left
                        #     if recommendation.target_lane - recommendation.lane>0:
                        #         # Get current lane vehicles
                        #         while current_lane_occupancy> left_lane_occupancy:
                        #             vehs = traci.lane.getLastStepVehicleIDs(target_lane.getID())
                        #             rand = randint(0, len(vehs)-1)
                        #             if traci.vehicle.couldChangeLane(vehs[rand], recommendation.target_lane + 1):
                        #                 traci.vehicle.changeLane(vehs[rand], recommendation.target_lane + 1, 500000)
                        #             elif ten == 10:
                        #                 traci.vehicle.changeLane(vehs[rand], recommendation.target_lane + 1, 500000)
                        #                 ten = 1
                        #             else:
                        #                 ten += 1
                        #
                        #             # Update current_lane_occupancy
                        #             current_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #                 target_lane.getID()
                        #             )
                        #             left_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #                 left_lane.getID()
                        #             )
                        #     else:
                        #         while current_lane_occupancy> right_lane_occupancy:
                        #             vehs = traci.lane.getLastStepVehicleIDs(target_lane.getID())
                        #             rand = randint(0, len(vehs)-1)
                        #             if traci.vehicle.couldChangeLane(vehs[rand], recommendation.target_lane - 1):
                        #                 traci.vehicle.changeLane(vehs[rand], recommendation.target_lane - 1, 500000)
                        #             elif ten == 10:
                        #                 traci.vehicle.changeLane(vehs[rand], recommendation.target_lane - 1, 500000)
                        #                 ten = 1
                        #             else:
                        #                 ten += 1
                        #
                        #             # Update current_lane_occupancy
                        #             current_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #                 target_lane.getID()
                        #             )
                        #             right_lane_occupancy = traci.lane.getLastStepOccupancy(
                        #                 right_lane.getID()
                        #             )