import threading

class TrafficStateManager:
    __trafficStateManager = None

    @staticmethod
    def get_instance():
        if TrafficStateManager.__trafficStateManager is None:
            TrafficStateManager.__trafficStateManager = TrafficStateManager()
        return TrafficStateManager.__trafficStateManager

    def start(self, consumer):
        for i in range(0,5):
            consumer.send(i)
            threading._sleep(5)
            print i