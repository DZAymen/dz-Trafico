"""dzTraficoBackend URL Configuration
"""

from django.conf.urls import url, include
from django.contrib import admin
from dzTrafico.views import home

from dzTrafico.ServiceLayer import SimulationCreationService, StatisticsService

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', dzTrafico.views.home),

    url(r'^api/simulation/run$', SimulationCreationService.run_simulation),

    #Simulation Creation Routes _________________________________________________________________
    url(r'^api/creation/map$', SimulationCreationService.set_simulation_map),
    url(r'^api/creation/trafficflow/departs$', SimulationCreationService.add_traffic_inflow),
    url(r'^api/creation/trafficflow/arrivals$', SimulationCreationService.add_traffic_outflow),
    url(r'^api/creation/incident$', SimulationCreationService.add_incidents),
    url(r'^api/creation/vehicletypes$', SimulationCreationService.add_vehicle_types),
    url(r'^api/creation/vehicletypespercentages$', SimulationCreationService.add_vehicle_types_percentages),
    url(r'^api/creation/sensorsdistance$', SimulationCreationService.set_sensors_distance),
    url(r'^api/creation/config$', SimulationCreationService.update_configuration_state),

    #Simulation Results Routes _________________________________________________________________
    url(r'^api/statistics/gpm$', StatisticsService.get_simulation_gpm_results),
]
