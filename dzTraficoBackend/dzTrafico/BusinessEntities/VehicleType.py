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

    maxSpeed = serializers.FloatField()
    length = serializers.FloatField(required=False)
    minGap = serializers.FloatField()
    speed_factor = serializers.FloatField(required=False)
    speed_dev = serializers.FloatField(required=False)
    accel = serializers.FloatField()
    decel = serializers.FloatField()
    sigma = serializers.FloatField()
    tau = serializers.FloatField()
    #Impatience

class VehicleTypesPercentagesSerializer(serializers.Serializer):
    type_id = serializers.CharField()
    percentage = serializers.FloatField()