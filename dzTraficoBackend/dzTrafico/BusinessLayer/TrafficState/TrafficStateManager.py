from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.Sink import Sink
from dzTrafico.BusinessEntities.EdgeState import EdgeStateSerializer
from dzTrafico.BusinessLayer.Statistics.GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementSerializer
from dzTrafico.BusinessLayer.TrafficAnalysis.TrafficAnalyzer import TrafficAnalyzer
import traci

class TrafficStateManager:
    __trafficStateManager = None
    __simulationManager = SimulationManager.get_instance()

    @staticmethod
    def get_instance():
        if TrafficStateManager.__trafficStateManager is None:
            TrafficStateManager.__trafficStateManager = TrafficStateManager()
        return TrafficStateManager.__trafficStateManager

    def start(self, consumer):
        lc_nodes = []


        self.simulation = self.__simulationManager.get_simulation()
        sinks = self.simulation.get_sinks()
        Lc_is_active = False

        self.simulation.start_simulation()

        for step in range(self.simulation.sim_duration):

            traci.switch(self.simulation.SIM)
            traci.simulationStep()
            self.simulation.check_incidents(step)
            self.set_sumo_LC_Model(lc_nodes, 528)

            traci.switch(self.simulation.SIM_VSL_LC)
            traci.simulationStep()
            self.simulation.check_incidents(step)

            # Check for LanChanges in nodes' recommendations
            incident = self.simulation.get_incidents()[0]
            if Lc_is_active and self.simulation.sim_step_duration>1 and step<(incident.accidentTime+incident.accidentDuration):
                self.change_lane(sinks)

            # Read traffic state in each time stamp
            # Check for congestion
            res, rest = divmod(step, self.simulation.sim_step_duration)
            if rest == 0:
                traffic_state = self.read_traffic_state(sinks)
                if TrafficAnalyzer.isVSLControlActivated:
                    self.update_vsl(sinks)
                consumer.send(traffic_state)

            if step == incident.accidentTime:
                edge_incident_id = traci.lane.getEdgeID(incident.lane_id)
                node = sinks[0][0].get_node_by_edgeID(edge_incident_id)
                lc_nodes = Sink.trafficAnalyzer.notify_congestion_detected(sinks[0][0], node, [incident.lane])
                Lc_is_active = TrafficAnalyzer.isLCControlActivated

            if step > incident.accidentTime:
                self.simulation.check_statistics_vehicles()


        traci.close()
        traci.switch(self.simulation.SIM)
        traci.close()

        gpms = self.__simulationManager.get_simulation_gpm_results()
        serializer = GlobalPerformanceMeasurementSerializer(gpms, many=True)
        consumer.send(serializer.data)

        consumer.disconnect()

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

    def update_vsl(self, sinks):
        for sink in sinks:
            sink[0].update_vsl()

    def set_sumo_LC_Model(self, lc_nodes, mode):
        for node in lc_nodes:
            for veh_id in traci.edge.getLastStepVehicleIDs(node.edge.getID()):
                traci.vehicle.setLaneChangeMode(veh_id, mode)