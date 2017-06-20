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
    inflowPointSerializer = InFlowPointSerializer(data=request.data, many=True)
    inflowPointSerializer.is_valid(raise_exception=True)

    inFlowPoints = []
    for data in request.data:
        inFlowPoints.append(
            InFlowPoint(
                data["location"]["lng"],
                data["location"]["lat"],
                data["departTime"],
                data["flow"])
        )

    simulationManager.add_inflows(inFlowPoints)
    return Response(status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def add_traffic_outflow(request):
    # request.data validation
    outflowPointSerializer = OutFlowPointSerializer(data=request.data, many=True)
    outflowPointSerializer.is_valid(raise_exception=True)

    outFlowPoints = []
    for data in request.data:
        outFlowPoints.append(
            OutFlowPoint(
                data["location"]["lng"],
                data["location"]["lat"],
                data["flow"])
        )

    simulationManager.add_outflows(outFlowPoints)
    return Response(status.HTTP_202_ACCEPTED)

#Post vehicle types
@api_view(['POST'])
def add_vehicle_types(request):
    vehicleTypes = []
    vehicleTypeSerializer = VehicleTypeSerializer(data=request.data, many=True)
    vehicleTypeSerializer.is_valid(raise_exception=True)

    for data in request.data:
        vehicleTypes.append(
            VehicleType(
                data["max_speed"],
                data["length"],
                data["min_gap"],
                data["speed_factor"],
                data["speed_dev"],
                data["acceleration"],
                data["deceleration"],
                data["sigma"],
                data["tau"]
            ))

    simulationManager.add_vehicule_types(vehicleTypes)
    return Response(status.HTTP_201_CREATED)

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
    incidentSerializer = IncidentSerializer(data=request.data, many=True)
    incidentSerializer.is_valid(raise_exception=True)
    #Create incidents objects
    incidents = []
    for incident in request.data:
        incidents.append(
            Incident(
                incident["location"]["lng"],
                incident["location"]["lat"],
                incident["time"]
            )
        )
    simulationManager.add_incidents(incidents)
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
