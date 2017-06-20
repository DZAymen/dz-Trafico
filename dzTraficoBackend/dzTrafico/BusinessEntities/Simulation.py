import os, sumolib, subprocess
import traci

class Simulation:

    inFlowPoints = []
    outFlowPoints = []

    project_directory = ""
    __sumocfg_file = "map.sumocfg"
    __osm_file = ""

    __network_file = "map.net.xml"
    __route_file = ""
    __sensors_file = ""

    __sensors_list = []
    __incidents = []
    __traffic_flows = []

    def __init__(self):
        simulations_directory = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        Simulation.project_directory = simulations_directory + "\\" + \
                                         [directory for directory in os.listdir(simulations_directory)][-1]
        Simulation.project_directory += "\\"

    def set_osm_file(self, file_path):
        Simulation.__osm_file = file_path

    def set_network_file(self, file_path):
        self.inFlowPoints = []
        self.outFlowPoints = []
        self.__incidents = []
        Simulation.project_directory = os.path.dirname(file_path) + "\\"
        Simulation.__network_file = os.path.basename(file_path)

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
    
                        <time>
                            <begin value="0"/>
                            <end value="10000"/>
                        </time>
                        
                    </configuration>'''
                )

    def add_sensors(self, sensors):
        self.__sensors_list.append(sensors)

    def start_simulation(self):
        sumogui = sumolib.checkBinary("sumo-gui")
        #subprocess.Popen([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file])
        traci.start([sumogui, "-c", Simulation.project_directory + Simulation.__sumocfg_file, "--summary", Simulation.project_directory + "summary.xml"])
        for step in range(2000):
            traci.simulationStep()
            self.check_incidents(step)
            #print self.__sensors_list[0].get_sensor_id()
            #for sensor in self.__sensors_list:
                #sensor.add_measure(traci.inductionloop.getLastStepMeanSpeed(str(sensor.get_sensor_id())))

    def set_flows(self, flows):
        self.__traffic_flows = flows

    def get_flows(self):
        return self.__traffic_flows

    def set_sensors_file(self, file_path):
        Simulation.__sensors_file = file_path

    def add_incidents(self, incident):
        self.__incidents.append(incident)

    def check_incidents(self, step):
        for incident in self.__incidents:
            if step == incident.time:
                for lane in incident.lanes:
                    vehicles = traci.lane.getLastStepVehicleIDs(lane)
                    if len(vehicles)>0:
                        #traci.vehicle.setSpeed(vehicles[0], 0)
                        edge_id = traci.lane.getEdgeID(lane)
                        traci.vehicle.setStop(vehID=vehicles[0],edgeID=edge_id,pos=100, laneIndex=0, duration=incident.duration)
                        break

    def add_inflows(self, inFlowPoints):
        self.inFlowPoints.append(inFlowPoints)

    def add_outflows(self, outFlowPoints):
        self.outFlowPoints.append(outFlowPoints)