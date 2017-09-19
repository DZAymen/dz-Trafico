import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class FlowMeasurementsController:

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_incident_flow_measurements(self):
        flow = dict()
        flow["time"], flow["with_control"] = self.get_incident_FM(self.simulation.incident_sensors_output)
        t, flow["no_control"] = self.get_incident_FM(self.simulation.incident_sensors_nocntrol_output)
        return flow

    def get_incident_FM(self, output_file):
        root = etree.parse(Simulation.project_directory + output_file)

        intervals = root.getroot().getchildren()

        flows = []
        for interval_num in range(0, len(intervals), 3):
            flow = 0
            for i in range(0,3):
                flow += float(intervals[interval_num + i].get("flow"))
            flows.append(flow)

        time = []
        for i in range(len(flows)):
            time.append(i * Simulation.sim_step_duration)

        return time, flows