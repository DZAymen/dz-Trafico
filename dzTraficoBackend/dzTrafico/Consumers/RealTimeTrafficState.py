from channels.generic.websockets import JsonWebsocketConsumer
from dzTrafico.BusinessLayer.TrafficState.TrafficStateManager import TrafficStateManager
import json

class RealTimeTrafficStateConsumer(JsonWebsocketConsumer):
    reply_channel = None
    manager = TrafficStateManager.get_instance()

    def connect(self, message, **kwargs):
        message.reply_channel.send(
            {"accept": True}
        )
        RealTimeTrafficStateConsumer.reply_channel = message.reply_channel

    def receive(self, content, **kwargs):
        if content["startSim"]:
            self.manager.start(self)

    def send(self, content, close=False):
        RealTimeTrafficStateConsumer.reply_channel.send(
            {
                "text": json.dumps({"i": content})
            },
            immediately=True
        )

    def disconnect(self, message, **kwargs):
        pass