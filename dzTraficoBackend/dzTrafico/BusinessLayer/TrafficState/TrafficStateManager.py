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

    @staticmethod
    def get_instance():
        if TrafficStateManager.__trafficStateManager is None:
            TrafficStateManager.__trafficStateManager = TrafficStateManager()
        return TrafficStateManager.__trafficStateManager

    def start(self, consumer):

        self.simulation = self.__simulationManager.get_simulation()
        sinks = self.simulation.get_sinks()

        self.deactivate_lc(sinks)
        TrafficAnalyzer.isCongestionDetected = False

        self.simulation.start_simulation()
        densities = []
        for step in range(self.simulation.sim_duration):

            traci.switch(self.simulation.SIM)
            traci.simulationStep()
            self.simulation.check_incidents(step, self.simulation.SIM)
            self.simulation.clean_incidents(step)
            self.set_sumo_LC_Model(sinks, self.simulation.LCMode_noControl)

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

            # Read traffic state in each time stamp
            # Check for congestion
            res, rest = divmod(step, self.simulation.sim_step_duration)
            if rest == 0:
                traffic_state = self.read_traffic_state(sinks)
                if TrafficAnalyzer.isVSLControlActivated and TrafficAnalyzer.isCongestionDetected:
                    self.update_vsl(sinks)
                consumer.send(traffic_state)
                if len(self.simulation.get_incidents())>0:
                    for state in traffic_state:
                        if state['edge_id'] == traci.lane.getEdgeID(self.simulation.get_incidents()[0].lane_id):
                            densities.append(state['density'])
                            print step, "  ", state['density']

            if TrafficAnalyzer.isCongestionDetected:
                self.simulation.check_statistics_vehicles()
                self.simulation.reset_vehicles_behaviour()

        traci.close()
        traci.switch(self.simulation.SIM)
        traci.close()

        print densities

        gpms = self.__simulationManager.get_simulation_gpm_results()
        serializer = GlobalPerformanceMeasurementSerializer(gpms, many=True)
        consumer.send(serializer.data)

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
        for sink in sinks:
            sink[0].update_vsl()

    def deactivate_vsl(self, sinks):
        for sink in sinks:
            sink[0].deactivate_vsl()

    def deactivate_lc(self, sinks):
        for sink in sinks:
            sink[0].deactivate_lc()

    def set_sumo_LC_Model(self, sinks, mode):
        for sink in sinks:
            sink[0].set_sumo_LC_Model(mode)