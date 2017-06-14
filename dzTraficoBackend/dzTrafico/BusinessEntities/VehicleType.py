from rest_framework import serializers


class VehicleType(object):

    def __init__(self, flow, minGap, speedFactor, speedDev, acceleration, deceleration, sigma, tau):
        self.flow = flow
        self.minGap = minGap
        self.speedFactor = speedFactor
        self.speedDev = speedDev
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.sigma = sigma
        self.tau = tau


class VehicleTypeSerializer(serializers.Serializer):

    flow = serializers.FloatField()
    minGap = serializers.FloatField()
    speedFactor = serializers.FloatField()
    speedDev = serializers.FloatField()
    acceleration = serializers.FloatField()
    deceleration = serializers.FloatField()
    sigma = serializers.FloatField()
    tau = serializers.FloatField()
