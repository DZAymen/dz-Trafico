from dzTrafico.Consumers.RealTimeTrafficState import RealTimeTrafficStateConsumer
from dzTrafico.Consumers.SimulationCreationConsumer import SimulationCreationConsumer
from dzTrafico.Consumers.LaneChangeRecommendation import LaneChangeRecommendationConsumer
from dzTrafico.Consumers.VSLConsumer import VSLConsumer
from channels.routing import route_class

channel_routing = [
    route_class(RealTimeTrafficStateConsumer, path=r"^/simulation/api/realtimetrafficstate/$"),
    route_class(SimulationCreationConsumer, path=r"^/simulation/api/simulationcreation/$"),
    route_class(LaneChangeRecommendationConsumer, path=r"^/simulation/api/lcrecommendations/$"),
    route_class(VSLConsumer, path=r"^/simulation/api/vsl/$")
]