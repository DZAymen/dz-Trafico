from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dzTrafico.BusinessLayer.SimulationManager import SimulationManager

simulationManager = SimulationManager.get_instance()

# Get simulation GlobalPerformanceMeasurements
@api_view(['GET'])
def get_simulation_gpm_results(request):
    gpm_results = simulationManager.get_simulation_gpm_results()
    # return a json format of gpm_results
    return Response(status.HTTP_201_CREATED)
