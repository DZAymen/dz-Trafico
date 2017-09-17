from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
from dzTrafico.BusinessLayer.Statistics.GlobalPerformanceMeasurementsController import GlobalPerformanceMeasurementSerializer
from matplotlib.pyplot import plot

simulationManager = SimulationManager.get_instance()

# Get simulation GlobalPerformanceMeasurements
@api_view(['GET'])
def get_simulation_gpm_results(request):
    gpm_results = simulationManager.get_simulation_gpm_results()
    # return a json format of gpm_results
    serializer = GlobalPerformanceMeasurementSerializer(gpm_results, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_incident_flow_stats(request):
    incident_flow_stats = simulationManager.get_incident_flow()
    simulationManager.get_queue_measurements()

    return Response(data=incident_flow_stats, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_incident_density_stats(request):
    incident_density_stats, time = simulationManager.get_density_flow()
    simulationManager.get_queue_measurements()

    # Plot flow stats
    print time, incident_density_stats
    plot(time, incident_density_stats)

    return Response(status=status.HTTP_200_OK)