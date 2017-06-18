from rest_framework import serializers


class VehicleType(object):

    type_id = -1

    def __init__(self, max_speed, length, min_gap, speed_factor, speed_dev, acceleration, deceleration, sigma, tau):
        VehicleType.type_id += 1
        self.type_id = "vtype" + str(VehicleType.type_id)
        self.max_speed = max_speed
        self.length = length
        self.min_gap = min_gap
        self.speed_factor = speed_factor
        self.speed_dev = speed_dev
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.sigma = sigma
        self.tau = tau

    def set_type_id(self, type_id):
        self.type_id = type_id

class VehicleTypeSerializer(serializers.Serializer):

    max_speed = serializers.FloatField()
    length = serializers.FloatField()
    min_gap = serializers.FloatField()
    speed_factor = serializers.FloatField()
    speed_dev = serializers.FloatField()
    acceleration = serializers.FloatField()
    deceleration = serializers.FloatField()
    sigma = serializers.FloatField()
    tau = serializers.FloatField()

class VehicleTypesPercentagesSerializer(serializers.Serializer):
    type_id = serializers.CharField()
    percentage = serializers.FloatField()