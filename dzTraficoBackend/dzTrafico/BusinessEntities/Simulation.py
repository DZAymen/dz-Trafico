import os, sumolib, subprocess
import traci

class Simulation:
    __project_directory = ""
    __sumocfg_file = "map.sumocfg"
    __osm_file = ""
    __network_file = "map.net.xml"
    __route_file = "map.rou.xml"
    __sensors_file = "sensors.add.xml"
    __sensors_list = []
    __incidents_list = []
    __traffic_flows = []

    def set_osm_file(self, file_path):
        Simulation.__osm_file = file_path

    def set_network_file(self, file_path):
        Simulation.__project_directory = os.path.dirname(file_path) + "\\"
        Simulation.__network_file = os.path.basename(file_path)

    def create_sumo_config_file(self):
        if Simulation.__project_directory:
            #Create the sumocfg file
            with open(Simulation.__project_directory + Simulation.__sumocfg_file, 'w') as file:
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
        else:
            simulations_directory = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
            Simulation.__project_directory = simulations_directory + "\\" + [directory for directory in os.listdir(simulations_directory)][-1]
            Simulation.__project_directory += "\\"

    def add_sensors(self, sensors):
        self.__sensors_list.append(sensors)

    def start_simulation(self):
        sumogui = sumolib.checkBinary("sumo-gui")
        #subprocess.Popen([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file])
        traci.start([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file])
        for step in range(2000):
            traci.simulationStep()
            #print self.__sensors_list[0].get_sensor_id()
            for sensor in self.__sensors_list:
                sensor.add_measure(traci.inductionloop.getLastStepMeanSpeed(str(sensor.get_sensor_id())))
