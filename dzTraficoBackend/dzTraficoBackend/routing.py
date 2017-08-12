from dzTrafico.Consumers.RealTimeTrafficState import RealTimeTrafficStateConsumer
from channels.routing import route, route_class

channel_routing = [
    route_class(RealTimeTrafficStateConsumer, path=r"^/simulation/api/realtimetrafficstate/$")
]