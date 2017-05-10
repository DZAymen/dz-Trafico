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
    url(r'^api/creation/map$', SimulationCreationService.set_map),
    url(r'^api/creation/sensors$', SimulationCreationService.add_sensors),
    url(r'^api/creation/trafficflow$', SimulationCreationService.set_traffic_flow),
    url(r'^api/creation/incident$', SimulationCreationService.add_incidents),
    url(r'^api/creation/state$', SimulationCreationService.update_configuration_state),

    #Simulation Creation Routes _________________________________________________________________
]
