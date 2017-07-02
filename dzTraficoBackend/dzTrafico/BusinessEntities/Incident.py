from rest_framework import serializers
from Location import Location, LocationSerializer

class Incident(object):

    lanes = []

    def __init__(self, lon, lat, accidentTime, accidentDuration):
        self.lon = lon
        self.lat = lat
        self.position = Location(lon, lat)
        self.accidentTime = accidentTime
        self.accidentDuration = accidentDuration

    def set_lanes(self, lanes):
        self.lanes = lanes

class IncidentSerializer(serializers.Serializer):
    position = LocationSerializer()
    accidentTime = serializers.FloatField()
    accidentDuration = serializers.FloatField()

    def create(self, validated_data):
        return Incident(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["accidentTime"],
            validated_data["accidentDuration"]
        )