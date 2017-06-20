from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessEntities.MapBox import MapBox, MapBoxSerializer
from dzTrafico.BusinessEntities.Flow import InFlowPoint, InFlowPointSerializer, OutFlowPoint, OutFlowPointSerializer
from dzTrafico.BusinessEntities.VehicleType import VehicleType, VehicleTypeSerializer, VehicleTypesPercentagesSerializer
from dzTrafico.BusinessEntities.Incident import Incident, IncidentSerializer

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
    simulationManager.set_traffic_flow()
    return Response(status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def add_traffic_inflow(request):
    # request.data validation
    inflowPointSerializer = InFlowPointSerializer(data=request.data)
    inflowPointSerializer.is_valid(raise_exception=True)

    simulationManager.add_inflows(
        InFlowPoint(
            request.data["location"]["lng"],
            request.data["location"]["lat"],
            request.data["departTime"],
            request.data["flow"]
        )
    )
    return Response(data=inflowPointSerializer.data,status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def add_traffic_outflow(request):
    # request.data validation
    outflowPointSerializer = OutFlowPointSerializer(data=request.data)
    outflowPointSerializer.is_valid(raise_exception=True)

    simulationManager.add_outflows(
        OutFlowPoint(
                request.data["location"]["lng"],
                request.data["location"]["lat"],
                request.data["flow"]
        )
    )
    return Response(data=outflowPointSerializer.data,status=status.HTTP_202_ACCEPTED)

#Post vehicle types
@api_view(['POST'])
def add_vehicle_types(request):
    vehicleTypes = []
    vehicleTypeSerializer = VehicleTypeSerializer(data=request.data)
    vehicleTypeSerializer.is_valid(raise_exception=True)

    simulationManager.add_vehicule_types(
        VehicleType(
                request.data["max_speed"],
                request.data["length"],
                request.data["min_gap"],
                request.data["speed_factor"],
                request.data["speed_dev"],
                request.data["acceleration"],
                request.data["deceleration"],
                request.data["sigma"],
                request.data["tau"]
            )
    )
    return Response(data=vehicleTypeSerializer.data,status=status.HTTP_201_CREATED)

@api_view(['POST'])
def add_vehicle_types_percentages(request):
    #Vehicle types percentages validation
    vehicleTypesPercentagesSerializer = VehicleTypesPercentagesSerializer(data=request.data, many=True)
    vehicleTypesPercentagesSerializer.is_valid(raise_exception=True)

    simulationManager.set_vehicle_types_percentages(request.data)
    return Response(status.HTTP_201_CREATED)

#Post incidents list
@api_view(['POST'])
def add_incidents(request):

    # request.data validation
    incidentSerializer = IncidentSerializer(data=request.data)
    incidentSerializer.is_valid(raise_exception=True)

    simulationManager.add_incidents(
        Incident(
                request.data["location"]["lng"],
                request.data["location"]["lat"],
                request.data["time"],
                request.data["duration"]
            )
    )
    #response = Response(status.HTTP_202_ACCEPTED)
    #response = JSon
    return Response(data=incidentSerializer.data,status=status.HTTP_202_ACCEPTED)

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
