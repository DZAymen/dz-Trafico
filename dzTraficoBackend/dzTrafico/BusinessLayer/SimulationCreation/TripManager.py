from dzTrafico.BusinessEntities.Flow import FlowPoint

class TripManager:

    __inflowPoints = []
    __outflowPoints = []

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    # The goal of this method is to define flows from flowPoints
    # and then generate the flow file which will be included in
    # the simulation config file
    def get_flows_file(self, flowPoints):
        self.generate_flows(flowPoints)
        return "flows.xml"

    #Define Flows from FlowPoints
    def generate_flows(self, flowPoints):
        self.__inflowPoints = []
        self.__outflowPoints = []
        for flowPoint in flowPoints:
            if flowPoint.type == FlowPoint.startType:
                self.__inflowPoints.append(flowPoint)
            elif flowPoint.type == FlowPoint.endType:
                self.__outflowPoints.append(flowPoint)
        print self.__inflowPoints
        print self.__outflowPoints