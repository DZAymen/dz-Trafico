from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.utils.six import BytesIO

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
    map_box = mapBoxSerializer.create(mapBoxSerializer.validated_data)

    simulationManager.set_map(map_box)
    return Response(status.HTTP_201_CREATED)

#POST: add an inflow point
#GET: get inflow points
@api_view(['POST', 'GET'])
def add_traffic_inflow(request):
    if request.method == 'POST':
        #Validate inflow point request data
        inflowPointSerializer = InFlowPointSerializer(data=request.data)
        inflowPointSerializer.is_valid(raise_exception=True)
        #Create inflow point instance
        inFlowPoint = inflowPointSerializer.create(inflowPointSerializer.validated_data)
        #Add the inflow point
        simulationManager.add_inflow(inFlowPoint)

        data = inflowPointSerializer.data
        data["id"] = inFlowPoint.id

        return Response(data=data,status=status.HTTP_202_ACCEPTED)

    elif request.method == 'GET':
        inFlowPoints = simulationManager.get_inflow_points()
        print inFlowPoints
        return Response(data=[], status=status.HTTP_200_OK)

#POST: add an outflow point
#GET: get outflow points
@api_view(['POST', 'GET'])
def add_traffic_outflow(request):
    if request.method == 'POST':
        # Validate outflow point request data
        outflowPointSerializer = OutFlowPointSerializer(data=request.data)
        outflowPointSerializer.is_valid(raise_exception=True)
        #Create outflow point instance
        outFlowPoint = outflowPointSerializer.create(outflowPointSerializer.validated_data)
        #Add the outflow point
        simulationManager.add_outflow(outFlowPoint)

        data = outflowPointSerializer.data
        data["id"] = outFlowPoint.id

        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'GET':
        outFlowPoints = simulationManager.get_outflow_points()
        print outFlowPoints
        return Response(data=[], status=status.HTTP_200_OK)

# Post incidents list
@api_view(['POST', 'GET'])
def add_incidents(request):

    if request.method == 'POST':
        # Validate incident request data
        incidentSerializer = IncidentSerializer(data=request.data)
        incidentSerializer.is_valid(raise_exception=True)
        # Create incident instance
        incident = incidentSerializer.create(incidentSerializer.validated_data)
        # Add incident to incidents list
        simulationManager.add_incident(incident)

        return Response(data=incidentSerializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == 'GET':
            incidents = simulationManager.get_incidents()
            print incidents
            return Response(data=[], status=status.HTTP_200_OK)

#Post vehicle types
@api_view(['POST', 'GET'])
def add_vehicle_types(request):
    if request.method == 'POST':
        # Validate vehicle type request data
        vehicleTypeSerializer = VehicleTypeSerializer(data=request.data)
        vehicleTypeSerializer.is_valid(raise_exception=True)

        # Create vehicle type instance
        vehicleType = vehicleTypeSerializer.create(vehicleTypeSerializer.validated_data)

        # Add vehicle type to vehicle types list
        simulationManager.add_vehicule_type(vehicleType)

        return Response(data=vehicleTypeSerializer.data,status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        vehicle_types = simulationManager.get_vehicle_types()
        serializer = VehicleTypeSerializer(vehicle_types, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_vehicle_types_percentages(request):
    #Vehicle types percentages validation
    vehicleTypesPercentagesSerializer = VehicleTypesPercentagesSerializer(data=request.data, many=True)
    vehicleTypesPercentagesSerializer.is_valid(raise_exception=True)

    simulationManager.set_vehicle_types_percentages(request.data)
    return Response(status.HTTP_201_CREATED)

#Post configuration state
# :true means to launch the simulation creation
@api_view(['POST'])
def update_configuration_state(request):
    # request.data validation

    #timeMeasure
    #startTime
    simulationManager.add_sensors(request.data["distance"])
    if request.data["configCompleted"]:
        simulationManager.create_simulation()
        return Response(status.HTTP_202_ACCEPTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
