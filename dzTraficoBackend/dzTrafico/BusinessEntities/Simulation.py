import os, sumolib, subprocess
import traci

class Simulation:
    #Simulation without vsl and lc control
    SIM = "sim"
    # Simulation with vsl and lc control
    SIM_VSL_LC = "sim_vsl_lc"

    simulation_summary_filename = "summary.xml"
    simulation_summary_vsl_lc_filename = "summary_vsl_lc.xml"
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
        self.__traffic_flows = []

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

    def add_sinks(self, sinks):
        self.__sinks.append(sinks)

    def add_sensors(self, sensors):
        self.__sensors_list.append(sensors)

    def start_simulation(self, sim_duration):
        sumogui = sumolib.checkBinary("sumo-gui")
        sumo = sumolib.checkBinary("sumo")
        #subprocess.Popen([sumogui, "-c", Simulation.__project_directory + Simulation.__sumocfg_file])
        traci.start(
            [
                sumo,
                "-c", Simulation.project_directory + Simulation.__sumocfg_file,
                "--summary", Simulation.project_directory + self.simulation_summary_filename
            ],
            label=self.SIM
        )
        traci.start(
            [
                sumogui,
                "-c", Simulation.project_directory + Simulation.__sumocfg_file,
                "--summary", Simulation.project_directory + self.simulation_summary_vsl_lc_filename
            ],
            label=self.SIM_VSL_LC
        )

        for step in range(sim_duration):
            traci.switch(self.SIM)
            traci.simulationStep()

            traci.switch(self.SIM_VSL_LC)
            traci.simulationStep()

            self.check_incidents(step)
            for sink in self.__sinks:
                sink[0].read_traffic_state()

        traci.close()
        traci.switch(self.SIM)
        traci.close()
        # self.draw_mean_travel_time_graph()

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
            if step == incident.accidentTime:
                for lane in incident.lanes:
                    vehicles = traci.lane.getLastStepVehicleIDs(lane)
                    if len(vehicles)>0:
                        #traci.vehicle.setSpeed(vehicles[0], 0)
                        edge_id = traci.lane.getEdgeID(lane)
                        traci.vehicle.setStop(vehID=vehicles[0],edgeID=edge_id, laneIndex=0, pos=traci.lane.getLength(lane)-20, duration=incident.accidentDuration * 1000)
                        break

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

    def draw_mean_travel_time_graph(self):
        subprocess.call(
            [
                r"python F:\PFE\Simulateurs\SUMO\tools\visualization\plot_summary.py",
                "-i", self.project_directory + self.simulation_summary_filename +
                      "," + self.project_directory + self.simulation_summary_vsl_lc_filename,
                "-l", "Mean Travel Time - VSL/LC" + "," + "Mean Travel Time + VSL/LC",
                "-o", self.project_directory + self.graph_image,
                "-m", "meanTravelTime"
            ]
        )
