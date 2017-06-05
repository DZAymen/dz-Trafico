from dzTrafico.BusinessEntities.Flow import FlowPoint, Flow

class TripManager:

    __inflowPoints = []
    __outflowPoints = []

    def __init__(self, networkManager):
        self.__networkManager = networkManager

    # The goal of this method is to define flows from flowPoints
    # and then generate the flow file which will be included in
    # the simulation config file
    def get_flows_file(self, flowPoints):
        self.flows = self.generate_flows(flowPoints)
        print self.flows
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
        return self.define_flow_combinations(self.__inflowPoints, self.__outflowPoints)

    def define_flow_combinations(self, inflowPoints, outflowPoints):
        flows = []
        for inflowPoint in inflowPoints:
            for outflowPoint in outflowPoints:
                # set the start and end edges for a new flow
                flows.append(
                    Flow(
                        self.__networkManager.get_edgeId_from_geoCoord(inflowPoint.lon, inflowPoint.lat),
                        self.__networkManager.get_edgeId_from_geoCoord(outflowPoint.lon, outflowPoint.lat),
                        200
                    ))
        return flows
