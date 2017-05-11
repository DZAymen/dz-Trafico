from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.MapBox import MapBox, MapBoxSerializer

simulationManager = SimulationManager.get_instance()

#Post the selected map
@api_view(['POST'])
def set_simulation_map(request):
    #request.data validation
    mapBoxSerializer = MapBoxSerializer(data=request.data)
    mapBoxSerializer.is_valid(raise_exception=True)
    #Call SimulationManager to pass the mapBox to the simulationCreator
    simulationManager.set_map(mapBoxSerializer.data)
    return Response(status.HTTP_201_CREATED)

#Post sensors list
@api_view(['POST'])
def add_sensors(request):
    # request.data validation
    simulationManager.add_sensors(request.data)
    return Response(status.HTTP_202_ACCEPTED)

#Post traffic flow
@api_view(['POST'])
def set_traffic_flow(request):
    # request.data validation
    simulationManager.set_traffic_flow(request.data)
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
    if request.data["configCompleted"]:
        simulationManager.createSimulation()
        return Response(status.HTTP_202_ACCEPTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
