import os
import sumolib
import subprocess

class Simulation:
    __project_directory = ""
    __sumocfg_file_path = "map.sumocfg"
    __osm_file = ""
    __network_file = ""
    __sensors_list = []
    __incidents_list = []
    __traffic_flows = []

    def set_osm_file(self, file_path):
        Simulation.__osm_file = file_path

    def set_network_file(self, file_path):
        Simulation.__network_file = file_path

    def create_sumo_config_file(self):
        #Get current project directory
        Simulation.__project_directory = os.path.dirname(Simulation.__network_file)
        Simulation.__sumocfg_file_path = Simulation.__project_directory + "\\map.sumocfg"
        #Create the sumocfg file
        with open(Simulation.__sumocfg_file_path, 'w') as file:
            file.write(
                '''<?xml version="1.0" encoding="iso-8859-1"?>
                <configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">

                    <input>
                        <net-file value="''' + Simulation.__network_file + '''"/>
                        <route-files value=""/>
                        <additional-files value=""/>
                    </input>

                    <time>
                        <begin value="0"/>
                        <end value="10000"/>
                    </time>

                <!--
                    196547668#0
                    196547668#7
                    <report>
                        <no-duration-log value="true"/>
                        <no-step-log value="true"/>
                    </report>
                -->
                </configuration>'''
            )

    def start_simulation(self):
        sumogui = sumolib.checkBinary("sumo-gui")

        #if not Simulation.__project_directory:
        #    simulations_directory = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        #    Simulation.__project_directory = simulations_directory + "\\" + [directory for directory in os.listdir(simulations_directory)][-1]
        #    Simulation.__project_directory += "\\"

        #subprocess.Popen([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file_path])
        print Simulation.__sumocfg_file_path
        subprocess.Popen([sumogui, "-c", Simulation.__sumocfg_file_path])
