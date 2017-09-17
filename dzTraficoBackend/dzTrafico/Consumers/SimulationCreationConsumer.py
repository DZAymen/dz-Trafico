from channels.generic.websockets import JsonWebsocketConsumer
from dzTrafico.BusinessLayer.SimulationManager import SimulationManager
import json

class SimulationCreationConsumer(JsonWebsocketConsumer):
    reply_channel = None
    manager = SimulationManager.get_instance()

    def connect(self, message, **kwargs):
        message.reply_channel.send(
            {"accept": True}
        )
        SimulationManager.reply_channel = message.reply_channel

    def receive(self, content, **kwargs):
        print content
        if content["createSim"]:
            self.manager.create_simulation(self)

    def send(self, content, close=False):
        SimulationManager.reply_channel.send(
            {
                "text": json.dumps(content)
            },
            immediately=True
        )

    def disconnect(self, message, **kwargs):
        pass