from channels.generic.websockets import JsonWebsocketConsumer
from dzTrafico.BusinessLayer.TrafficState.TrafficStateManager import TrafficStateManager
import json

class LaneChangeRecommendationConsumer(JsonWebsocketConsumer):
    reply_channel = None
    manager = TrafficStateManager.get_instance()

    def connect(self, message, **kwargs):
        message.reply_channel.send(
            {"accept": True}
        )
        LaneChangeRecommendationConsumer.reply_channel = message.reply_channel
        self.manager.set_LC_consumer(self)

    def receive(self, content, **kwargs):
        pass

    def send(self, content, close=False):
        LaneChangeRecommendationConsumer.reply_channel.send(
            {
                "text": json.dumps(content)
            },
            immediately=True
        )

    def disconnect(self, message, **kwargs):
        pass