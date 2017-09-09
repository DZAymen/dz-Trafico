from rest_framework import serializers


class VehicleType(object):

    id = -1
    speedFactor = "normc(1,0.05,0.2,1)"

    def __init__(self, maxSpeed, length, height, width, minGap, acceleration, deceleration):
        VehicleType.id += 1
        self.id = VehicleType.id
        self.maxSpeed = maxSpeed
        self.length = length
        self.height = height
        self.width = width
        self.minGap = minGap
        self.acceleration = acceleration
        self.deceleration = deceleration

    def set_type_id(self, id):
        self.id = id

    def set_speed_factor(self, speedFactor):
        self.speedFactor = speedFactor

class VehicleTypeSerializer(serializers.Serializer):

    id = serializers.CharField(required=False)
    maxSpeed = serializers.FloatField()
    length = serializers.FloatField(required=False)
    width = serializers.FloatField(required=False)
    height = serializers.FloatField(required=False)
    minGap = serializers.FloatField()
    acceleration = serializers.FloatField()
    deceleration = serializers.FloatField()

    def create(self, validated_data):
        return VehicleType(
            validated_data["maxSpeed"],
            validated_data["length"],
            validated_data["height"],
            validated_data["width"],
            validated_data["minGap"],
            validated_data["acceleration"],
            validated_data["deceleration"]
        )

class VehicleTypesPercentagesSerializer(serializers.Serializer):
    id = serializers.CharField()
    percentage = serializers.FloatField()