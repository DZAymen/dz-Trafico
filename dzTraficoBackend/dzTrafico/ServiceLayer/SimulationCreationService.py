from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

#Post the selected map
@api_view(['POST'])
def set_map(request):
    return Response(request.data)

#Post sensors list
@api_view(['POST'])
def add_sensors(request):
    return Response(request.data)

#Post traffic flow
@api_view(['POST'])
def set_traffic_flow(request):
    return Response(request.data)

#Post incidents list
@api_view(['POST'])
def add_incidents(request):
    return Response(request.data)

#Post configuration state
# :true means to launch the simulation creation
@api_view(['POST'])
def update_configuration_state(request):
    return Response(request.data)