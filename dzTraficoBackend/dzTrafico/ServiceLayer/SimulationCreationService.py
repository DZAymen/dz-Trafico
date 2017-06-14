from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.MapBox import MapBox, MapBoxSerializer
from dzTrafico.BusinessEntities.Flow import InFlowPoint, InFlowPointSerializer, OutFlowPoint, OutFlowPointSerializer

simulationManager = SimulationManager.get_instance()

#Post the selected map
@api_view(['POST'])
def set_simulation_map(request):
    #request.data validation
    mapBoxSerializer = MapBoxSerializer(data=request.data)
    mapBoxSerializer.is_valid(raise_exception=True)
    #Call SimulationManager to pass the mapBox to the simulationCreator
    map_box = MapBox(request.data["left"], request.data["bottom"], request.data["right"], request.data["top"])
    simulationManager.set_map(map_box)
    return Response(status.HTTP_201_CREATED)

#Post traffic flow
@api_view(['POST'])
def set_traffic_flow(request):
    # request.data validation

    inflowPointSerializer = InFlowPointSerializer(data=request.data["inFlows"], many=True)
    inflowPointSerializer.is_valid(raise_exception=True)

    outflowPointSerializer = OutFlowPointSerializer(data=request.data["outFlows"], many=True)
    outflowPointSerializer.is_valid(raise_exception=True)

    inFlowPoints = []
    outFlowPoints = []
    for data in request.data["inFlows"]:
        inFlowPoints.append(InFlowPoint(data["lon"], data["lat"], data["depart_time"], data["value"]))
    for data in request.data["outFlows"]:
        outFlowPoints.append(OutFlowPoint(data["lon"], data["lat"], data["value"]))

    simulationManager.set_traffic_flow(inFlowPoints, outFlowPoints)
    return Response(status.HTTP_202_ACCEPTED)

#Post incidents list
@api_view(['POST'])
def add_incidents(request):
    # request.data validation
    simulationManager.add_incidents(request.data)
    return Response(status.HTTP_202_ACCEPTED)

#Post configuration state
# :true means to launch the simulation creation
@api_view(['POST'])
def update_configuration_state(request):
    # request.data validation
    simulationManager.add_sensors(request.data["sensors_distance"])
    if request.data["configCompleted"]:
        simulationManager.create_simulation()
        return Response(status.HTTP_202_ACCEPTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
