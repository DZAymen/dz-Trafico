import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation
import lxml.etree as etree
from dzTrafico.BusinessEntities.Simulation import Simulation

class QueueMeasurementsController:

    def __init__(self, simulation):
        # Initialize necessary file paths
        self.simulation = simulation

    def get_queue_measurements(self):
        noControl_queue = self.get_QM(self.simulation.queue_output)
        vsl_lc_queue = self.get_QM(self.simulation.queue_output_vsl_lc)
        print noControl_queue
        print vsl_lc_queue


    def get_QM(self, file):
        root = etree.parse(Simulation.project_directory + file)

        datas = root.getroot().getchildren()
        # print datas
        q_times = []
        for data in datas:
            q_time = 0
            lanes = data.getchildren()
            lanes = lanes[0].getchildren()
            for lane in lanes:
                q_time += float(lane.get("queueing_length"))
            q_times.append(q_time)

        return q_times