from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.Simulation import Simulation
from dzTrafico.BusinessEntities.EdgeState import EdgeStateSerializer
import traci
import threading

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

        self.simulation.start_simulation()

        for step in range(self.simulation.sim_duration):
            traci.switch(self.simulation.SIM)
            traci.simulationStep()

            veh_id = self.simulation.check_incidents(step)
            if veh_id is not None and Simulation.incident_veh is None:
                Simulation.incident_veh = veh_id

            traci.switch(self.simulation.SIM_VSL_LC)
            traci.simulationStep()
            self.simulation.check_incidents(step)

            # Check for LanChanges in nodes' recommendations
            if self.simulation.sim_step_duration>1:
                self.change_lane(sinks)

            # Read traffic state in each time stamp
            # Check for congestion
            res, rest = divmod(step, self.simulation.sim_step_duration)
            if rest == 0:
                traffic_state = self.read_traffic_state(sinks)
                consumer.send(traffic_state)

        traci.close()
        traci.switch(self.simulation.SIM)
        traci.close()

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