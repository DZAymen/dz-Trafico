"""dzTraficoBackend URL Configuration
"""

from django.conf.urls import url, include
from django.contrib import admin
from dzTrafico.views import home

from dzTrafico.ServiceLayer import SimulationCreationService

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', dzTrafico.views.home),

    #Simulation Creation Routes _________________________________________________________________
    url(r'^api/creation/map$', SimulationCreationService.set_simulation_map),
    url(r'^api/creation/trafficflow/departs$', SimulationCreationService.add_traffic_inflow),
    url(r'^api/creation/trafficflow/arrivals$', SimulationCreationService.add_traffic_outflow),
    url(r'^api/creation/incident$', SimulationCreationService.add_incidents),
    url(r'^api/creation/vehicletypes$', SimulationCreationService.add_vehicle_types),
    url(r'^api/creation/vehicletypespercentages$', SimulationCreationService.add_vehicle_types_percentages),
    url(r'^api/creation/state$', SimulationCreationService.update_configuration_state),

    #Simulation Creation Routes _________________________________________________________________
]
