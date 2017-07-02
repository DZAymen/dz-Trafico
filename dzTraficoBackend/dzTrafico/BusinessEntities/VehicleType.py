from rest_framework import serializers


class VehicleType(object):

    id = -1

    def __init__(self, maxSpeed, length, minGap, speedFactor, speedDev, accel, decel, sigma, tau):
        VehicleType.id += 1
        self.id = VehicleType.id
        self.maxSpeed = maxSpeed
        self.length = length
        self.minGap = minGap
        self.speedFactor = speedFactor
        self.speedDev = speedDev
        self.accel = accel
        self.decel = decel
        self.sigma = sigma
        self.tau = tau

    def set_type_id(self, id):
        self.id = id

class VehicleTypeSerializer(serializers.Serializer):

    maxSpeed = serializers.FloatField()
    length = serializers.FloatField(required=False)
    minGap = serializers.FloatField()
    speedFactor = serializers.FloatField(required=False)
    speedDev = serializers.FloatField(required=False)
    accel = serializers.FloatField()
    decel = serializers.FloatField()
    sigma = serializers.FloatField()
    tau = serializers.FloatField()
    #Impatience

    def create(self, validated_data):
        return VehicleType(
            validated_data["maxSpeed"],
            4,
            #validated_data["length"],
            validated_data["minGap"],
            0.9,
            #validated_data["speedFactor"],
            0,
            #validated_data["speedDev"],
            validated_data["accel"],
            validated_data["decel"],
            validated_data["sigma"],
            validated_data["tau"]
        )

class VehicleTypesPercentagesSerializer(serializers.Serializer):
    id = serializers.CharField()
    percentage = serializers.FloatField()