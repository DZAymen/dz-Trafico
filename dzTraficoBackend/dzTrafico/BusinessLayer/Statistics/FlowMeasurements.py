import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class FlowMeasurementsController:

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_incident_flow_measurements(self):
        root = etree.parse(Simulation.project_directory + self.simulation.incident_sensors_output)

        intervals = root.getroot().getchildren()

        flows = []
        for interval_num in range(0, len(intervals), 3) :
            flow = 0
            for i in range(0,3):
                flow += float(intervals[interval_num + i].get("flow"))
            flows.append(flow)

        time = []
        for i in range(len(flows)):
            time.append(i * Simulation.sim_step_duration)

        # plot(time, newflows)
        return flows, time
