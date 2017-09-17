from channels.generic.websockets import JsonWebsocketConsumer
from dzTrafico.BusinessLayer.TrafficState.TrafficStateManager import TrafficStateManager
import json

class RealTimeTrafficStateConsumer(JsonWebsocketConsumer):
    reply_channel = None
    manager = TrafficStateManager.get_instance()

    def connect(self, message, **kwargs):
        message.reply_channel.send(
            {"accept": True},
            immediately=True
        )
        RealTimeTrafficStateConsumer.reply_channel = message.reply_channel
        self.manager.start(self)

    def receive(self, content, **kwargs):
        # if content["startSim"]:
        #     self.manager.start(self)
        pass

    def send(self, content, close=False):
        RealTimeTrafficStateConsumer.reply_channel.send(
            {
                "text": json.dumps(content)
            },
            immediately=True
        )

    def disconnect(self, message, **kwargs):
        pass