from channels.generic.websockets import JsonWebsocketConsumer
from dzTrafico.BusinessLayer.TrafficState.TrafficStateManager import TrafficStateManager
import json

class VSLConsumer(JsonWebsocketConsumer):
    reply_channel = None
    manager = TrafficStateManager.get_instance()

    def connect(self, message, **kwargs):
        message.reply_channel.send(
            {"accept": True}
        )
        VSLConsumer.reply_channel = message.reply_channel
        self.manager.set_VSL_consumer(self)

    def receive(self, content, **kwargs):
        pass

    def send(self, content, close=False):
        VSLConsumer.reply_channel.send(
            {
                "text": json.dumps(content)
            },
            immediately=True
        )

    def disconnect(self, message, **kwargs):
        pass