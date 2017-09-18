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
    url(r'^api/creation/trafficflow/departs/(?P<pk>[0-9]+)$', SimulationCreationService.delete_traffic_inflow),
    url(r'^api/creation/trafficflow/arrivals$', SimulationCreationService.add_traffic_outflow),
    url(r'^api/creation/trafficflow/arrivals/(?P<pk>[0-9]+)$', SimulationCreationService.delete_traffic_outflow),
    url(r'^api/creation/incident$', SimulationCreationService.add_incidents),
    url(r'^api/creation/incident/(?P<pk>[0-9]+)$', SimulationCreationService.delete_incident),
    url(r'^api/creation/vehicletypes$', SimulationCreationService.add_vehicle_types),
    url(r'^api/creation/vehicletypespercentages$', SimulationCreationService.add_vehicle_types_percentages),
    url(r'^api/creation/config$', SimulationCreationService.update_configuration_state),

    #Simulation Results Routes _________________________________________________________________
    url(r'^api/statistics/gpm$', StatisticsService.get_simulation_gpm_results),
    url(r'^api/statistics/incidentflowstats$', StatisticsService.get_incident_flow_stats),
    url(r'^api/statistics/incidentdensitystats$', StatisticsService.get_incident_density_stats),
]
