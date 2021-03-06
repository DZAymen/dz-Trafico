from numpy.distutils.system_info import numarray_info
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.EdgeState import EdgeStateSerializer
from dzTrafico.BusinessLayer.Statistics.GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementSerializer
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer
import traci

from dzTrafico.BusinessEntities.LCRecommendation import LCRecommendation

class TrafficStateManager:
    __trafficStateManager = None
    __simulationManager = SimulationManager.get_instance()
    vehicles = []
    LC_consumer = None
    VSL_consumer = None

    @staticmethod
    def get_instance():
        if TrafficStateManager.__trafficStateManager is None:
            TrafficStateManager.__trafficStateManager = TrafficStateManager()
        return TrafficStateManager.__trafficStateManager

    def start(self, realTimeTrafficStateConsumer):

        self.realtimeData = dict()
        self.realtimeData["vsl"] = []
        self.realtimeData["lc"] = []
        self.realtimeData["trafficState"] = []

        self.control_vehs_dict = dict()
        self.no_control_vehs_dict = dict()

        self.simulation = self.__simulationManager.get_simulation()
        sinks = self.simulation.get_sinks()

        self.deactivate_lc(sinks)
        TrafficAnalyzer.isCongestionDetected = False

        self.simulation.start_simulation()
        densities = []
        nocontrol_densities = []
        time = []

        self.incident_node = self.get_incident_node(sinks)

        for step in range(self.simulation.sim_duration):

            traci.switch(self.simulation.SIM)
            traci.simulationStep()
            self.simulation.check_incidents(step, self.simulation.SIM)
            self.simulation.clean_incidents(step)
            self.set_sumo_LC_Model(sinks, self.simulation.LCMode_noControl)


            res, rest = divmod(step, self.simulation.sim_step_duration)
            if rest == 0:
                nocontrol_densities.append(self.incident_node.get_node_density())

            # Changelane in accident edge
            if TrafficAnalyzer.congestionExists:
                self.incident_change_lane(sinks)
            traci.switch(self.simulation.SIM_VSL_LC)
            traci.simulationStep()
            incidentIsClear = self.simulation.check_incidents(step, self.simulation.SIM_VSL_LC)
            self.simulation.clean_incidents(step)
            self.set_sumo_LC_Model(sinks, self.simulation.LCMode_vsl_lc)

            if step == 0 or (TrafficAnalyzer.isCongestionDetected and incidentIsClear):
                self.deactivate_vsl(sinks)

            if TrafficAnalyzer.congestionExists:
                self.incident_change_lane(sinks)

            # Check for LanChanges in nodes' recommendations
            if TrafficAnalyzer.congestionExists and TrafficAnalyzer.isLCControlActivated and self.simulation.sim_step_duration>1:
                self.change_lane(sinks)
                # if self.LC_consumer is not None:
                    # self.LC_consumer.send(self.get_LC_recommendations(sinks))
                self.realtimeData["lc"] = self.get_LC_recommendations(sinks)

            # Read traffic state in each time stamp
            # Check for congestion
            res, rest = divmod(step, self.simulation.sim_step_duration)
            if rest == 0:
                traffic_state = self.read_traffic_state(sinks)
                if TrafficAnalyzer.isVSLControlActivated and TrafficAnalyzer.isCongestionDetected:
                    vsl_values = self.update_vsl(sinks)
                    # if self.VSL_consumer is not None:
                    self.realtimeData["vsl"] = vsl_values
                        # self.VSL_consumer.send(vsl_values)
                self.realtimeData["trafficState"] = traffic_state
                realTimeTrafficStateConsumer.send(self.realtimeData)
                densities.append(self.incident_node.get_current_density())
                time.append(step)

            if TrafficAnalyzer.isCongestionDetected:
                self.simulation.check_statistics_vehicles()
                self.simulation.reset_vehicles_behaviour()

        self.set_density_stats(time, densities, nocontrol_densities)

        traci.close()
        traci.switch(self.simulation.SIM)
        traci.close()

        gpms = self.__simulationManager.get_simulation_gpm_results()
        serializer = GlobalPerformanceMeasurementSerializer(gpms, many=True)
        realTimeTrafficStateConsumer.send(serializer.data)

    def read_traffic_state(self, sinks):
        traffic_state = []
        for sink in sinks:
            for edgeState in sink[0].read_traffic_state():
                traffic_state.append(edgeState)

        edgeStateSerializer = EdgeStateSerializer(traffic_state, many=True)
        return edgeStateSerializer.data

    def change_lane(self, sinks):
        for sink in sinks:
            sink[0].change_lane()

    def incident_change_lane(self, sinks):
        # node = None
        # incidents = self.simulation.get_incidents()
        # for incident in incidents:
        #     if step >= incident.accidentTime and step <= (incident.accidentTime+incident.accidentDuration):
        #         for sink in sinks:
        #             node = sink[0].get_node_by_edgeID(
        #                 traci.lane.getEdgeID(incident.lane_id)
        #             )
        #             if node is not None:
        #                 break
        #         node.incident_change_lane()
        for sink in sinks:
            sink[0].incident_change_lane()

    def update_vsl(self, sinks):
        vsl_values = []
        for sink in sinks:
            vsl_values.extend(sink[0].update_vsl())
        return vsl_values

    def deactivate_vsl(self, sinks):
        for sink in sinks:
            sink[0].deactivate_vsl()

    def deactivate_lc(self, sinks):
        for sink in sinks:
            sink[0].deactivate_lc()

    def set_sumo_LC_Model(self, sinks, mode):
        for sink in sinks:
            sink[0].set_sumo_LC_Model(mode)

    def check_departed_vehicles(self, step, vehs_dict):
        # Add departed vehicles
        for veh_id in traci.simulation.getDepartedIDList():
            vehs_dict[veh_id] = Vehicle(veh_id)
        # Remove arrived vehicles
        for veh_id in traci.simulation.getArrivedIDList():
            vehs_dict[veh_id].set_arrived()

        for veh_id in vehs_dict:
            print " Step #", step, " num_stops", vehs_dict[veh_id].measure_vehicle_variables(step)

    def get_num_stops(self, vehs_dict):
        num_stops = 0
        for veh_id in vehs_dict:
            # if vehs_dict[veh_id].arrived:
            print vehs_dict[veh_id].arrived
            print vehs_dict[veh_id].num_stops
            num_stops += vehs_dict[veh_id].num_stops
            print num_stops
        return num_stops

    def set_LC_consumer(self, consumer):
        self.LC_consumer = consumer

    def set_VSL_consumer(self, consumer):
        self.VSL_consumer = consumer

    def get_LC_recommendations(self, sinks):
        lc_recommendations = []
        for sink in sinks:
            lc_recommendations.extend(sink[0].get_LC_recommendations())
        return lc_recommendations

    def get_incident_node(self, sinks):
        return sinks[0][0].get_node_by_edgeID(traci.lane.getEdgeID(self.simulation.get_incidents()[0].lane_id))

    def set_density_stats(self, time, densities, nocontrol_densities):
        Simulation.set_density_stats(time, densities, nocontrol_densities)


class Vehicle:

    num_stops = 0

    isStoppedLastStep = False
    isStopeed = False

    def __init__(self, id):
        self.id = id
        self.arrived = False

    def set_arrived(self):
        self.arrived = True

    def measure_vehicle_variables(self, step):
        if not self.arrived:
            self.isStoppedLastStep = self.isStopeed
            self.isStopeed = traci.vehicle.isStopped(self.id)

            if self.isStopeed and not self.isStoppedLastStep:
                self.num_stops += 1
        return self.num_stops