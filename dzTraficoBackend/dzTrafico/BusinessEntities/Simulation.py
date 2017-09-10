import os, sumolib, subprocess
import traci
from dzTrafico.Helpers.Converter import Converter

class Simulation:
    #Simulation without vsl and lc control
    SIM = "sim"
    # Simulation with vsl and lc control
    SIM_VSL_LC = "sim_vsl_lc"

    simulation_summary_filename = "summary.xml"
    simulation_summary_vsl_lc_filename = "summary_vsl_lc.xml"

    incident_sensors_output = "incident.sensors.output.xml"

    trip_output = "trip.output.xml"
    trip_output_vsl_lc = "trip.output.vsl_lc.xml"

    lanechange_summary_filename = "lc.summary.xml"
    lanechange_summary_vsl_lc_filename = "lc.summary_vsl_lc.xml"

    edge_dump_additional_filename = "..\..\data\edge.dump.add.xml"
    edge_dump_filename = "..\..\data\edge.dump.xml"
    emissions_edge_dump_filename = "..\..\data\emissions.edge.dump.xml"

    edge_dump_additional_vsl_lc_filename = "..\..\data\edge.dump.add.vsl_lc.xml"
    edge_dump_vsl_lc_filename = "..\..\data\edge.dump.vsl_lc.xml"
    emissions_edge_dump_vsl_lc_filename = "..\..\data\emissions.edge.dump.vsl_lc.xml"

    graph_image = "summary_mean_travel_time.png"

    inFlowPoints = []
    outFlowPoints = []

    project_directory = ""
    __sumocfg_file = "map.sumocfg"
    __osm_file = ""

    __network_file = "map.net.xml"
    __route_file = ""
    __sensors_file = ""

    __sinks = []
    __sensors_list = []
    __incidents = []
    __traffic_flows = []
    __vehicle_types = []

    incident_veh = None
    sim_duration = 0
    sim_step_duration = 1

    initial_incident_lane_max_speed = 80

    statistics_vehicles = []

    LCMode_noControl = 597
    LCMode_vsl_lc = 512
    LCMode_default = 597

    __map_box = None
    __sensors_distance = 0

    def __init__(self):

        self.inFlowPoints = []
        self.outFlowPoints = []
        self.__incidents = []
        self.__traffic_flows = []
        self.__vehicle_types = []
        self.__sinks = []

        simulations_directory = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        Simulation.project_directory = simulations_directory + "\\" + \
                                         [directory for directory in os.listdir(simulations_directory)][-1]
        Simulation.project_directory += "\\"

    def set_osm_file(self, file_path):
        Simulation.__osm_file = file_path

    def set_project_directory_path(self, project_directory):
        Simulation.project_directory = project_directory + "\\"

    def set_network_file(self, file_path):
        self.inFlowPoints = []
        self.outFlowPoints = []
        self.__incidents = []
        self.__traffic_flows = []
        self.__vehicle_types = []
        self.__sinks = []

        Simulation.__network_file = file_path

    def set_route_file(self, route_file_path):
        Simulation.__route_file = route_file_path

    def get_route_file(self):
        return Simulation.__route_file

    def get_network_file_path(self):
        return Simulation.project_directory + Simulation.__network_file

    def create_sumo_config_file(self):
        if Simulation.project_directory:
            #Create the sumocfg file
            with open(Simulation.project_directory + Simulation.__sumocfg_file, 'w') as file:
                file.write(
                    '''<?xml version="1.0" encoding="iso-8859-1"?>
                    <configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">
    
                        <input>
                            <net-file value="''' + Simulation.__network_file + '''"/>
                            <route-files value="''' + Simulation.__route_file + '''"/>
                            <additional-files value="''' + Simulation.__sensors_file + '''"/>
                        </input>
                        
                        <processing>
                            <time-to-teleport value="-1"/>
                        </processing>
                        
                        <time>
                            <begin value="0"/>
                            <end value="10000"/>
                        </time>
                        
                    </configuration>'''
                )

    def add_sinks(self, sinks):
        self.__sinks.append(sinks)

    def add_sensors(self, sensors):
        self.__sensors_list.append(sensors)

    def start_simulation(self):
        sumogui = sumolib.checkBinary("sumo-gui")
        sumo = sumolib.checkBinary("sumo")
        #subprocess.Popen([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file])
        traci.start(
            [
                sumogui,
                "-c", Simulation.project_directory + Simulation.__sumocfg_file,
                "--summary", Simulation.project_directory + self.simulation_summary_filename,
                "--lanechange-output", Simulation.project_directory + self.lanechange_summary_filename,
                "-a", Simulation.project_directory + self.edge_dump_additional_filename
                      # + ','
                      # + Simulation.project_directory + Simulation.__sensors_file
                ,
                "--tripinfo-output", Simulation.project_directory + self.trip_output,
                "--device.emissions.probability", "1"
            ],
            label=self.SIM
        )
        traci.start(
            [
                sumogui,
                "-c", Simulation.project_directory + Simulation.__sumocfg_file,
                "--summary", Simulation.project_directory + self.simulation_summary_vsl_lc_filename,
                "--lanechange-output", Simulation.project_directory + self.lanechange_summary_vsl_lc_filename,
                "-a", Simulation.project_directory + self.edge_dump_additional_vsl_lc_filename + ','
                      + Simulation.project_directory + Simulation.__sensors_file,
                "--tripinfo-output", Simulation.project_directory + self.trip_output_vsl_lc,
                "--device.emissions.probability", "1"
            ],
            label=self.SIM_VSL_LC
        )

    def set_flows(self, flows):
        self.__traffic_flows = flows

    def get_flows(self):
        return self.__traffic_flows

    def set_sensors_file(self, file_path):
        Simulation.__sensors_file = file_path

    def add_incidents(self, incidents):
        for incident in incidents:
            self.__incidents.append(incident)

    def check_incidents(self, step, sim_type):
        clear = False
        for incident in self.__incidents:
            if step == incident.accidentTime:
                vehicles = traci.lane.getLastStepVehicleIDs(incident.lane_id)
                if len(vehicles)>0:
                    edge_id = traci.lane.getEdgeID(incident.lane_id)
                    self.initial_incident_lane_max_speed = traci.lane.getMaxSpeed(incident.lane_id)
                    traci.vehicle.changeLane(vehicles[0], incident.lane, 500000)
                    traci.vehicle.setStop(vehID=vehicles[0],edgeID=edge_id, laneIndex=incident.lane, pos=incident.lane_position, duration=incident.accidentDuration * 1000)
                    if sim_type == self.SIM:
                        traci.edge.setMaxSpeed(traci.lane.getEdgeID(incident.lane_id), Converter.toms(60))
                    else:
                        traci.edge.setMaxSpeed(traci.lane.getEdgeID(incident.lane_id), Converter.toms(60))
            if step > incident.accidentTime+incident.accidentDuration:
                clear = True
        return clear

    def clean_incidents(self, step):
        for incident in self.__incidents:
            if step == incident.accidentTime+incident.accidentDuration:
                traci.edge.setMaxSpeed(
                    traci.lane.getEdgeID(incident.lane_id),
                    self.initial_incident_lane_max_speed
                )
                traci.lane.setDisallowed(incident.lane_id, "truck")

    def add_inflows(self, inFlowPoints):
        self.inFlowPoints.append(inFlowPoints)

    def add_outflows(self, outFlowPoints):
        self.outFlowPoints.append(outFlowPoints)

    def get_inflows(self):
        return self.inFlowPoints

    def get_outflows(self):
        return self.outFlowPoints

    def get_incidents(self):
        return self.__incidents

    def set_duration(self, sim_duration):
        self.sim_duration = sim_duration

    def get_sinks(self):
        return self.__sinks

    def check_statistics_vehicles(self):
        if len(self.__incidents)>0:
            incident = self.__incidents[0]
            edge_id = traci.lane.getEdgeID(incident.lane_id)
            for veh_id in traci.edge.getLastStepVehicleIDs(edge_id):
                if not self.statistics_vehicles.count(veh_id):
                    self.statistics_vehicles.append(veh_id)

    def reset_vehicles_behaviour(self):
        if len(self.__incidents)>0:
            incident = self.__incidents[0]
            edge_id = traci.lane.getEdgeID(incident.lane_id)
            for veh_id in traci.edge.getLastStepVehicleIDs(edge_id):
                if traci.vehicle.getLaneIndex(veh_id) != incident.lane and traci.vehicle.getLanePosition(veh_id) > incident.lane_position:
                    traci.vehicle.setLaneChangeMode(veh_id, Simulation.LCMode_default)
                    traci.vehicle.changeLane(
                        veh_id,
                        traci.vehicle.getLaneIndex(veh_id),
                        1500
                    )

    def add_vehicle_types(self, types):
        self.__vehicle_types.extend(types)

    def set_map_box(self, map_box):
        self.__map_box = map_box

    def get_map_box(self):
        return self.__map_box

    def set_sensors_distance(self, distance):
        self.__sensors_distance = distance

    def get_sensors_distance(self):
        return self.__sensors_distance
