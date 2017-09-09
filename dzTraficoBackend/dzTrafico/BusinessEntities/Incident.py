from rest_framework import serializers
from Location import Location, LocationSerializer

class Incident(object):

    def __init__(self, lon, lat, accidentTime, accidentDuration, lane):
        self.lon = lon
        self.lat = lat
        self.position = Location(lon, lat)
        self.accidentTime = accidentTime
        self.accidentDuration = accidentDuration
        self.lane = lane

    def set_lane(self, lane_id):
        self.lane_id = lane_id

    def set_edge(self, edge):
        self.edge = edge

    def set_lane_position(self, lane_position):
        self.lane_position = lane_position

class IncidentSerializer(serializers.Serializer):
    position = LocationSerializer()
    accidentTime = serializers.FloatField()
    accidentDuration = serializers.FloatField()
    lane = serializers.IntegerField()

    def create(self, validated_data):
        return Incident(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["accidentTime"],
            validated_data["accidentDuration"],
            validated_data["lane"]
        )