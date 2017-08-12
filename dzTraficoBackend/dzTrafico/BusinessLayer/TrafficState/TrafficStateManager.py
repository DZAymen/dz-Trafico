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
        print self.simulation.sim_duration
        for step in range(self.simulation.sim_duration):
            traffic_state = []
            traci.switch(self.simulation.SIM)
            traci.simulationStep()

            veh_id = self.simulation.check_incidents(step)
            if veh_id is not None and Simulation.incident_veh is None:
                Simulation.incident_veh = veh_id

            traci.switch(self.simulation.SIM_VSL_LC)
            traci.simulationStep()
            self.simulation.check_incidents(step)

            for sink in sinks:
                for edgeState in sink[0].read_traffic_state():
                    traffic_state.append(edgeState)

            edgeStateSerializer = EdgeStateSerializer(traffic_state, many=True)
            consumer.send(edgeStateSerializer.data)

        traci.close()
        traci.switch(self.simulation.SIM)
        traci.close()

        consumer.disconnect()